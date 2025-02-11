from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PySide6.QtCore import Qt

from Factory import LoggerFactory

from .BasePageUI import BasePageUI


class LauncherUI(BasePageUI):
    def __init__(self, parent, stacked_widget):
        super().__init__()
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.logger = LoggerFactory("UI").get_logger()
        self.setupWindow()
        self.parent.setCentralWidget(self.setup_ui())
        self.logger.info("LauncherUI init")

    def setupWindow(self) -> None:
        self.parent.setWindowTitle("Danga Launcher")
        self.parent.setFixedSize(1000, 629)
        self.parent.setWindowFlags(Qt.FramelessWindowHint)
        self.parent.setAttribute(Qt.WA_TranslucentBackground)
        self.logger.info("LauncherUI window init complete")

    def setup_ui(self):
        launcher_label = self.ui_factory.create_label(
            text="Danga",
            stylesheet="""
            QLabel {
                background-color: rgba(0, 0, 0, 0);
                font-size: 14px;
                color: rgba(254, 254, 254, 120);
                font-weight: 700;
            }
        """,
            font=self.bold_font,
        )

        minimize_button = self.ui_factory.create_button(
            text="",
            stylesheet="""
            QPushButton {
                background-image: url(assets/minimize.png);
                background-repeat: no-repeat;
                background-position: left;
                background-color: transparent;
                border: none;
                min-width: 12px;
                max-width: 12px;
                min-height: 12px;
                max-height: 12px;
            }
            QPushButton:hover {
                background-image: url(assets/minimizeHover.png);
            }
        """,
            cursor=True,
            on_click_callback=self.parent.showMinimized,
        )

        # Кнопка закрытия
        close_button = self.ui_factory.create_button(
            text="",
            stylesheet="""
            QPushButton {
                background-image: url(assets/close.png);
                background-repeat: no-repeat;
                background-position: left;
                background-color: transparent;
                border: none;
                min-width: 12px;
                max-width: 12px;
                min-height: 12px;
                max-height: 12px;
            }
            QPushButton:hover {
                background-image: url(assets/closeHover.png);
            }
        """,
            cursor=True,
            on_click_callback=self.parent.close,
        )
        header_layout = self.ui_factory.create_layout(
            layout_type=QHBoxLayout,
            contents_margins=(10, 0, 10, 0),
            spacing=470,
            elements=[
                {
                    "widget": launcher_label,
                    "alignment": Qt.AlignCenter,
                    "stretch": True,
                },
                {"widget": minimize_button, "spacing": 20},
                {"widget": close_button},
            ],
        )

        content_layout = self.ui_factory.create_layout(
            layout_type=QVBoxLayout,
            contents_margins=(0, 0, 0, 0),
            elements=[{"widget": self.stacked_widget}],
        )

        header_frame = self.ui_factory.create_frame(
            layout=header_layout,
            fixed_size=24,
            stylesheet="""
            QFrame {
                background-color: rgba(37, 32, 40, 120);  /* Полупрозрачный цвет */
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
        """,
        )

        content_frame = self.ui_factory.create_frame(
            layout=content_layout,
            fixed_size=(1000, 600),
            stylesheet="""
            QFrame {
                background-color: rgba(0, 0, 0, 0);
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }
        """,
        )

        main_layout = self.ui_factory.create_layout(
            layout_type=QVBoxLayout,
            contents_margins=(0, 0, 0, 0),
            spacing=0,
            elements=[
                {
                    "widget": header_frame,
                    "spacer": (0, 5, QSizePolicy.Minimum, QSizePolicy.Expanding),
                },
                {
                    "widget": content_frame,
                },
            ],
        )
        container = self.ui_factory.create_frame(
            layout=main_layout,
            stylesheet="""
            QFrame {
                border: none;
                background-color: rgba(0, 0, 0, 0);
                border-radius: 8px;
            }
        """,
        )
        return container
