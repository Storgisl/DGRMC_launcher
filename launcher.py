import sys

from PySide6.QtWidgets import QMainWindow, QApplication, QStackedWidget
from PySide6.QtCore import Qt
from icecream import ic

from Factory import LoggerFactory
from Utils import PageManager, PageStatusChecker
from UI import LauncherUI


class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_logger = LoggerFactory("Launcher").get_logger()
        self.mouse_logger = LoggerFactory(
            name="Mouse events", log_file="MouseEvents.log"
        ).get_logger()

        self.stacked_widget = QStackedWidget()
        self.ui = LauncherUI(self, self.stacked_widget)
        self.status_checker = PageStatusChecker()
        self.download_status = self.status_checker.download_status()
        self.user_status = self.status_checker.user_status(
            self.status_checker.current_username_var
        )
        self.page = PageManager(self.stacked_widget)
        self.check_status()
        self.signals_setup()
        self.show()
        self.main_logger.info("Launcher initialized")

    def signals_setup(self):
        """Connect the page change signal to handle_page_signals."""
        self.page.page_changed.connect(self.handle_page_signals)
        self.main_logger.info("Connected page_changed signal to handle_page_signals.")

    def handle_page_signals(self, page_name):
        self.main_logger.debug(f"handle_page_signals fired with: {page_name}")
        self.main_logger.debug(f"Current page: {self.page.current_page}")
        if self.page.current_page is None:
            ic("ERROR: current_page is None! show_page() might be broken.")
            return
        match page_name:
            case "home":
                self.main_logger.info("Switched to Home page")
                home = self.page.current_page
                home.go_to_account.connect(lambda: self.page.show_page("account"))

            case "account":
                account = self.page.current_page
                account.go_to_reg.connect(lambda: self.page.show_page("registration"))
                account.go_to_main_page.connect(lambda: self.page.show_page("main"))
                account.go_to_download_page.connect(
                    lambda: self.page.show_page("download")
                )
                self.main_logger.info("Switched to Account page")

            case "registration":
                self.main_logger.info("Switched to Registration page")
                registration = self.page.current_page
                registration.go_to_login.connect(lambda: self.page.show_page("login"))
                registration.registration_complete.connect(
                    lambda: self.page.show_page("account")
                )

            case "main":
                self.main_logger.info("Switched to Main page")
                main = self.page.current_page
                ic(f"Connecting to_settings signal on {main}")
                self.main_logger.debug(self.page.current_page)
                main.to_settings.connect(
                    lambda: self.page.show_page("launcher_settings")
                )

            case "download":
                self.main_logger.info("Switched to Download page")
                download = self.page.current_page
                download.download_complete.connect(lambda: self.page.show_page("main"))

            case "login":
                self.main_logger.info("Switched to Login page")
                login = self.page.current_page
                login.go_to_reg.connect(lambda: self.page.show_page("registration"))

            case "launcher_settings":
                self.main_logger.info("Switched to Launcher Settings")
                launcher_settings = self.page.current_page
                launcher_settings.to_game_settings.connect(
                    lambda: self.page.show_page("game_settings")
                )
                launcher_settings.go_back.connect(lambda: self.page.show_page("main"))
                launcher_settings.to_account.connect(
                    lambda: self.page.show_page("account")
                )

            case "game_settings":
                self.main_logger.info("Switched to Game Settings")
                game_settings = self.page.current_page
                game_settings.to_launcher_settings.connect(
                    lambda: self.page.show_page("launcher_settings")
                )
                game_settings.go_back.connect(lambda: self.page.show_page("main"))
                game_settings.delete_complete.connect(
                    lambda: self.page.show_page("download")
                )

            case _:

                self.main_logger.warning(f"Unhandled page name: {page_name}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_logger.debug("Mouse press event detected (window drag start)")
            self.drag_position = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            self.mouse_logger.debug("Mouse move event detected (window moving)")
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.mouse_logger.debug("Mouse release event detected (window drag end)")
        self.drag_position = None
        event.accept()

    def check_status(self):
        ic(
            f"Checking status: user_status={self.user_status}, download_status={self.download_status}"
        )

        if not self.user_status:
            ic("User not logged in, showing home page.")
            self.page.show_page("home")
        elif self.user_status and not self.download_status:
            ic("User logged in, but download is not complete, showing download page.")
            self.page.show_page("account")
        elif self.user_status and self.download_status:
            ic("User logged in and download complete, showing main page.")
            self.page.show_page("main")
        else:
            ic("Fallback: showing account page.")
            self.page.show_page("home")


def main():
    app = QApplication(sys.argv)
    launcher = Launcher()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
