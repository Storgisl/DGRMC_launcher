from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from Factory import LoggerFactory, UIFactory

from .BasePageUI import BasePageUI


class AccountPageUI(BasePageUI):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.logger = LoggerFactory("UI").get_logger()
        self.ui_factory = UIFactory()
        self.setup_ui()
        self.logger.info("AccountUI init")

    def setup_ui(self):
        layout = self.ui_factory.create_layout(
            layout_type=QVBoxLayout,
            spacing=20,
            elements=[
                {"widget": self.create_navbar_frame(), "stretch": True},
                {
                    "layout": self.load_accounts(self.parent.user_data),
                    "stretch": True,
                },
                {"layout": self.create_footer_layout()},
            ],
        )
        self.parent.setLayout(layout)

    def load_accounts(self, user_data: dict) -> None:
        account_layout = self.ui_factory.create_layout(
            layout_type=QVBoxLayout, alignment=Qt.AlignCenter
        )
        users = user_data
        if users:
            account_list_layout = self.ui_factory.create_layout(
                layout_type=QHBoxLayout, alignment=Qt.AlignCenter
            )

            for username in users.keys():
                account_list_layout.addWidget(self.create_account_button(username))

            add_account_button = self.create_add_account_button()
            account_list_layout.addWidget(add_account_button)

            account_layout.addLayout(account_list_layout)
            return account_layout
        else:
            account_layout.addWidget(self.create_add_account_button())
            return account_layout

    def create_account_button(self, username):
        account_button = self.ui_factory.create_button(
            text=username,
            stylesheet="""
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
            """,
            font=self.bold_font,
            on_click_callback=self.parent.login_user,
            callback_args=[username],
            cursor=True,
        )
        self.logger.info("AccountPage UI account button complete")
        return account_button

    def create_add_account_button(self):
        add_account_button = self.ui_factory.create_button(
            stylesheet="""
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
        """,
            cursor=True,
            emit_signal=self.parent.emit_signal,
            signal_args=[self.parent.go_to_reg],
        )
        self.logger.info("AccountPage UI add account button complete")
        return add_account_button
