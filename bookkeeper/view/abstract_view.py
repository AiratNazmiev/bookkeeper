"""
Реализация абстрактоного интерфейса AbstractView
"""

from abc import ABC, abstractmethod
from typing import Iterable, Callable

from bookkeeper.view.window import Window

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget


class AbstractView(ABC):
    """Абстактный класс компонента View """
    # Окно приложения
    main_window: Window

    @abstractmethod
    def create_categories(self,
                          item_list: list[Category]
                          ) -> None:
        pass

    @abstractmethod
    def create_expenses(self,
                        item_list: list[Expense]
                        ) -> None:
        pass

    @abstractmethod
    def create_budgets(self,
                       item_list: list[Budget]
                       ) -> None:
        pass

    @abstractmethod
    def set_category_add_handler(self,
                                 handler: Callable[[str, str | None], None]
                                 ) -> None:
        pass

    @abstractmethod
    def set_category_modify_handler(self,
                                    handler: Callable[[str, str, str | None], None]
                                    ) -> None:
        pass

    @abstractmethod
    def set_category_delete_handler(self,
                                    handler: Callable[[str], None]
                                    ) -> None:
        pass

    @abstractmethod
    def set_category_name_check(self,
                                handler: Callable[[str], None]
                                ) -> None:
        pass

    @abstractmethod
    def add_category(self, name: str, parent: str | None) -> None:
        pass

    @abstractmethod
    def modify_category(self, cat_name: str,
                        new_name: str,
                        new_parent: str | None
                        ) -> None:
        pass

    @abstractmethod
    def delete_category(self, cat_name: str) -> None:
        pass

    @abstractmethod
    def set_budget_modify_handler(self,
                                  handler: Callable[[int | None, str, str], None]
                                  ) -> None:
        pass

    @abstractmethod
    def modify_budget(self, pk: int, new_limit: str, period: str) -> None:
        pass

    @abstractmethod
    def set_expense_add_handler(self,
                                handler: Callable[[str, str, str], None]
                                ) -> None:
        pass

    @abstractmethod
    def set_expense_delete_handler(self,
                                   handler: Callable[[Iterable[int]], None]
                                   ) -> None:
        pass

    @abstractmethod
    def set_expense_modify_handler(self,
                                   handler: Callable[[int, str, str], None]
                                   ) -> None:
        pass

    @abstractmethod
    def add_expense(self, amount: str, cat_name: str, comment: str = "") -> None:
        pass

    @abstractmethod
    def delete_expenses(self, exp_pks: Iterable[int]) -> None:
        pass

    @abstractmethod
    def modify_expense(self, pk: int, attr: str, new_val: str) -> None:
        pass

    @abstractmethod
    def budget_limit_exceeded_message(self) -> None:
        pass
