from PySide6.QtCore import Signal, QObject, QTimer
from PySide6.QtWidgets import QMessageBox
import Page

from icecream import ic


class PageManager(QObject):
    page_changed = Signal(str)

    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.current_page = None

        self.page_classes = {
            "home": Page.HomePage,
            "account": Page.AccountPage,
            "registration": Page.RegistrationPage,
            "main": Page.MainPage,
            "download": Page.DownloadPage,
            "login": Page.LoginPage,
            "launcher_settings": Page.LauncherSettings,
            "game_settings": Page.GameSettings,
        }

        ic(f"{self.current_page} in PageManager init")

    def show_page(self, page_name):
        ic(f"show_page called: {page_name}")

        if page_name not in self.page_classes:
            ic(f"Error: Page '{page_name}' does not exist.")
            self.show_error_message(f"Page '{page_name}' does not exist.")
            return

        if self.current_page and isinstance(
            self.current_page, self.page_classes[page_name]
        ):
            ic(f"Page '{page_name}' is already shown. No changes needed.")
            return

        ic(
            f"Current page before change: {self.current_page.__class__.__name__ if self.current_page else 'None'}"
        )

        try:
            new_page = self.page_classes[page_name](self.stacked_widget)

            if self.current_page:
                self.stacked_widget.removeWidget(self.current_page)
                self.current_page.deleteLater()
                ic(f"Deleted previous page: {self.current_page.__class__.__name__}")

            self.current_page = new_page

            self.stacked_widget.addWidget(self.current_page)
            self.stacked_widget.setCurrentWidget(self.current_page)
            ic(f"Page '{page_name}' initialized and shown.")

            QTimer.singleShot(10, lambda: self.page_changed.emit(page_name))

        except Exception as e:
            import traceback

            tb = traceback.extract_tb(e.__traceback__)
            filename, line, func, text = tb[
                -1
            ]  # Get the last traceback entry (most relevant)

            ic(f"Error loading page '{page_name}': {e} (Line {line} in {filename})")
            self.show_error_message(
                f"Failed to load '{page_name}'.\nError: {e}\nLine: {line} in {filename}"
            )

    def show_error_message(self, message):
        """Displays an error message in a popup window."""
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Error")
        error_dialog.setText(message)
        error_dialog.exec()
