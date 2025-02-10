from PySide6.QtCore import Signal

from UI import HomePageUI
from .Page import Page


class HomePage(Page):
    go_to_account = Signal()

    def __init__(self, stacked_widget):
        super().__init__()
        self.page_logger.info("Home page initialized")
        self.stacked_widget = stacked_widget
        self.ui = HomePageUI(self)
