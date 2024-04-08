"""
TODO
"""

from pytestqt.qt_compat import qt_api

from bookkeeper.view.expense_table import WidgetExpenseTable, WidgetExpenseTableBox
from bookkeeper.models.expense import Expense

test_cell_data = [
    ["A", "B", "C", "D", 42],
    ["E", "F", "G", "H", 24],
]


def modify_handler(pk, attr, new_val): return None
def pk2name(pk): return "C"
def delete_handler(exp_pks): return None


def test_create_widget(qtbot):
    widget = WidgetExpenseTable(modify_handler)
    qtbot.addWidget(widget)
    assert widget.modify_handler == modify_handler


def test_add_data(qtbot):
    widget = WidgetExpenseTable(modify_handler)
    qtbot.addWidget(widget)
    widget.add_data(test_cell_data)
    assert widget.cell_data == test_cell_data
    for i, row in enumerate(test_cell_data):
        for j, _ in enumerate(row[:-1]):
            assert widget.item(i, j).text() == test_cell_data[i][j]


def test_cell_changed(qtbot):
    def modify_handler(pk, attr, new_val):
        modify_handler.was_called = True
        assert pk == test_cell_data[0][4]
        assert new_val == test_cell_data[0][0]
    modify_handler.was_called = False
    widget = WidgetExpenseTable(modify_handler)
    qtbot.addWidget(widget)
    widget.add_data(test_cell_data)
    widget.cellChanged.emit(0, 0)
    assert modify_handler.was_called is False
    widget.cellDoubleClicked.emit(0, 0)
    widget.cellChanged.emit(0, 0)
    assert modify_handler.was_called is True


def test_create_group(qtbot):
    widget = WidgetExpenseTableBox(
        pk2name,
        modify_handler,
        delete_handler
    )
    qtbot.addWidget(widget)
    assert widget.pk2name == pk2name
    assert widget.delete_handler == delete_handler


def test_set_expenses(qtbot):
    widget = WidgetExpenseTableBox(
        pk2name,
        modify_handler,
        delete_handler
    )
    qtbot.addWidget(widget)
    exps = [Expense(111, 2, expense_date="1984-01-02 22:22", comment="tmp"),
            Expense(222, 1, expense_date="1984-02-01 11:11")]

    widget.set_expense(exps)
    assert widget.expense_list == exps

    for e, w_data in zip(exps, widget.cell_data):
        assert str(e.expense_date) == w_data[0]
        assert str(e.amount) == w_data[1]
        assert pk2name(e.category) == w_data[2]
        assert str(e.comment) == w_data[3]
        assert e.pk == w_data[4]


def test_delete_expenses(qtbot):
    def delete_handler(exp_pks):
        delete_handler.was_called = True
        assert exp_pks == set([2, 3])
    delete_handler.was_called = False
    widget = WidgetExpenseTableBox(pk2name,
                                   modify_handler,
                                   delete_handler)
    qtbot.addWidget(widget)
    exps = [
        Expense(100, 1, pk=1), Expense(200, 2, pk=2),
        Expense(300, 3, pk=3), Expense(400, 4, pk=4)
    ]
    widget.set_expense(exps)
    widget.table.setRangeSelected(
        qt_api.QtWidgets.QTableWidgetSelectionRange(1, 1, 2, 2), True)
    widget.table.setRangeSelected(
        qt_api.QtWidgets.QTableWidgetSelectionRange(1, 3, 3, 4), True)
    qtbot.mouseClick(
        widget.dbtn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )
    assert delete_handler.was_called is True
