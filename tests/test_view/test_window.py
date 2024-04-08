from pytestqt.qt_compat import qt_api

from bookkeeper.view.window import Window
from bookkeeper.view.add_expense import WidgetAddExpenseBox
from bookkeeper.view.budget_table import WidgetBudgetTableBox
from bookkeeper.view.expense_table import WidgetExpenseTableBox


modify_handler = lambda pk, arg1, arg2: None
pk2name = lambda pk: ""
delete_handler = lambda pks: None
show_edit = lambda: None
add_handler = lambda amount, name, comment: None


def test_create_window(qtbot):
    budget_table = WidgetBudgetTableBox(modify_handler)
    add_expense = WidgetAddExpenseBox([], show_edit, add_handler)
    expense_table = WidgetExpenseTableBox(pk2name, modify_handler, delete_handler)
    window = Window(budget_table, add_expense, expense_table)
    qtbot.addWidget(window)

    assert window.budget_table  == budget_table
    assert window.add_expense   == add_expense
    assert window.expense_table == expense_table


def test_close_yes(qtbot, monkeypatch):
    budget_table = WidgetBudgetTableBox(modify_handler)
    new_expense = WidgetAddExpenseBox([], show_edit, add_handler)
    expense_table = WidgetExpenseTableBox(pk2name, modify_handler, delete_handler)

    window = Window(budget_table, new_expense, expense_table)
    qtbot.addWidget(window)

    monkeypatch.setattr(
        qt_api.QtWidgets.QMessageBox, 
        "question",
        lambda *args: qt_api.QtWidgets.QMessageBox.Yes
    )
    
    assert window.close() == True

    
def test_close_no(qtbot, monkeypatch):
    budget_table = WidgetBudgetTableBox(modify_handler)
    new_expense = WidgetAddExpenseBox([], show_edit, add_handler)
    expense_table = WidgetExpenseTableBox(pk2name, modify_handler, delete_handler)

    window = Window(budget_table, new_expense, expense_table)
    qtbot.addWidget(window)

    monkeypatch.setattr(
        qt_api.QtWidgets.QMessageBox, 
        "question",
        lambda *args: qt_api.QtWidgets.QMessageBox.No
    )
    
    assert window.close() == False