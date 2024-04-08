from pytestqt.qt_compat import qt_api

from bookkeeper.view.edit_category import WidgetEditCategory

from bookkeeper.models.category import Category


def add_handler(name, parent): return None
def delete_handler(cat_name): return None
def checker(parent_name): return None


def test_create_window(qtbot):
    widget = WidgetEditCategory([], add_handler, delete_handler)
    qtbot.addWidget(widget)

    assert widget.add_handler == add_handler
    assert widget.delete_handler == delete_handler


def test_set_categories(qtbot):

    widget = WidgetEditCategory([], add_handler, delete_handler)
    qtbot.addWidget(widget)

    cats = [
        Category("A",   pk=1),
        Category("B",   pk=2),
        Category("AA",  pk=42,  parent=1),
        Category("AB",  pk=13,  parent=1),
        Category("ABA", pk=451, parent=13)
    ]

    widget.set_categories(cats)

    assert widget.categories == cats
    assert widget.add_parent.items[1:] == [c.name for c in cats]

    # Проверка структуры дерева
    assert widget.category_tree.topLevelItem(0).text(0) == "A"
    assert widget.category_tree.topLevelItem(1).text(0) == "B"
    assert widget.category_tree.topLevelItem(0).child(0).text(0) == "AA"
    assert widget.category_tree.topLevelItem(0).child(1).text(0) == "AB"
    assert widget.category_tree.topLevelItem(0).child(1).child(0).text(0) == "ABA"


def test_set_cat_checker(qtbot):
    widget = WidgetEditCategory([], add_handler, delete_handler)
    qtbot.addWidget(widget)

    widget.set_checker(checker)

    assert widget.cat_checker == checker


def test_double_clicked(qtbot):
    widget = WidgetEditCategory([Category("A", pk=1)], add_handler, delete_handler)
    qtbot.addWidget(widget)

    item = widget.category_tree.topLevelItem(0)
    widget.category_tree.itemDoubleClicked.emit(item, 0)
    clicked_cat_name = item.text(0)

    assert widget.category_delete.text() == clicked_cat_name
    assert widget.add_parent.text() == clicked_cat_name


def test_delete_category(qtbot):
    # Define category deletion handler:
    def delete_handler(cat_name):
        delete_handler.was_called = True

        assert cat_name == "A"

    delete_handler.was_called = False

    widget = WidgetEditCategory([Category("A", pk=1)], add_handler, delete_handler)
    qtbot.addWidget(widget)

    widget.category_delete.set_text("A")
    qtbot.mouseClick(
        widget.dbtn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )

    assert delete_handler.was_called is True


def test_add_category(qtbot):
    def add_handler(name, parent):
        add_handler.was_called = True

        assert name == "AB"
        assert parent == "A"

    add_handler.was_called = False

    widget = WidgetEditCategory([Category("A", pk=1)], add_handler, delete_handler)
    qtbot.addWidget(widget)
    widget.set_checker(checker)

    widget.add_name.set_text("AB")
    widget.add_parent.set_text("A")
    qtbot.mouseClick(
        widget.abtn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )

    assert add_handler.was_called is True


def test_add_category_no_parent(qtbot):
    def add_handler(name, parent):
        add_handler.was_called = True

        assert name == "A"
        assert parent is None

    add_handler.was_called = False

    widget = WidgetEditCategory([], add_handler, delete_handler)
    qtbot.addWidget(widget)

    widget.set_checker(checker)

    widget.add_name.set_text("A")
    widget.add_parent.set_text(WidgetEditCategory.NO_PARENT_CAT_STR)
    qtbot.mouseClick(
        widget.abtn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )

    add_name_text = widget.add_name.text()
    widget.add_name.set_default()
    assert add_name_text == widget.add_name.text()

    add_parent_text = widget.add_parent.text()
    widget.add_parent.set_default()
    assert add_parent_text == widget.add_parent.text()

    assert add_handler.was_called is True
