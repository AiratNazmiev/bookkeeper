"""
Описан класс, реализующий модуль Presenter
"""
# mypy: disable-error-code="attr-defined"
from datetime import datetime
from typing import Callable, Iterable, Any

from bookkeeper.view.abstract_view import AbstractView
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense


class Presenter:
    """
    Класс Presenter в паттерне MVP.
    Использует класс представления, наследуемый от AbstractView и
    классы репозиториев, наследуемые от AbstractRepository
    Операции работают с данными в визуальном представлении и
    в репозиториях
    """
    view: AbstractView
    category_repository: AbstractRepository[Category]  # type: ignore
    budget_repository: AbstractRepository[Budget]  # type: ignore
    expense_repository: AbstractRepository[Expense]  # type: ignore

    def __init__(self,
                 view: AbstractView,
                 repository_factory: Callable[[Any], AbstractRepository[Any]]
                 ) -> None:

        self.view = view

        # Репозиторий категорий расходов
        self.category_repository = repository_factory(Category)
        self.categories = self.category_repository.get_all()

        self.view.create_categories(self.categories)
        self.view.set_category_add_handler(self.add_category)
        self.view.set_category_delete_handler(self.delete_category)
        self.view.set_category_name_check(self.cat_checker)

        # Репозиторий бюджетов
        self.budget_repository = repository_factory(Budget)
        self.budgets = self.budget_repository.get_all()
        self.view.set_budget_modify_handler(self.modify_budget)

        # Репозиторий расходов
        self.expense_repository = repository_factory(Expense)

        self.update_expenses()
        self.view.set_expense_add_handler(self.add_expense)
        self.view.set_expense_delete_handler(self.delete_expenses)
        self.view.set_expense_modify_handler(self.modify_expense)

    def show_window(self) -> None:
        """ Отображение окна приложения """
        self.view.main_window.show()

    # Методы категорий расходов
    def cat_checker(self, category_name: str) -> None:
        """ Проверка наличия категорий """
        if category_name not in [c.name for c in self.categories]:
            raise ValueError(f"Категории '{category_name}' не существует")

    def add_category(self, name: str, parent: str | None = None) -> None:
        """ Добавление категории расходов """
        # Категория уже есть
        if name in [c.name for c in self.categories]:
            raise ValueError(f"Категория '{name}' уже существует")

        # Нет данной родительской категории
        if parent is not None:
            if parent not in [c.name for c in self.categories]:
                raise ValueError(f"Категории '{parent}' не существует")
            parent_pk = self.category_repository.get_all(where={'name': parent})[0].pk
        else:
            parent_pk = None

        category = Category(name, parent_pk)
        self.categories.append(category)  # обновления данных
        self.category_repository.add(category)  # обновление репозитория
        self.view.create_categories(self.categories)  # обновление представленя

    def delete_category(self, category_name: str) -> None:
        """ Удаление категории """
        categories = self.category_repository.get_all(where={"name": category_name})
        if len(categories) == 0:
            raise ValueError(f"Категории '{category_name}' не существует")

        category = categories[0]
        self.category_repository.delete(category.pk)

        for child in self.category_repository.get_all(where={'parent': category.pk}):
            child.parent = category.parent
            self.category_repository.update(child)

        self.categories = self.category_repository.get_all()
        self.view.create_categories(self.categories)

        for exp in self.expense_repository.get_all(where={'category': category.pk}):
            self.expense_repository.delete(exp.pk)

        self.update_expenses()

    # Методы элементов расходов
    def update_expenses(self) -> None:
        """ Обновление элементов расходов """

        self.expenses = self.expense_repository.get_all()
        self.view.create_expenses(self.expenses)

        # необходимо также обновить данные бюджетов
        self.update_budgets()

    def add_expense(self, amount: str, category_name: str, comment: str = "") -> None:
        """ Добавление элементов расходов """
        try:
            amount_int = int(amount)
        except ValueError as ex:
            raise ValueError("Введите сумму покупки как целое число") from ex

        if amount_int <= 0:
            raise ValueError("Неверная сумма покупки:\nСумма должна быть положительной")

        categories = self.category_repository.get_all(
            where={"name": category_name.lower()}
        )

        if len(categories) == 0:
            raise ValueError(f"Категории '{category_name}' не существует")

        category = categories[0]
        new_exp = Expense(amount_int, category.pk, comment=comment)

        self.expense_repository.add(new_exp)
        self.update_expenses()

        for budget in self.budgets:
            if budget.spent > budget.lim:
                self.view.budget_limit_exceeded_message()

    def delete_expenses(self, exp_pks: Iterable[int]) -> None:
        """ Удаление элеменов расходов """
        for pk in exp_pks:
            self.expense_repository.delete(pk)
        self.update_expenses()

    def modify_expense(self, pk: int, attr: str, new_val: str) -> None:
        """ Обновление пунктов расходов: в базе данных и в интерфейсе """
        exp = self.expense_repository.get(pk)
        if exp is None:
            raise ValueError(f"Расхода с pk='{pk}' не существует")

        match attr:
            case "category":
                category_name = new_val.lower()
                if category_name not in [c.name for c in self.categories]:
                    raise ValueError(f"Категории '{category_name}' не существует")

                cat_pk = self.category_repository.get_all(
                    where={'name': category_name})[0].pk
                exp.category = cat_pk

            case "amount":
                try:
                    amount = int(new_val)
                except ValueError as ex:
                    raise ValueError("Сумма должна быть целым числом") from ex

                if amount <= 0:
                    raise ValueError("Неверная сумма покупки:\n"
                                     "Сумма должна быть положительной")
                exp.amount = amount

            case "expense_date":
                try:
                    time_str = datetime.fromisoformat(new_val)
                    time_date = time_str.isoformat(sep='\t', timespec='minutes')
                except ValueError as ex:
                    raise ValueError("Неверный формат даты:\n"
                                     "Требуется yyyy-mm-dd hh:mm") from ex
                exp.expense_date = time_date

            case 'comment':
                exp.comment = new_val

        self.expense_repository.update(exp)
        self.update_expenses()

    # Методы бюджетов
    def update_budgets(self) -> None:
        """ Обновление параметров бюджетов """
        for budget in self.budget_repository.get_all():
            budget.update(self.expense_repository)
            self.budget_repository.update(budget)

        self.budgets = self.budget_repository.get_all()
        self.view.create_budgets(self.budgets)

    def modify_budget(self, pk: int | None, new_limit: str, period: str) -> None:
        """ Обновление лимита и периода бюджета """
        if new_limit == "":
            if pk is not None:
                self.budget_repository.delete(pk)
            self.update_budgets()
            return

        try:
            new_limit_int = int(new_limit)
        except ValueError as ex:
            self.update_budgets()
            raise ValueError("Неверная сумма\nОтрицательное число") from ex

        if new_limit_int < 0:
            self.update_budgets()
            raise ValueError("Неверный период:\nОтрицательное число")

        if pk is None:
            budget_new = Budget(new_limit_int, period)
            self.budget_repository.add(budget_new)
        else:
            budget_old = self.budget_repository.get(pk)
            if budget_old is None:
                raise ValueError(f"Бюджета с pk='{pk}' не существует")

            budget_old.lim = new_limit_int
            self.budget_repository.update(budget_old)

        self.update_budgets()
