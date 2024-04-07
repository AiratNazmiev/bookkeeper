from pytestqt.qt_compat import qt_api

from bookkeeper.view.add_expense import WidgetAddExpenseBox
from bookkeeper.models.category import Category


def show_edit(): return None
def add_handler(amount, cat_name, comment): return None


def test_create_group(qtbot):
    widget = WidgetAddExpenseBox([], show_edit, add_handler)
    qtbot.addWidget(widget)
    assert widget.add_handler == add_handler


def test_set_categories(qtbot):
    widget = WidgetAddExpenseBox([], show_edit, add_handler)
    qtbot.addWidget(widget)
    category_list = [Category("1"), Category("2"), Category("3")]
    widget.set_categories(category_list)
    
    for i in range(3):
        assert widget.category.box.itemText(i) == category_list[i].name


def test_add_expense(qtbot):
    def add_handler(amount, cat_name, comment):
        add_handler.was_called = True
        assert amount == "123"
        assert cat_name == "1"
        assert comment == "no"
    add_handler.was_called = False
    
    category_list = [Category("1"), Category("2"), Category("3")]
    widget = WidgetAddExpenseBox(
        category_list,
        show_edit,
        add_handler
    )
    qtbot.addWidget(widget)
    
    widget.amount.set_text("123")
    widget.category.set_text("1")
    widget.comment.set_text("no")
    
    qtbot.mouseClick(
        widget.submit_button,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )
    assert add_handler.was_called is True