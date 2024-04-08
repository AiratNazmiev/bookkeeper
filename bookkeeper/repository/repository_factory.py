from typing import Callable, Any

from bookkeeper.repository.abstract_repository import Model
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository


def repository_factory(db_file: 'str | None' = None
                       ) -> Callable[[Model], Any]:

    if db_file is None:
        def memory_repository_factory(model: Model) -> Any:
            return MemoryRepository[model]()  # type: ignore
        return memory_repository_factory
    else:
        def sqlite_repositry_factory(model: Model) -> Any:
            return SQLiteRepository[model](db_file=db_file, cls=model)  # type: ignore
        return sqlite_repositry_factory
