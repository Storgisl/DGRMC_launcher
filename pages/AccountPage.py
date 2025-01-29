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
        self.account_layout = QVBoxLayout()
        self.account_layout.setAlignment(Qt.AlignCenter)

        self.load_accounts()

        layout = QVBoxLayout()
        layout.addWidget(self.create_navbar())
        layout.addLayout(self.account_layout)
        layout.addStretch()
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
        """Loads user accounts dynamically from Page's user data."""
        self.clear_layout(self.account_layout)

        users = self.user_data  # Now inherited from Page
        if users:
            account_list_layout = QHBoxLayout()
            account_list_layout.setAlignment(Qt.AlignCenter)

            for username in users.keys():
                account_list_layout.addWidget(self.create_account_button(username))

            # Add "Add Account" button
            add_account_button = self.create_add_account_button()
            account_list_layout.addWidget(add_account_button)

            self.account_layout.addLayout(account_list_layout)
        else:
            self.account_layout.addWidget(self.create_add_account_button())

    def create_account_button(self, username):
        """Creates a button for each account."""
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
        account_button.clicked.connect(lambda: self.login_user(username))
        return account_button

    def create_add_account_button(self):
        """Creates the 'Add Account' button."""
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
        return add_account_button

    def add_account(self):
        """Opens the registration page when adding a new account."""
        self.go_to_reg.emit()

    def login_user(self, username):
        """Handles clicking on an account button."""
        if self.download_status():
            self.go_to_main_page.emit()
        else:
            self.go_to_download_page.emit()

    def clear_layout(self, layout):
        """Removes all widgets from a layout."""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())
