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
    obj_cls: type
    fields: dict[str, Any]
    
    def __init__(self, db_file: str, cls: type) -> None:
        super().__init__()
                
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.obj_cls = cls
        self.fields.pop('pk')
        
    def add(self, obj: T) -> int | None:  # TODO: int | None(?)
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        
        names = ', '.join(self.fields.keys())   # можно вычислить однажды в init
        qs = ', '.join('?' * len(self.fields))  # можно вычислить однажды в init
        values = [getattr(obj, f) for f in self.fields]
        
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
    
    def _obj_adapter(self, pk: int, row: tuple[Any]) -> T:
        obj = self.obj_cls(**dict(zip(self.fields, row)))
        obj.pk = pk
        return obj
        
    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            row = cur.execute(
                f'SELECT * FROM {self.table_name} WHERE ROWID={pk}'
            ).fetchone()
        con.close()
        if row is None:
            return None
        return self._obj_adapter(pk, row)
    
    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            if where is not None:
                mask = [f'{f} LIKE ?' for f in where.keys()]
                rows = cur.execute(
                    f'SELECT ROWID, * FROM {self.table_name} '
                    f'WHERE {" AND ".join(mask)}',
                    list(where.values())
                ).fetchall()
            else:
                rows = cur.execute(
                    f'SELECT ROWID, * FROM {self.table_name} '
                ).fetchall()
        con.close()
        return [self._obj_adapter(pk=r[0], row=r[1:]) for r in rows]
    
    def get_all_substr(self, where: dict[str, str]) -> list[T]:
        substr_where = {f : f'%{s}%' for f, s  in where.items()}
        return self.get_all(substr_where)
    
    def update(self, obj: T) -> None:
        fields = ", ".join([f"{k}=?" for k in self.fields.keys()])
        values = [getattr(obj, f) for f in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                f'UPDATE {self.table_name} SET {fields} '
                f'WHERE ROWID={obj.pk}', values
            )
            # не обновили ни одной записи
            if cur.rowcount == 0: 
                raise ValueError('attempt to update object with unknown primary key')
        con.close()
        
    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f'DELETE FROM {self.table_name} WHERE ROWID={pk}')
            
            if cur.rowcount == 0:
                raise ValueError('attempt to delete object with unknown primary key')
        con.close()
    
    