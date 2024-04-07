import pytest
from datetime import datetime, timedelta

from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.repository.memory_repository import MemoryRepository


@pytest.fixture
def repo():
    return MemoryRepository()


def test_create_object():
    obj = Budget(24, 'week', 7)
    assert obj.limit == 24
    assert obj.period == 'week'
    assert obj.spent == 7
        
def test_create_brief():
    obj = Budget(42, 'day')
    assert obj.limit == 42
    assert obj.period == 'day'
    assert obj.spent == 0
    
def test_exception_period():
    with pytest.raises(ValueError):
        obj = Budget(limit=123, period='eternity')
    
def test_can_add_to_repo(repo):
    obj = Budget(555, 'month')
    pk = repo.add(obj)
    assert obj.pk == pk
    
def test_update_day(repo):
    obj = Budget(42, 'day')
    for _ in range(10):
        repo.add(Expense(5, 1))
    obj.update(repo)
    assert obj.spent == 50

def test_update_spent_week(repo):
    obj = Budget(11, 'week')
    date = datetime.now().date()
    week_day = datetime.now().weekday()
    week_start = date - timedelta(days=week_day)
    repo.add(Expense(5, 1, week_start.isoformat()))
    repo.add(Expense(7, 1, date.isoformat()))

    obj.update(repo)
    assert obj.spent == 12
    
def test_update_month(repo):
    obj = Budget(42, 'month')
    date = datetime.now()
    
    for i in range(1, 11):
        expense_day = date.day-i if date.day-i > 0 else date.day
        expense_date = datetime(date.year, date.month, expense_day)
        repo.add(Expense(10 * i, 1, expense_date=expense_date.date().isoformat()))
    
    expense_date_out_1 = (expense_date - timedelta(days=50)).date().isoformat()
    repo.add(Expense(42, 1, expense_date=expense_date_out_1))
    expense_date_out_2 = (expense_date + timedelta(days=50)).date().isoformat()
    repo.add(Expense(10, 1, expense_date=expense_date_out_2))
    
    obj.update(repo)
    assert obj.spent == 550