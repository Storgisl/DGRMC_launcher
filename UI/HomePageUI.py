from PySide6.QtWidgets import (
    QVBoxLayout,
    QSizePolicy,
)
from PySide6.QtCore import Qt

from .BasePageUI import BasePageUI


class HomePageUI(BasePageUI):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup_ui()
        self.logger.info("HomeUI init")

    def setup_ui(self):
        layout = self.ui_factory.create_layout(
            layout_type=QVBoxLayout,
            spacing=20,
            elements=[
                {
                    "widget": self.create_navbar_frame(),
                    "spacing": 60,
                },
                {"layout": self.create_main_layout(), "stretch": True},
                {
                    "layout": self.create_footer_layout(),
                },
            ],
        )
        self.parent.setLayout(layout)

    def create_main_layout(self):
        main_image_label = self.ui_factory.create_label(pixmap="assets/Main.png")
        text_image_label = self.ui_factory.create_label(pixmap="assets/Text.png")
        start_button = self.ui_factory.create_button(
            text="Start Journey",
            stylesheet="""
            QPushButton {
                background-color: #412483;
                color: #F0F0F0;
                font-size: 14px;
                border-radius: 10px;
                min-height: 35px;
                max-height: 35px;
                min-width: 170px;
                max-width: 170px;
            }
            QPushButton:hover {
                background-color: #7247CB;
            }
        """,
            font=self.bold_font,
            emit_signal=self.parent.emit_signal,
            signal_args=[self.parent.go_to_account],
        )

        main_layout = self.ui_factory.create_layout(
            layout_type=QVBoxLayout,
            alignment=Qt.AlignCenter,
            elements=[
                {
                    "widget": main_image_label,
                    "alignment": Qt.AlignCenter,
                    "spacer": (5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed),
                },
                {
                    "widget": text_image_label,
                    "alignment": Qt.AlignCenter,
                    "spacer": (5, 30, QSizePolicy.Minimum, QSizePolicy.Fixed),
                },
                {
                    "widget": start_button,
                    "alignment": Qt.AlignCenter,
                },
            ],
        )

        return main_layout
