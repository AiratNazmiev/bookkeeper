"""
TODO
"""

from abc import ABC, abstractmethod
from typing import Iterable, Callable

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget


class AbstractView(ABC):
    """Абстактный класс компонента View """
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
    def set_budget_modify_handler(self,
                                  handler: Callable[[int | None, str, str], None]
                                  ) -> None:
        pass
        
    @abstractmethod
    def set_expense_add_handler(self, 
                                handler: Callable[[str, str, str], None]
                                ) -> None:
        pass
        
    @abstractmethod
    def set_exppense_delete_handler(self,
                                    handler: Callable[[Iterable[int]], None]
                                    ) -> None:
        pass
        
    @abstractmethod
    def set_expense_modify_handler(self, 
                                   handler: Callable[[int, str, str], None]
                                   ) -> None:
        pass
        
    @abstractmethod
    def set_expense_exceeded_handler(self) -> None:
        pass