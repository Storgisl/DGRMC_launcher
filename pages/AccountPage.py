from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal

from .Page import Page


class AccountPage(Page):
    go_to_reg = Signal()

    def __init__(self, stacked_widget):
        super().__init__()
        self.setObjectName("account_page")
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        self.account_layout = QVBoxLayout()
        self.account_layout.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addSpacing(20)
        layout.addWidget(self.create_navbar())
        layout.addStretch()
        layout.addLayout(self.account_layout)
        layout.addStretch()
        layout.addLayout(self.footer_layout)
        self.setLayout(layout)

    def create_navbar(self):
        navbar_layout = QHBoxLayout()
        navbar_layout.setContentsMargins(40, 0, 40, 0)

        logo_label = QLabel(self)
        logo_pixmap = QPixmap("assets/Logo.png")
        logo_label.setPixmap(logo_pixmap)
        navbar_layout.addWidget(logo_label, alignment=Qt.AlignLeft)

        version_label = QLabel("v2.1.1", self)
        version_label.setStyleSheet("font-size: 16px; color: #F0F0F0;")
        version_label.setFont(self.medium_font)
        navbar_layout.addWidget(version_label, alignment=Qt.AlignRight)

        navbar_frame = QFrame(self)
        navbar_frame.setLayout(navbar_layout)
        navbar_frame.setFixedHeight(44)
        return navbar_frame

    def load_accounts(self):
        self.clear_layout(self.account_layout)

        users = self.user_data
        if users:
            account_list_layout = QHBoxLayout()
            account_list_layout.setAlignment(Qt.AlignCenter)

            for username in users.keys():
                account_list_layout.addWidget(self.create_account_button(username))

            add_account_button = self.create_add_account_button()
            account_list_layout.addWidget(add_account_button)

            layout.addLayout(account_list_layout)
        else:
            layout.addWidget(self.create_add_account_button())

    def create_account_button(self, username):
        account_button = QPushButton(username, self)
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
        account_button.clicked.connect(lambda: self.login_user(username=username))
        return account_button

    def create_add_account_button(self):
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
        add_account_button.clicked.connect(lambda: self.emit_signal(self.go_to_reg))
        return add_account_button

    def clear_layout(self, layout):
        """Removes all widgets from a layout."""
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
        elif item.layout():
            self.clear_layout(item.layout())