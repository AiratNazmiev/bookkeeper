"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода (yyyy-mm-dd\\t03:01)
    added_date - дата добавления в бд (yyyy-mm-dd\\t03:01)
    comment - комментарий
    pk - id записи в базе данных
    """
    amount: int
    category: int
    expense_date: str = datetime.now().isoformat(sep='\t', timespec='minutes')
    added_date: str = datetime.now().isoformat(sep='\t', timespec='minutes')
    comment: str = ''
    pk: int = 0
    
# TODO: можно добавить валидацию данных (например, нельзя создать расход с отрицательной суммой)
# можно через @property
