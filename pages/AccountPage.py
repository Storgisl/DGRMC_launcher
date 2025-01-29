import sys
import os

from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal

from .Page import Page


class AccountPage(Page):
    go_to_reg = Signal()
    go_to_main_page = Signal()
    go_to_download_page = Signal()

    def __init__(self, stacked_widget):
        super().__init__()
        self.setObjectName("account_page")
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        # Navbar
        navbar_layout = QHBoxLayout()
        navbar_layout.setContentsMargins(
            40, 0, 40, 0
        )  # Добавляем отступы слева и справа
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("assets/Logo.png")
        logo_label.setPixmap(logo_pixmap)
        navbar_layout.addWidget(logo_label, alignment=Qt.AlignLeft)
        version_label = QLabel("v2.1.1", self)
        version_label.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                color: #F0F0F0;
                padding: 0;
                vertical-align: middle;
            }
        """
        )
        version_label.setFont(self.medium_font)
        navbar_layout.addWidget(version_label, alignment=Qt.AlignRight)
        navbar_frame = QFrame(self)
        navbar_frame.setLayout(navbar_layout)
        navbar_frame.setFixedHeight(44)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        frame = QFrame(self)
        frame.setFixedSize(440, 300)
        frame.setStyleSheet(
            """
            QFrame {
                background-color: #412483;
                border-radius: 10px;
            }
        """
        )
        frame_layout = QVBoxLayout()
        frame_layout.setAlignment(Qt.AlignCenter)

        text_image_label = QLabel(self)
        text_image_pixmap = QPixmap("assets/Text.png")
        text_image_label.setPixmap(text_image_pixmap)
        frame_layout.addWidget(
            text_image_label, alignment=Qt.AlignTop | Qt.AlignHCenter
        )

        top_spacer = QSpacerItem(0, 30, QSizePolicy.Minimum, QSizePolicy.Fixed)
        frame_layout.addItem(top_spacer)

        if self.user_status():
            account_layout = QHBoxLayout()
            account_layout.setAlignment(Qt.AlignCenter)
            account_button = QPushButton(self.username_var, self)
            account_button.setStyleSheet(
                """
                QPushButton {
                    background-image: url(assets/Profile.png);
                    background-repeat: no-repeat;
                    background-position: center;
                    background-color: transparent;
                    border: none;
                    width: 120px;
                    height: 120px;
                    font-size: 14px;
                    color: #412483;
                    padding: 0;
                    text-align: bottom;
                }
                QPushButton:hover {
                    background-image: url(assets/ProfileHover.png);
                    color: #B59AEE;
                }
            """
            )
            account_button.setCursor(Qt.PointingHandCursor)
            account_button.setFont(self.bold_font)
            account_layout.addWidget(account_button)

            if self.download_status():
                account_button.clicked.connect(self.main_page)
            else:
                account_button.clicked.connect(self.download_page)

            button_spacer = QSpacerItem(20, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
            account_layout.addItem(button_spacer)
            add_account_button = QPushButton(self)
            add_account_button.setStyleSheet(
                """
                QPushButton {
                    background-image: url(assets/AddAccountIcon.png);
                    background-repeat: no-repeat;
                    background-position: center;
                    background-color: transparent;
                    border: none;
                    width: 120px;
                    height: 120px;
                }
                QPushButton:hover {
                    background-image: url(assets/AddAccountIconHover.png);
                }
            """
            )
            add_account_button.setCursor(Qt.PointingHandCursor)
            add_account_button.clicked.connect(self.add_account)
            account_layout.addWidget(add_account_button)
            frame_layout.addLayout(account_layout)
        else:
            add_account_button = QPushButton(self)
            add_account_button.setStyleSheet(
                """
                QPushButton {
                    background-image: url(assets/AddAccountIcon.png);
                    background-repeat: no-repeat;
                    background-position: center;
                    background-color: transparent;
                    border: none;
                    width: 120px;
                    height: 120px;
                }
                QPushButton:hover {
                    background-image: url(assets/AddAccountIconHover.png);
                }
            """
            )
            add_account_button.setCursor(Qt.PointingHandCursor)
            add_account_button.clicked.connect(self.add_account)
            frame_layout.addWidget(add_account_button, alignment=Qt.AlignCenter)

            add_account_label = QLabel("Add any account", self)
            add_account_label.setStyleSheet(
                """
                QLabel {
                    font-size: 14px;
                    color: #7247CB;
                }
            """
            )
            add_account_label.setFont(self.light_font)
            frame_layout.addWidget(add_account_label, alignment=Qt.AlignCenter)

        frame.setLayout(frame_layout)
        main_layout.addWidget(frame, alignment=Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addSpacing(20)
        layout.addWidget(navbar_frame)
        layout.addSpacing(80)
        layout.addLayout(main_layout)
        layout.addStretch()
        layout.addLayout(self.footer_layout)
        self.setLayout(layout)

    def load_accounts(self):
        user_data = self.data_manip.load_user_data(
            directory=self.config_dir, json_file=self.user_data_json
        )
        accounts = user_data.get("accounts", [])
        return accounts

    def user_status(self) -> bool:
        self.user_data = self.data_manip.load_user_data(
            directory=self.config_dir, json_file=self.user_data_json
        )
        self.username_var = self.user_data.get("username", "")
        self.password_var = self.user_data.get("password", "")
        if self.username_var not in ("", None) and self.password_var not in ("", None):
            return True
        else:
            return False

    def check_dirs(self, directory: str, folders: list) -> bool:
        try:
            contents = os.listdir(directory)
            for folder in folders:
                if folder not in contents:
                    return False
            return True
        except FileNotFoundError:
            print(f"Directory '{directory}' not found.")
            return False

    def download_status(self) -> bool:
        dgrmc_dir = os.path.join(self.mc_dir, "DGRMClauncher")
        required_folders = ["assets", "libraries", "runtime", "versions"]
        if self.check_dirs(directory=dgrmc_dir, folders=required_folders):
            return True
        else:
            if (
                dgrmc_dir is False
                and self.username_var not in ("", None)
                and self.password_var not in ("", None)
            ):
                return True
            else:
                return False

    def add_account(self):
        self.go_to_reg.emit()

    def main_page(self):
        self.go_to_main_page.emit()

    def download_page(self):
        self.go_to_download_page.emit()
