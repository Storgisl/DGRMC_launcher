from PySide6.QtCore import Signal

from UI import DownloadPageUI
from .Page import Page


class DownloadPage(Page):
    set_status_signal = Signal(str)
    set_progress_signal = Signal(int)
    set_max_signal = Signal(int)
    download_complete = Signal()
    finished = Signal()

    def __init__(self, stacked_widget):
        super().__init__()
        self.page_logger.info("Download page initialized")
        self.setObjectName("download_page")
        self.stacked_widget = stacked_widget

        self.ui = DownloadPageUI(self)

        self.set_status_signal.connect(self.ui.update_status)
        self.set_progress_signal.connect(self.ui.update_progress)
        self.set_max_signal.connect(self.ui.set_progress_max)
