"""
Модуль описывает репозиторий, работающий c БД SQLite 
Реализуется на основе стандартной библиотеки sqlite3
"""

import sqlite3
from inspect import get_annotations
from typing import Any

from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):
    """
    TODO
    """
    db_file: str
    table_name: str
    fields: dict[str, Any]
    
    def __init__(self, db_file: str, cls: type) -> None:
        super().__init__()
        
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')
        
    def add(self, obj: T) -> int:  # TODO: int | None(?)
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        
        names = ', '.join(self.fields.keys())  # можно вычислить однажды в init
        qs = ', '.join("?" * len(self.fields))  # можно вычислить однажды в init
        values = [getattr(obj, f) for f in self.fields]  # можно вычислить однажды в init
        
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES({qs})',
                values
            )
            obj.pk = cur.lastrowid
        con.close()
        
        return obj.pk
        
    
        
        