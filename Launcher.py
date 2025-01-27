import os
import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QStackedWidget
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import Qt
from icecream import ic
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.HomePage import HomePage
from pages.RegistrationPage import RegistrationPage
from pages.LoginPage import LoginPage
from pages.MainPage import MainPage
from pages.DownloadPage import DownloadPage
from pages.InstallPage import InstallPage
from pages.AccountPage import AccountPage
from pages.LauncherSettings import LauncherSettings
from pages.GameSettings import GameSettings

class Launcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupWindow()
        self.setupWidgets()
        self.check_user_status()
        self.check_download_status()
        self.background_image = QPixmap("assets/Back.png")
        if not self.background_image or self.background_image.isNull():
            print("Ошибка: Изображение back.png не найдено или повреждено")
        self.signals_setup()
    
    def signals_setup(self):
        self.home_page.go_to_account.connect(
            self.show_account_page
        )
        self.account_page.go_to_reg.connect(
            self.show_registration_page
        )
        self.account_page.go_to_main_page.connect(
            self.show_main_page
        )
        self.account_page.go_to_download_page.connect(
            self.show_download_page
        )
        self.registration_page.go_to_login.connect(
            self.show_login_page
        )
        self.registration_page.registration_complete.connect(
            self.show_download_page
        )
        self.login_page.go_to_reg.connect(
            self.show_registration_page
        )
        self.download_page.go_to_install.connect(
            self.show_install_page
        )
        self.install_page.download_complete.connect(
            self.show_main_page
        )
        self.main_page.to_settings.connect(
            self.show_launcher_settings_page
        )
        self.launcher_settings_page.to_game_settings.connect(
            self.show_game_settings_page
        )
        self.launcher_settings_page.go_back.connect(
            self.show_main_page
        )
        self.launcher_settings_page.to_account.connect(
            self.show_account_page
        )
        self.game_settings_page.to_launcher_settings.connect(
            self.show_launcher_settings_page
        )
        self.game_settings_page.go_back.connect(
            self.show_main_page
        )

    def setupWindow(self) -> None:
        self.setWindowTitle("Danga Launcher")
        self.setFixedHeight(600)
        self.setFixedWidth(1000)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        try:
            scaled_image = self.background_image.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding
            )
            painter.drawPixmap(0, 0, scaled_image)
        finally:
            painter.end()

    def setupWidgets(self) -> None:
        self.stacked_widget = QStackedWidget()
        self.home_page = HomePage(self.stacked_widget)
        self.registration_page = RegistrationPage(self.stacked_widget)
        self.login_page = LoginPage(self.stacked_widget)
        self.download_page = DownloadPage(self.stacked_widget)
        self.account_page = AccountPage(self.stacked_widget)
        self.main_page = MainPage(self.stacked_widget)
        self.install_page = InstallPage(self.stacked_widget)
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
        self.stacked_widget.addWidget(self.install_page)
        self.stacked_widget.addWidget(self.launcher_settings_page)
        self.stacked_widget.addWidget(self.game_settings_page)
        
        self.setCentralWidget(self.stacked_widget)
        self.stacked_widget.setCurrentWidget(self.home_page)

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
        print("reg")
        self.stacked_widget.setCurrentWidget(self.registration_page)

    def show_download_page(self):
        print("download")
        self.stacked_widget.setCurrentWidget(self.download_page)

    def show_home_page(self) -> None:
        print("home")
        self.stacked_widget.setCurrentWidget(self.home_page)
    
    def show_account_page(self):
        print("acc")
        self.stacked_widget.setCurrentWidget(self.account_page)
    
    def show_login_page(self):
        print("login")
        self.stacked_widget.setCurrentWidget(self.login_page)

    def show_main_page(self):
        print("main")
        self.stacked_widget.setCurrentWidget(self.main_page)
    
    def show_install_page(self):
        print("install")
        self.stacked_widget.setCurrentWidget(self.install_page)
    
    def show_launcher_settings_page(self):
        print("laun settings")
        self.stacked_widget.setCurrentWidget(self.launcher_settings_page)
    
    def show_game_settings_page(self):
        print("game settings")
        self.stacked_widget.setCurrentWidget(self.game_settings_page)
    
    def clear_frames(self) -> None:
        print("clear")
        self.home_page.hide()
        self.registration_page.hide()
        self.login_page.hide()
        self.download_page.hide()
        self.install_page.hide()
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