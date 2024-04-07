# pylint: disable = no-name-in-module
# pylint: disable=c-extension-no-member
# pylint: disable=too-many-instance-attributes
# mypy: disable-error-code="attr-defined"
from typing import Callable, Any
from PySide6 import QtWidgets

from bookkeeper.view.widgets import (
    WidgetName,
    WidgetLineInput,
    WidgetBoxInput,
)
from bookkeeper.models.category import Category


class WidgetAddExpenseBox(QtWidgets.QGroupBox):
    """ Виджет для добавления информации о расходах """
    def __init__(self, 
                 category_list: list[Category],
                 show_edit: Callable[[], None],
                 add_handler: Callable[[str, str, str], None],
                 name: str = 'Новая трата',
                 *args: Any, **kwargs: Any
                 ) -> None:
        super().__init__(*args, **kwargs)
        
        self.add_handler = add_handler
        self.grid = QtWidgets.QGridLayout()
        
        self.label = WidgetName(name)
        self.grid.addWidget(self.label, 0, 0, 1, 5)
        
        self.amount = WidgetLineInput('Сумма', '0')
        self.grid.addWidget(self.amount, 1, 0, 1, 4)
        
        self.category = WidgetBoxInput('Категория', [])
        self.grid.addWidget(self.category, 2, 0, 1, 4)
        
        self.ebtn = QtWidgets.QPushButton('Редактировать')
        self.ebtn.clicked.connect(show_edit)
        self.grid.addWidget(self.ebtn, 2, 4, 1, 1)
        
        self.comment = WidgetLineInput('Комментарий', '')
        self.grid.addWidget(self.comment, 3, 0, 1, 4)
        
        self.submit_button = QtWidgets.QPushButton('Добавить')
        self.submit_button.clicked.connect(self._add_expense)
        self.grid.addWidget(self.submit_button, 4, 0, 1, 5)
        
        self.setLayout(self.grid)
        self.set_categories(category_list)
        
    def _add_expense(self) -> None:
        """ Добавление расхода """
        self.add_handler(
            self.amount.text(),
            self.category.text(),
            self.comment.text()
        )
        self.amount.set_default()
        self.category.set_default()
        self.comment.set_default()

    def set_categories(self, category_list: list[Category]) -> None:
        """  список категорий """
        self.category.set_items([c.name for c in category_list])