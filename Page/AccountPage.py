from PySide6.QtCore import Signal

from UI import AccountPageUI
from .Page import Page


class AccountPage(Page):
    go_to_reg = Signal()

    def __init__(self, stacked_widget):
        super().__init__()
        self.page_logger.info("Account page initialized")
        self.setObjectName("account_page")
        self.stacked_widget = stacked_widget
        self.ui = AccountPageUI(self)
