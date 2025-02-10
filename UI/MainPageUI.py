from PySide6.QtWidgets import (
    QVBoxLayout,
    QSizePolicy,
)
from PySide6.QtCore import Qt

from Factory import LoggerFactory
from .BasePageUI import BasePageUI


class MainPageUI(BasePageUI):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup_ui()
        self.logger = LoggerFactory("UI").get_logger()
        self.logger.info("MainPageUI init")

    def setup_ui(self):
        layout = self.ui_factory.create_layout(
            layout_type=QVBoxLayout,
            elements=[
                {"widget": self.create_navbar_frame(), "spacing": 20},
                {"layout": self.create_main_content(), "spacing": 20, "stretch": True},
                {"layout": self.create_footer_layout()},
            ],
        )
        self.parent.setLayout(layout)
        self.logger.info("MainPage UI setup complete")

    def create_main_content(self):
        text_image_label = self.ui_factory.create_label(
            pixmap="assets/MainPageLogo.png"
        )

        # Welcome Text
        nickname = self.ui_factory.create_label(
            text=f"Welcome back {self.parent.current_username_var}",
            stylesheet="font-size: 14px; color: #F0F0F0; font-weight: 200;",
            font=self.extra_light_font,
        )

        start_button = self.ui_factory.create_button(
            text="PLAY",
            stylesheet="""
                QPushButton {
                    background-color: rgba(0, 0, 0, 0);
                    border: none;
                    color: #F0F0F0;
                    font-size: 48px;
                    font-weight: 400;
                }
                QPushButton:hover {
                    text-decoration: underline;
                }
            """,
            font=self.light_font,
            cursor=True,
            on_click_callback=self.parent.run_mc,
        )

        # Settings Button
        settings_button = self.ui_factory.create_button(
            text="settings",
            stylesheet="""
                QPushButton {
                    background-color: rgba(0, 0, 0, 0);
                    border: none;
                    color: #F0F0F0;
                    font-size: 16px;
                    font-weight: 400;
                }
                QPushButton:hover {
                    text-decoration: underline;
                }
            """,
            font=self.regular_font,
            cursor=True,
            emit_signal=self.parent.emit_signal,
            signal_args=[self.parent.to_settings],
        )

        main_layout = self.ui_factory.create_layout(
            layout_type=QVBoxLayout,
            alignment=Qt.AlignmentFlag.AlignCenter,
            contents_margins=(40, 0, 40, 0),
            elements=[
                {"widget": text_image_label, "alignment": Qt.AlignmentFlag.AlignCenter},
                {
                    "widget": nickname,
                    "alignment": Qt.AlignmentFlag.AlignCenter,
                    "spacer": (0, 200, QSizePolicy.Minimum, QSizePolicy.Fixed),
                },
                {
                    "widget": start_button,
                    "alignment": Qt.AlignmentFlag.AlignCenter,
                    "spacer": (0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed),
                },
                {
                    "widget": settings_button,
                    "alignment": Qt.AlignmentFlag.AlignCenter,
                },
            ],
        )
        return main_layout
