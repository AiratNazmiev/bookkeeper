"""
Реализация главного окна приложения
"""
# pylint: disable=no-name-in-module
# pylint: disable=c-extension-no-member
# mypy: disable-error-code="attr-defined,union-attr"
from typing import Any

from PySide6 import QtWidgets
from PySide6.QtCore import QEvent

from bookkeeper.view.budget_table import WidgetBudgetTableBox
from bookkeeper.view.expense_table import WidgetExpenseTableBox
from bookkeeper.view.add_expense import WidgetAddExpenseBox


# pylint: disable=too-few-public-methods
class Window(QtWidgets.QWidget):
    """ Основное окно приложения """
    MSG_TITLE_STR: str = " "
    MSG_TEXT_STR: str = "Закрыть приложение?"

    def __init__(self,
                 budget_table: WidgetBudgetTableBox,
                 add_expense: WidgetAddExpenseBox,
                 expense_table: WidgetExpenseTableBox,
                 name: str = 'The Bookkeeper App',
                 *args: Any, **kwargs: Any
                 ) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle(name)

        self.budget_table = budget_table
        self.add_expense = add_expense
        self.expense_table = expense_table

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.expense_table, stretch=6)
        self.vbox.addWidget(self.add_expense,   stretch=2)
        self.vbox.addWidget(self.budget_table,  stretch=3)
        self.setLayout(self.vbox)

    # pylint: disable=invalid-name
    def closeEvent(self, event: QEvent) -> None:
        """ Диалоговое окно с закрытием приложения """
        msg_box = QtWidgets.QMessageBox
        answer = msg_box.question(
            self, Window.MSG_TITLE_STR, Window.MSG_TEXT_STR
        )

        # Считывание ответа пользователя
        if answer == QtWidgets.QMessageBox.Yes:  # type: ignore
            event.accept()
            app = QtWidgets.QApplication.instance()
            app.closeAllWindows()  # type: ignore
        else:
            event.ignore()
