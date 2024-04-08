from typing import Any

from PySide6 import QtWidgets
from PySide6.QtCore import QEvent   # pylint: disable=no-name-in-module

from bookkeeper.view.budget_table import WidgetBudgetTableBox
from bookkeeper.view.expense_table import WidgetExpenseTable
from bookkeeper.view.add_expense  import WidgetAddExpenseBox


# pylint: disable=too-few-public-methods
class Window(QtWidgets.QWidget):
    """ Основное окно приложения """
    MSG_TITLE_STR: str = "Закрыть приложение?"
    MSG_TEXT_STR: str = "Несохраненные данные будут удалены"
    def __init__(self,
                 budget_table: WidgetBudgetTableBox,
                 add_expense: WidgetAddExpenseBox,
                 expense_table: WidgetExpenseTable,
                 name: str = 'The Bookkeeper App',
                 *args: Any, **kwargs: Any
                ) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle(name)

        self.budget_table  = budget_table
        self.add_expense   = add_expense
        self.expense_table = expense_table
        
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.budget_table, stretch=3)
        self.vbox.addWidget(self.add_expense, stretch=1)
        self.vbox.addWidget(self.expense_table, stretch=6)
        self.setLayout(self.vbox)

    def closeEvent(self, event: QEvent) -> None:  # pylint: disable=invalid-name
        """ Диалоговое окно с закрытием приложения """
        reply = QtWidgets.QMessageBox.question(
            self, Window.MSG_TITLE_STR, Window.MSG_TEXT_STR
        )
        
        # Считывание ответа пользователя
        if reply == QtWidgets.QMessageBox.Yes:  # type: ignore
            event.accept()
            app = QtWidgets.QApplication.instance()
            app.closeAllWindows()  # type: ignore
        else:
            event.ignore()