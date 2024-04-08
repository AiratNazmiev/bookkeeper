"""
TODO
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from typing import Callable, Any

from bookkeeper.view.widgets import WidgetName
from bookkeeper.models.budget import Budget


class WidgetBudgetTable(QtWidgets.QTableWidget):
    """ 
    Виджет таблицы с бюджетами на расходы:
    столбцы: Бюждет Траты Остаток
    строки: День, Неделя, Месяц
    """
    def __init__(self,
                 modify_handler: Callable[[int, int, int], None],
                 *args: Any, **kwargs: Any
                 ) -> None:    
        super().__init__(*args, **kwargs)
        
        self.cell_data: list[list[Any]] = []
        
        self.modify_handler = modify_handler
        
        self.setColumnCount(3)
        self.setRowCount(3)
        
        self._row2period_list = [
            'day', 'week', 'month'
        ]
        
        self.setHorizontalHeaderLabels(
            ['Бюджет', 'Траты', 'Остаток']
        )
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        self.setVerticalHeaderLabels(
            ['День', 'Неделя', 'Месяц']
        )
        self.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        self.cellDoubleClicked.connect(self._dclick_cell)
        
    def _row2period(self, row: int) -> str:
        return self._row2period_list[row]
    
    # pylint: disable=duplicate-code
    # pylint: disable=unused-argument
    def _dclick_cell(self, row: int, col: int) -> None:
        """ Обработчик двойного нажатия на ячейку """
        self.cellChanged.connect(self._change_cell)
        
    def _change_cell(self, row: int, col: int) -> None:
        """ Изменение ячейки по двойному нажатию """
        self.cellChanged.disconnect(self._change_cell)
        pk = self.cell_data[row][-1]
        upd_limit = self.item(row, col).text()
        self.modify_handler(pk, upd_limit, self._row2period(row))
        
    def add(self, cell_data: list[list[Any]]) -> None:
        """ Добавление и обновления данных таблицы """
        self.cell_data = cell_data
        for y, row in enumerate(self.cell_data):
            for x, text in enumerate(row[:-1]):
                self.setItem(
                    y, x, QtWidgets.QTableWidgetItem(text.capitalize())
                )
                self.item(y, x).setTextAlignment(Qt.AlignCenter)
                if x == 0:
                    self.item(y, x).setFlags(
                        Qt.ItemIsEditable| Qt.ItemIsEnabled | Qt.ItemIsSelectable
                    )
                else:
                    self.item(y, x).setFlags(Qt.ItemIsEnabled)
        
    
class WidgetBudgetTableBox(QtWidgets.QGroupBox):
    """ Группа бюджетов с таблицей и заголовком"""

    def __init__(self,
                 modify_handler: Callable[[int, str, str], None],
                 name: str = "Бюджет",
                 *args: Any, **kwargs: Any
                 ) -> None:
        super().__init__(*args, **kwargs)
        
        self.cell_data: list[list[Any]] = []
        self.budget_list: list[Budget] = []
    
        self.box = QtWidgets.QVBoxLayout()
        self.box.addWidget(WidgetName(name))
        
        self.table = WidgetBudgetTable(modify_handler)
        self.box.addWidget(self.table)
        
        self.setLayout(self.box)
        
    def _budget2data(self, budget_list: list[Budget]) -> list[list[Any]]:
        """ Перевод бюджетов в текстовые данные для таблицы """
        cell_data = []
        for p in self.table._row2period_list:
            curr_budget_list = [b for b in budget_list if b.period == p]
            if len(curr_budget_list) == 0:
                cell_data.append(["-", "", "", None])
            else:
                budget = curr_budget_list[0]
                new_data = ([str(budget.lim),
                        str(budget.spent),
                        str(int(budget.lim) - int(budget.spent)),
                        budget.pk])
                cell_data.append(new_data)  # type: ignore
        return cell_data       

    def set_budget(self, budget_list: list[Budget]) -> None:
        """ Выставление бюджета """
        self.budget_list = budget_list
        self.cell_data = self._budget2data(self.budget_list)
        
        self.table.clearContents()
        self.table.add(self.cell_data)