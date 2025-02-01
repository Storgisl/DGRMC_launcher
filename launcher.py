import os
import sys
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QStackedWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QSpacerItem,
    QSizePolicy,
    QLabel,
)
from PySide6.QtGui import QMouseEvent, QFontDatabase, QFont
from PySide6.QtCore import Qt
from icecream import ic

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages import (
    RegistrationPage,
    LauncherSettings,
    HomePage,
    GameSettings,
    MainPage,
    AccountPage,
    LoginPage,
    DownloadPage,
)


class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupWindow()
        self.setupWidgets()
        self.check_user_status()
        self.check_download_status()
        self.signals_setup()
        self.drag_position = None

    def signals_setup(self):
        self.home_page.go_to_account.connect(self.show_account_page)
        self.account_page.go_to_reg.connect(self.show_registration_page)
        self.account_page.go_to_main_page.connect(self.show_main_page)
        self.account_page.go_to_download_page.connect(self.show_download_page)
        self.registration_page.go_to_login.connect(self.show_login_page)
        self.registration_page.registration_complete.connect(self.show_download_page)
        self.login_page.go_to_reg.connect(self.show_registration_page)
        self.download_page.download_complete.connect(self.show_main_page)
        self.main_page.to_settings.connect(self.show_launcher_settings_page)
        self.launcher_settings_page.to_game_settings.connect(
            self.show_game_settings_page
        )
        self.launcher_settings_page.go_back.connect(self.show_main_page)
        self.launcher_settings_page.to_account.connect(self.show_account_page)
        self.game_settings_page.to_launcher_settings.connect(
            self.show_launcher_settings_page
        )
        self.game_settings_page.go_back.connect(self.show_main_page)
        self.game_settings_page.delete_complete.connect(self.show_main_page)

    def setupWindow(self) -> None:
        self.setWindowTitle("Danga Launcher")
        self.setFixedSize(1000, 629)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def setupWidgets(self) -> None:
        bold_font_id = QFontDatabase.addApplicationFont("assets/Heebo-Bold.ttf")
        if bold_font_id == -1:
            print("Ошибка: Не удалось загрузить Heebo-Bold.ttf")
        bold_font = QFont(QFontDatabase.applicationFontFamilies(bold_font_id)[0])

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header_frame = QFrame(self)
        header_frame.setFixedHeight(24)
        header_frame.setStyleSheet(
            """
            QFrame {
                background-color: rgba(37, 32, 40, 120);  /* Полупрозрачный цвет */
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
        """
        )
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(
            10, 0, 10, 0
        )

        header_layout.addSpacing(470)

        launcherlabel = QLabel("Danga", self)
        launcherlabel.setStyleSheet(
            """
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                font-size: 14px;
                color: rgba(254, 254, 254, 120);
                font-weight: 700;
            }
        """
        )
        launcherlabel.setFont(bold_font)
        header_layout.addWidget(launcherlabel, alignment=Qt.AlignCenter)

        header_layout.addStretch()

        # Кнопка свертывания
        minimize_button = QPushButton("", self)
        minimize_button.setStyleSheet(
            """
            QPushButton {
                background-image: url(assets/minimize.png);
                background-repeat: no-repeat;
                background-position: left;
                background-color: transparent;
                border: none;
                min-width: 12px;
                max-width: 12px;
                min-height: 12px;
                max-height: 12px;
            }
            QPushButton:hover {
                background-image: url(assets/minimizeHover.png);
            }
        """
        )
        minimize_button.setCursor(Qt.PointingHandCursor)
        minimize_button.clicked.connect(self.showMinimized)
        header_layout.addWidget(minimize_button)

        header_layout.addSpacing(20)

        # Кнопка закрытия
        close_button = QPushButton("", self)
        close_button.setStyleSheet(
            """
            QPushButton {
                background-image: url(assets/close.png);
                background-repeat: no-repeat;
                background-position: left;
                background-color: transparent;
                border: none;
                min-width: 12px;
                max-width: 12px;
                min-height: 12px;
                max-height: 12px;
            }
            QPushButton:hover {
                background-image: url(assets/closeHover.png);
            }
        """
        )
        close_button.setCursor(Qt.PointingHandCursor)
        close_button.clicked.connect(self.close)
        header_layout.addWidget(close_button)

        header_frame.setLayout(header_layout)
        main_layout.addWidget(header_frame)

        top_spacer = QSpacerItem(0, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(top_spacer)

        # Фрейм для отображения страниц
        content_frame = QFrame(self)
        content_frame.setFixedSize(1000, 600)
        content_frame.setStyleSheet(
            """
            QFrame {
                background-color: rgba(0, 0, 0, 0);
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }
        """
        )

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Содержимое окна
        self.stacked_widget = QStackedWidget()
        self.home_page = HomePage(self.stacked_widget)
        self.registration_page = RegistrationPage(self.stacked_widget)
        self.login_page = LoginPage(self.stacked_widget)
        self.download_page = DownloadPage(self.stacked_widget)
        self.account_page = AccountPage(self.stacked_widget)
        self.main_page = MainPage(self.stacked_widget)
        self.launcher_settings_page = LauncherSettings(self.stacked_widget)
        self.game_settings_page = GameSettings(self.stacked_widget)
        ic(self.registration_page.user_status())
        ic(self.download_page.download_status())
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.registration_page)
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.download_page)
        self.stacked_widget.addWidget(self.account_page)
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.launcher_settings_page)
        self.stacked_widget.addWidget(self.game_settings_page)
        self.setCentralWidget(self.stacked_widget)
        self.stacked_widget.setCurrentWidget(self.home_page)

        content_layout.addWidget(self.stacked_widget)
        content_frame.setLayout(content_layout)

        main_layout.addWidget(content_frame)

        container = QFrame(self)
        container.setLayout(main_layout)
        container.setStyleSheet(
            """
            QFrame {
                border: none;
                background-color: rgba(0, 0, 0, 0);
                border-radius: 8px;
            }
        """
        )

        self.setCentralWidget(container)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.drag_position = None
        event.accept()

    def check_user_status(self) -> None:
        try:
            if self.registration_page.user_status() is True:
                self.show_download_page()
            else:
                self.show_home_page()
        except Exception as e:
            print(f"Error: {e}")
            self.show_home_page()

    def check_download_status(self) -> None:
        try:
            if self.download_page.download_status() is True:
                self.show_main_page()
            else:
                if self.registration_page.user_status() is False:
                    self.show_home_page()
                else:
                    self.show_home_page()
        except Exception as e:
            print(f"Error: {e}")

    def show_registration_page(self):
        ic("reg")
        self.stacked_widget.setCurrentWidget(self.registration_page)

    def show_download_page(self):
        ic("download")
        self.stacked_widget.setCurrentWidget(self.download_page)

    def show_home_page(self) -> None:
        ic("home")
        self.stacked_widget.setCurrentWidget(self.home_page)

    def show_account_page(self):
        ic("acc")
        self.stacked_widget.setCurrentWidget(self.account_page)

    def show_login_page(self):
        ic("login")
        self.stacked_widget.setCurrentWidget(self.login_page)

    def show_main_page(self):
        ic("main")
        self.stacked_widget.setCurrentWidget(self.main_page)

    def show_launcher_settings_page(self):
        ic("launcher settings")
        self.stacked_widget.setCurrentWidget(self.launcher_settings_page)

    def show_game_settings_page(self):
        ic("game settings")
        self.stacked_widget.setCurrentWidget(self.game_settings_page)

    def clear_frames(self) -> None:
        ic("clear")
        self.home_page.hide()
        self.registration_page.hide()
        self.login_page.hide()
        self.download_page.hide()
        self.main_page.hide()
        self.launcher_settings_page.hide()
        self.game_settings_page.hide()


def main():
    app = QApplication(sys.argv)
    launcher = Launcher()
    launcher.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

