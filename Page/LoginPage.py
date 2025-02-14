from PySide6.QtCore import Signal

from UI import LoginPageUI

from .Page import Page


class LoginPage(Page):
    go_to_reg = Signal()

    def __init__(self, stacked_widget):
        super().__init__()
        self.page_logger.info("Login page initialized")
        self.setObjectName("login_page")
        self.stacked_widget = stacked_widget
        self.ui = LoginPageUI(self)
