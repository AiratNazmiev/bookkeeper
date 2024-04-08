"""
Тесты GUI для модуля с таблицей бюджетов
"""

from pytestqt.qt_compat import qt_api

from bookkeeper.view.budget_table import WidgetBudgetTable, WidgetBudgetTableBox
from bookkeeper.models.budget import Budget

test_cell_data = [
    ["A", "B", "C", 42],
    ["D", "E", "F", 24],
]


def modify_handler(pk, new_limit, period):
    modify_handler.was_called = True
    assert pk == test_cell_data[1][-1]
    assert new_limit == test_cell_data[1][0]
    assert period == "week"


def test_create_widget(qtbot):
    widget = WidgetBudgetTable(modify_handler)
    qtbot.addWidget(widget)
    assert widget.modify_handler == modify_handler


def test_add_data(qtbot):
    widget = WidgetBudgetTable(modify_handler)
    qtbot.addWidget(widget)

    widget.add(test_cell_data)
    assert widget.cell_data == test_cell_data

    for i, row in enumerate(test_cell_data):
        for j, _ in enumerate(row[:-1]):
            assert widget.item(i, j).text() == test_cell_data[i][j]
            if j == 0:
                flags = (qt_api.QtCore.Qt.ItemIsEditable
                         | qt_api.QtCore.Qt.ItemIsEnabled
                         | qt_api.QtCore.Qt.ItemIsSelectable)
                assert widget.item(i, j).flags() == flags
            else:
                assert widget.item(i, j).flags() == qt_api.QtCore.Qt.ItemIsEnabled


def test_cell_changed(qtbot):
    def modify_handler(pk, new_limit, period):
        modify_handler.was_called = True
        assert pk == test_cell_data[1][-1]
        assert new_limit == test_cell_data[1][0]
        assert period == "week"

    modify_handler.was_called = False

    widget = WidgetBudgetTable(modify_handler)
    qtbot.addWidget(widget)
    widget.add(test_cell_data)

    # Нажатия не было
    widget.cellChanged.emit(1, 0)
    assert modify_handler.was_called is False

    # Было нажатие
    widget.cellDoubleClicked.emit(1, 0)
    widget.cellChanged.emit(1, 0)
    assert modify_handler.was_called is True


def test_create_group(qtbot):
    widget = WidgetBudgetTableBox(modify_handler)
    qtbot.addWidget(widget)


def test_set_budgets(qtbot):
    widget = WidgetBudgetTableBox(modify_handler)
    qtbot.addWidget(widget)
    budget_list = [Budget(111, "day", spent=42), Budget(777, "week")]
    widget.set_budget(budget_list)
    assert widget.budget_list == budget_list
    for b, w_data in zip(budget_list, widget.cell_data):
        assert str(b.lim) == w_data[0]
        assert str(b.spent) == w_data[1]
        assert str(int(b.lim) - int(b.spent)) == w_data[2]
        assert b.pk == w_data[3]
    assert widget.cell_data[2] == ["-", "", "", None]
