"""
Реализация базовых типов виджетов:
обертка для названия, строка для ввода данных
"""
# pylint: disable=no-name-in-module
# pylint: disable=c-extension-no-member
# pylint: disable=too-few-public-methods
# mypy: disable-error-code="attr-defined,assignment"
from PySide6.QtCore import Qt
from PySide6 import QtWidgets

from typing import Any


class WidgetName(QtWidgets.QLabel):
    """ Выставление названия виджета """

    def __init__(self, text: str,
                 *args: Any, **kwargs: Any
                 ) -> None:
        super().__init__(text, *args, **kwargs)
        self.setFrameStyle(QtWidgets.QFrame.Plain | QtWidgets.QFrame.Box)
        self.setAlignment(Qt.AlignCenter)


class WidgetLineInput(QtWidgets.QWidget):
    """ Поле для ввода с названием """

    def __init__(self, text: str, placeholder: str,
                 *args: Any, **kwargs: Any
                 ) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QHBoxLayout()

        self.label = QtWidgets.QLabel(text)
        self.layout.addWidget(self.label, stretch=1)

        self.input = QtWidgets.QLineEdit(placeholder)
        self.layout.addWidget(self.input, stretch=4)
        self.placeholder = placeholder

        self.setLayout(self.layout)  # type: ignore

    def text(self) -> str:
        """ Получение текста виджета """
        return self.input.text()

    def set_text(self, text: str) -> None:
        """ Устанавливает текст виджета """
        self.input.setText(text)

    def set_default(self) -> None:
        """ Устанавливает значение по умолчанию """
        self.input.setText(self.placeholder)


class WidgetBoxInput(QtWidgets.QWidget):
    """ Поле для ввода данных из списка """

    def __init__(self, text: str, items: list[str],
                 placeholder: str = "",
                 max_visible_items: int = 12,
                 *args: Any, **kwargs: Any
                 ) -> None:
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QHBoxLayout()

        self.label = QtWidgets.QLabel(text)
        self.layout.addWidget(self.label, stretch=1)

        self.box = QtWidgets.QComboBox()
        self.box.setEditable(True)
        self.box.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.box.setMaxVisibleItems(max_visible_items)
        self.placeholder = placeholder

        self.set_items(items)
        self.layout.addWidget(self.box, stretch=4)

        self.setLayout(self.layout)  # type: ignore

    def text(self) -> str:
        """ Получение текста виджета """
        return self.box.currentText()

    def set_text(self, text: str) -> None:
        """ Устанавливает текст виджета """
        self.box.setCurrentText(text)

    def set_default(self) -> None:
        """ Устанавливает значение текста по умолчанию """
        self.box.setCurrentText(self.box.placeholderText())

    def set_items(self, items: list[str]) -> None:
        """ Устанавливает элементы выпадающего списка """
        self.items = items
        self.box.clear()
        self.box.addItems(items)

        if len(items) > 0:
            self.box.setPlaceholderText(items[0])
        else:
            self.box.setPlaceholderText(self.placeholder)

        self.set_default()
