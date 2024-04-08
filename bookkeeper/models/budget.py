from dataclasses import dataclass
from datetime import datetime, timedelta

from ..repository.abstract_repository import AbstractRepository
from ..models.expense import Expense


@dataclass(init=False)
class Budget:
    """
    Бюджет, установленный на данный период
    lim - размер бюджета;
    period - выделенный период
    spent - сколько было потрачено за выбранный период;
    pk - первичный ключ
    """
    lim: int
    period: str
    spent: int
    pk: int

    def __init__(self, lim: int, period: str, spent: int = 0, pk: int = 0) -> None:
        if period not in ['day', 'week', 'month']:
            raise ValueError('Invalid period, only day, '
                             'week and month are available')
        self.lim = lim
        self.period = period
        self.spent = spent
        self.pk = pk

    def _get_day_expense(self, curr_date_str: str,
                         expense_repository: AbstractRepository[Expense]
                         ) -> list[Expense]:
        mask = curr_date_str
        return expense_repository.get_all_substr(where={'expense_date': mask})

    def _get_week_expense(self, curr_date_str: str,
                          expense_repository: AbstractRepository[Expense]
                          ) -> list[Expense]:
        curr_date = datetime.fromisoformat(curr_date_str)
        curr_week_day = datetime.now().weekday()
        curr_week_start = curr_date - timedelta(days=curr_week_day)

        expense_list = []

        for d in range(curr_week_day + 1):
            mask = (curr_week_start + timedelta(days=d)).date().isoformat()
            expense_list.extend(
                expense_repository.get_all_substr(where={'expense_date': mask})
            )
        return expense_list

    def _get_month_expense(self, curr_date_str: str,
                           expense_repository: AbstractRepository[Expense]
                           ) -> list[Expense]:
        mask = curr_date_str[:7]  # yyyy-mm
        return expense_repository.get_all_substr(where={'expense_date': mask})

    def update(self, expense_repository: AbstractRepository[Expense]) -> None:
        """
        Обновление расходов за выбранный период на основе данных из репозитория 
        """
        curr_date_str = datetime.now().date().isoformat()  # yyyy-mm-dd

        match self.period:
            case 'day':
                expense_list = self._get_day_expense(curr_date_str,
                                                     expense_repository)
            case 'week':
                expense_list = self._get_week_expense(curr_date_str,
                                                      expense_repository)
            case 'month':
                expense_list = self._get_month_expense(curr_date_str,
                                                       expense_repository)

        self.spent = sum([int(e.amount) for e in expense_list])
