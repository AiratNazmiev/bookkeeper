"""
Реализация интерфейса View, наследуемого от AbstractView
"""
from PySide6 import QtWidgets
from typing import Callable, Iterable, Any

from bookkeeper.view.abstract_view import AbstractView
from bookkeeper.view.window import Window
from bookkeeper.view.budget_table import WidgetBudgetTableBox
from bookkeeper.view.add_expense import WidgetAddExpenseBox
from bookkeeper.view.expense_table import WidgetExpenseTableBox
from bookkeeper.view.edit_category import WidgetEditCategory

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget


class View(AbstractView):
    """ Абстактный класс компонента View модели MVP """

    def __init__(self) -> None:
        super().__init__()

        # получение экземпляра QApplication
        self.app = QtWidgets.QApplication.instance()
        if self.app is None:
            raise RuntimeError("Ошибка получения экземпляра QApplication")

        self.categories: list[Category] = []
        self.expenses: list[Expense] = []
        self.budgets: list[Budget] = []

        # Настройка окна для редактирования категорий трат
        self.cats_edit_window = WidgetEditCategory(
            self.categories,
            self.add_category,
            self.delete_category
        )

        self.cats_edit_window.setWindowTitle("Редактирование категорий")
        self.cats_edit_window.resize(600, 600)

        # Получение основных элементов
        self.budget_table = WidgetBudgetTableBox(self.modify_budget)
        self.new_expense = WidgetAddExpenseBox(self.categories,
                                               self.cats_edit_window.show,
                                               self.add_expense)
        self.expenses_table = WidgetExpenseTableBox(self._category_pk2name,
                                                    self.modify_expense,
                                                    self.delete_expenses)

        # Настройка главного окна
        self.main_window = Window(
            self.budget_table,
            self.new_expense,
            self.expenses_table
        )
        self.main_window.resize(600, 700)

    @staticmethod
    def _try(widget: QtWidgets.QWidget, func: Any) -> Callable[[Any], None]:
        """ Обработка ошибки и вывод сообщения на экран """
        def inner(*args: Any, **kwargs: Any) -> None:
            try:
                func(*args, **kwargs)
            except ValueError as err:
                QtWidgets.QMessageBox.critical(widget, 'Ошибка!', str(err))
        return inner

    def _category_pk2name(self, pk: int) -> str:
        name = [c.name for c in self.categories if int(c.pk) == int(pk)]
        if len(name) > 0:
            return str(name[0])
        return ""

    ### Обработка категорий трат ###
    def create_categories(self, item_list: list[Category]) -> None:
        self.categories = item_list
        self.new_expense.set_categories(self.categories)
        self.cats_edit_window.set_categories(self.categories)

    # Установка обработчиков
    def set_category_add_handler(self,
                                 handler: Callable[[str, str | None], None]
                                 ) -> None:
        self.cat_adder = self._try(self.main_window, handler)

    def set_category_modify_handler(self,
                                    handler: Callable[[str, str, str | None], None]
                                    ) -> None:
        self.cat_modifier = self._try(self.main_window, handler)

    def set_category_delete_handler(self,
                                    handler: Callable[[str], None]
                                    ) -> None:
        self.cat_deleter = self._try(self.main_window, handler)

    def set_category_name_check(self, handler: Callable[[str], None]) -> None:
        self.cat_checker = self._try(self.main_window, handler)
        self.cats_edit_window.set_checker(self.cat_checker)

    # Вызовы обработчиков
    def add_category(self, name: str, parent: str | None) -> None:
        self.cat_adder(name, parent)

    def modify_category(self, cat_name: str,
                        new_name: str,
                        new_parent: str | None
                        ) -> None:
        self.cat_modifier(cat_name, new_name, new_parent)

    def delete_category(self, cat_name: str) -> None:
        self.cat_deleter(cat_name)

    ### Обработка расходов ###
    def create_expenses(self, exps: list[Expense]) -> None:
        self.expenses = exps
        self.expenses_table.set_expense(self.expenses)

    # Установка обработчиков
    def set_expense_add_handler(self,
                                handler: Callable[[str, str, str], None]
                                ) -> None:
        self.exp_adder = self._try(self.main_window, handler)

    def set_expense_delete_handler(self,
                                   handler: Callable[[set[int]], None]
                                   ) -> None:
        self.exp_deleter = self._try(self.main_window, handler)

    def set_expense_modify_handler(self,
                                   handler: Callable[[int, str, str], None]
                                   ) -> None:
        self.exp_modifier = self._try(self.main_window, handler)

    # Вызовы обработчиков
    def add_expense(self, amount: str, cat_name: str, comment: str = "") -> None:
        self.exp_adder(amount, cat_name, comment)

    def delete_expenses(self, exp_pks: Iterable[int]) -> None:
        if len(list(exp_pks)) == 0:
            QtWidgets.QMessageBox.critical(
                self.main_window,
                'Ошибка',
                'Расходы для удаления не выделены'
            )
        else:
            reply = QtWidgets.QMessageBox.question(
                self.main_window,
                'Удаление расходов',
                'Вы уверены, что хотите удалить все выбранные расходы?')
            if reply == QtWidgets.QMessageBox.Yes:
                self.exp_deleter(exp_pks)

    def modify_expense(self, pk: int, attr: str, new_val: str) -> None:
        self.exp_modifier(pk, attr, new_val)

    ### Обработка бюджетов ###
    def create_budgets(self, budgets: list[Budget]) -> None:
        self.budgets = budgets
        self.budget_table.set_budget(self.budgets)

    def set_budget_modify_handler(self,
                                  handler: Callable[[int | None, str, str], None]
                                  ) -> None:
        """ Определение обработчика метода изменения бюджета """
        self.bdg_modifier = self._try(self.main_window, handler)

    def modify_budget(self, pk: int, new_limit: str, period: str) -> None:
        """ Вызывает функцию изменения бюджета """
        self.bdg_modifier(pk, new_limit, period)

    def budget_limit_exceeded_message(self) -> None:
        msg = "Достигнут лимит бюджета"
        QtWidgets.QMessageBox.warning(self.main_window, 'Лимит превышен!', msg)
