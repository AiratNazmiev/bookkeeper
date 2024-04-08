"""
Запуск проекта:
poetry run python bookkeeper
"""

import sys
from PySide6.QtWidgets import QApplication  # pylint: disable=no-name-in-module

from bookkeeper.presenter.presenter import Presenter as App  # alias for Presenter
from bookkeeper.view.view import View
from bookkeeper.repository.repository_factory import repository_factory

# DB_FILE = None
DB_FILE = 'db/bookkeeper.db'

if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    view = View()

    bookkeeper = App(
        view=view,
        repository_factory=repository_factory(DB_FILE)
    )
    bookkeeper.show_window()

    sys.exit(qapp.exec())
