from typing import Callable, Any

from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from bookkeeper.models.category import Category
from bookkeeper.view.widgets import WidgetBoxInput, WidgetLineInput, WidgetName


class WidgetEditCategory(QtWidgets.QWidget):
    """ Окно для добавления/редактирования/удаления категорий """
    
    NO_PARENT_CAT_STR: str = "Нет родительской категории"
    cat_checker : Callable[[str], None]

    def __init__(self,
                 category_list: list[Category],
                 add_handler: Callable[[str, str | None], None],
                 delete_handler : Callable[[str], None],
                 *args: Any, **kwargs: Any
                 ) -> None:
        super().__init__(*args, **kwargs)

        self.add_handler    = add_handler
        self.delete_handler = delete_handler

        # Дерево категорий
        label_cats = WidgetName("<b>Список категорий</b>") # type: ignore
        
        self.category_tree = QtWidgets.QTreeWidget()
        self.category_tree.setHeaderLabel("")
        self.category_tree.itemDoubleClicked.connect(self._dclick)  # type: ignore

        # Удаление категории
        label_del = WidgetName("<b>Удаление категории</b>")

        # Категория, которую нужно удалить
        self.category_delete = WidgetBoxInput("Категория", [])

        # Кнопка удаления
        self.dbtn = QtWidgets.QPushButton('Удалить')
        self.dbtn.clicked.connect(self._delete)  # type: ignore
        
        # Добавление категории
        add_label = WidgetName("<b>Добавление категории</b>") # type: ignore
        self.add_parent = WidgetBoxInput("Родитель", [])
        self.add_name = WidgetLineInput("Название", "Новая категория")

        # Кнопка добавления
        self.abtn = QtWidgets.QPushButton('Добавить')
        self.abtn.clicked.connect(self.add)  # type: ignore

        # Размещение элементов
        self.grid = QtWidgets.QGridLayout()

        #                                        y  x dy dx
        self.grid.addWidget(label_cats,          0, 0, 1, 2)
        self.grid.addWidget(self.category_tree,  1, 0, 1, 2)
        self.grid.addWidget(label_del,           2, 0, 1, 2)
        self.grid.addWidget(self.category_delete,3, 0, 1, 1)
        self.grid.addWidget(self.dbtn,           3, 1, 1, 1)
        self.grid.addWidget(add_label,           4, 0, 1, 2)
        self.grid.addWidget(self.add_parent,     5, 0, 1, 1)
        self.grid.addWidget(self.add_name,       6, 0, 1, 1)
        self.grid.addWidget(self.abtn,           6, 1, 1, 1)
        self.setLayout(self.grid)

        self.set_categories(category_list)

    def set_categories(self, category_list: list[Category]) -> None:
        self.categories = category_list
        category_names = [c.name for c in category_list]

        category_hierarchy = self.find_children()

        self.category_tree.clear()
        self.category_tree.insertTopLevelItems(0, category_hierarchy)

        self.category_delete.set_items(category_names)
        self.add_parent.set_items(
            [WidgetEditCategory.NO_PARENT_CAT_STR] + category_names
        )

    def _delete(self) -> None:
        self.delete_handler(self.category_delete.text())
        self.category_delete.set_default()

    def set_checker(self, checker : Callable[[str], None]) -> None:
        self.cat_checker = checker

    def add(self) -> None:
        add_name = self.add_name.text()
        parent_cat_name = self.add_parent.text()

        if parent_cat_name == WidgetEditCategory.NO_PARENT_CAT_STR:
            self.add_handler(add_name, None)
        else:
            # pylint: disable=todo
            # TODO: Нужна реализация проверок на циклические зависимости
            self.cat_checker(parent_cat_name)
            self.add_handler(add_name, parent_cat_name)

        self.add_name.set_default()
        self.add_parent.set_default()

    def find_children(self,
                      parent_pk: int | None = None
                     ) -> list[QtWidgets.QTreeWidgetItem]:
        """ Обход списка категорий с нахождением подкатегорий """
        items = []
        children = [c for c in self.categories if c.parent == parent_pk]
        for child in children:
            item = QtWidgets.QTreeWidgetItem([child.name])
            # pylint: disable=fixme
            # FIXME: Нужна реализация проверок на циклические зависимости
            item.addChildren(self.find_children(parent_pk=child.pk))
            items.append(item)
        return items

    def _dclick(self, item: QtWidgets.QTreeWidgetItem, column: int) -> None:
        clicked_cat_name = item.text(column)

        self.category_delete.set_text(clicked_cat_name)
        self.add_parent.set_text(clicked_cat_name)