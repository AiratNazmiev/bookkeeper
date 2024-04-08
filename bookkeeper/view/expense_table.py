"""
Реализация виджетов, связанных с таблицей расходов
"""
# pylint: disable=no-name-in-module
# pylint: disable=c-extension-no-member
# pylint: disable=too-many-instance-attributes
# mypy: disable-error-code="attr-defined"
from PySide6 import QtWidgets

from typing import Callable, Iterable, Any

from bookkeeper.view.widgets import WidgetName
from bookkeeper.models.budget import Expense


class WidgetExpenseTable(QtWidgets.QTableWidget):
    """
    Виджет таблицы c расходами:
    столбцы: Бюждет Расходы Остаток
    строки: День, Неделя, Месяц
    """

    def __init__(self,
                 modify_handler: Callable[[int, str, str], None],
                 row_num: int = 60,
                 *args: Any, **kwargs: Any
                 ) -> None:
        super().__init__(*args, **kwargs)

        self.cell_data: list[list[Any]] = []

        self.modify_handler = modify_handler
        self.row_num = row_num

        self.setColumnCount(4)
        self.setRowCount(self.row_num)

        self._col2attr_list = [
            'expense_date', 'amount', 'category', 'comment'
        ]

        self.setHorizontalHeaderLabels(
            ['Дата', 'Сумма', 'Категория', 'Комментарий']
        )

        header = self.horizontalHeader()
        for i in range(4):
            if i == 3:
                mode = QtWidgets.QHeaderView.Stretch
            else:
                mode = QtWidgets.QHeaderView.Stretch
            header.setSectionResizeMode(i, mode)

        self.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.cellDoubleClicked.connect(self._dclick_cell)

    def _col2attr(self, col: int) -> str:
        return self._col2attr_list[col]

    # pylint: disable=duplicate-code
    # pylint: disable=unused-argument
    def _dclick_cell(self, row: int, col: int) -> None:
        """ Обработчик двойного нажатия на ячейку """
        self.cellChanged.connect(self._change_cell)

    def _change_cell(self, row: int, col: int) -> None:
        """ Изменение ячейки по двойному нажатию """
        self.cellChanged.disconnect(self._change_cell)
        # проверка, что изменение было в поле с существующим расходом
        try:
            self.cell_data[row][-1]
        except IndexError:
            pass
        else:
            pk = self.cell_data[row][-1]
            upd_value = self.item(row, col).text()
            self.modify_handler(pk, self._col2attr(col), upd_value)

    def add_data(self, cell_data: list[list[Any]]) -> None:
        """ Добавление и обновления данных таблицы """
        self.cell_data = cell_data
        for y, row in enumerate(cell_data):
            for x, text in enumerate(row[:-1]):
                self.setItem(
                    y, x, QtWidgets.QTableWidgetItem(text)
                )


class WidgetExpenseTableBox(QtWidgets.QGroupBox):
    """ Группа с таблицей расходов """

    def __init__(self,
                 pk2name: Callable[[int], str],
                 modify_handler: Callable[[int, str, str], None],
                 delete_handler: Callable[[Iterable[int]], None],
                 name: str = "<b>Расходы</b>",
                 *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.cell_data: list[list[Any]] = []
        self.expense_list: list[Expense] = []

        self.pk2name = pk2name
        self.delete_handler = delete_handler

        self.vbox = QtWidgets.QVBoxLayout()

        self.label = WidgetName(name)
        self.vbox.addWidget(self.label)

        self.table = WidgetExpenseTable(modify_handler)
        self.vbox.addWidget(self.table)

        self.dbtn = QtWidgets.QPushButton('Удалить выделенные расходы')
        self.dbtn.clicked.connect(self.delete_expense)

        self.vbox.addWidget(self.dbtn)
        self.setLayout(self.vbox)

    def _expense2data(self, expense_list: list[Expense]) -> list[list[Any]]:
        """ Перевод трат в текстовые данные для таблицы """
        cell_data = []
        for e in expense_list:
            new_data = [
                str(e.expense_date) if e.expense_date else "",
                str(e.amount) if e.amount else "",
                str(self.pk2name(e.category)) if e.category else "",
                str(e.comment) if e.comment else "",
                e.pk
            ]
            cell_data.append(new_data)
        return cell_data

    def set_expense(self, expense_list: list[Expense]) -> None:
        """ Выставления списка расходов """
        self.expense_list = expense_list
        self.cell_data = self._expense2data(self.expense_list)

        self.table.clearContents()
        self.table.add_data(self.cell_data)

    def delete_expense(self) -> None:
        """ Удаление расходов """
        delete_list = []
        range = self.table.selectedRanges()

        for r in range:
            first = r.topRow()
            last = min(r.bottomRow(), len(self.cell_data))
            delete_list.extend([i[-1] for i in self.cell_data[first: last+1]])

        self.delete_handler(set(delete_list))
