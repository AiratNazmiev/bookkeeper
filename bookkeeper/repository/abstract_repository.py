"""
Модуль содержит описание абстрактного репозитория

Репозиторий реализует хранение объектов, присваивая каждому объекту уникальный
идентификатор в атрибуте pk (primary key). Объекты, которые могут быть сохранены
в репозитории, должны поддерживать добавление атрибута pk и не должны
использовать его для иных целей.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Protocol, Any


class Model(Protocol):  # pylint: disable=too-few-public-methods
    """
    Модель должна содержать атрибут pk
    """
    pk: int | None # TODO: or int | None(?)


T = TypeVar('T', bound=Model)


class AbstractRepository(ABC, Generic[T]):
    """
    Абстрактный репозиторий.
    Абстрактные методы:
    add
    get
    get_all
    update
    delete
    """

    @abstractmethod
    def add(self, obj: T) -> int | None:  # TODO: or int | None(?)
        """
        Добавить объект в репозиторий, вернуть id объекта,
        также записать id в атрибут pk.
        """

    @abstractmethod
    def get(self, pk: int) -> T | None:  # TODO: написать про возвращение None
        """ Получить объект по id """

    @abstractmethod
    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """
        
    @abstractmethod
    def get_all_substr(self, where: dict[str, str]) -> list[T]:
        """
        Получить все записи по некоторому условию для строчного типа
        where - условие в виде словаря {'название_поля': значение},
        где значение имеет тип строки. Для выполнения условия проверки 
        значения должны быть подстроками строки записи таблицы с полями
        'название_поля'
        """

    @abstractmethod
    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле pk. """

    @abstractmethod
    def delete(self, pk: int) -> None:
        """ Удалить запись """
