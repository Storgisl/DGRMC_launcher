from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PySide6.QtCore import Qt

from Factory import LoggerFactory
from .BasePageUI import BasePageUI


class LauncherSettingsUI(BasePageUI):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup_ui()
        self.logger = LoggerFactory("UI").get_logger()
        self.logger.info("LauncherSettingsUI")

    def setup_ui(self):
        layout = self.ui_factory.create_layout(
            layout_type=QVBoxLayout,
            spacing=20,
            elements=[
                {
                    "widget": self.create_navbar_settings_frame(),
                    "spacing": 40,
                },
                {"layout": self.create_main_layout(), "stretch": True},
                {
                    "layout": self.create_footer_layout(),
                },
            ],
        )
        self.parent.setLayout(layout)

    def create_navbar_settings_frame(self):
        launcher_settings_button = self.ui_factory.create_button(
            text="Launcher settings",
            stylesheet="""
            QPushButton {
                background-color: transparent;
                color: #7C58FF;
                font-size: 16px;
                font-weight: 500;
                border: none;
            }
        """,
            font=self.medium_font,
        )
        game_settings_button = self.ui_factory.create_button(
            text="Game settings",
            stylesheet="""
            QPushButton {
                background-color: transparent;
                color: #F0F0F0;
                font-size: 16px;
                font-weight: 500;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """,
            font=self.medium_font,
            cursor=True,
            emit_signal=self.parent.emit_signal,
            signal_args=[self.parent.to_game_settings],
        )

        logo_label = self.ui_factory.create_label(pixmap="assets/Logo.png")

        version_label = self.ui_factory.create_label(
            text="V 1.0",
            stylesheet="""
            QLabel {
                font-size: 16px;
                color: #F0F0F0;
                padding: 0;
                vertical-align: middle;
            }
        """,
            font=self.medium_font,
        )
        navbar_settings_layout = self.ui_factory.create_layout(
            layout_type=QHBoxLayout,
            contents_margins=(40, 0, 40, 0),
            elements=[
                {
                    "widget": logo_label,
                    "alignment": Qt.AlignmentFlag.AlignLeft,
                    "spacing": 140,
                },
                {"widget": launcher_settings_button, "spacing": 160},
                {"widget": game_settings_button, "stretch": True},
                {
                    "widget": version_label,
                    "alignment": Qt.AlignmentFlag.AlignCenter,
                },
            ],
        )
        navbar_settings_frame = self.ui_factory.create_frame(
            layout=navbar_settings_layout, fixed_size=44
        )

        return navbar_settings_frame

    def create_main_layout(self):
        back_button = self.ui_factory.create_button(
            text="back",
            stylesheet="""
            QPushButton {
                background-image: url(assets/GoBack.png);
                background-repeat: no-repeat;
                background-position: left;
                background-color: transparent;
                border: none;
                padding-left: 15px;
                padding-right: 0;
                min-height: 30px;
                max-height: 30px;
                min-width: 40px;
                max-width: 40px;
                font-size: 14px;
                color: #7247CB;
                text-align: left;
                margin-left: 15px;
                margin-top: 5px;
                font-weight: 200;
            }
            QPushButton:hover {
                background-image: url(assets/GoBackHover.png);
                color: #F0F0F0;
            }
        """,
            cursor=True,
            font=self.extra_light_font,
            emit_signal=self.parent.emit_signal,
            signal_args=[self.parent.go_back],
        )

        change_account = self.ui_factory.create_label(
            text="You may change account",
            stylesheet="""
            QLabel {
                font-size: 16px;
                color: #7247CB;
                font-weight: 200;
            }
        """,
            font=self.extra_light_font,
        )
        change_button = self.ui_factory.create_button(
            text="Change",
            stylesheet="""
            QPushButton {
                background-color: #503684;
                color: #F0F0F0;
                font-size: 16px;
                border-radius: 10px;
                min-height: 35px;
                max-height: 35px;
                min-width: 170px;
                max-width: 170px;
                font-weight: 400;
            }
            QPushButton:hover {
                background-color: #7247CB;
            }
        """,
            font=self.regular_font,
            cursor=True,
            emit_signal=self.parent.emit_signal,
            signal_args=[self.parent.to_account],
        )

        check_updates_label = self.ui_factory.create_label(
            text="Check for updates",
            stylesheet="""
            QLabel {
                font-size: 16px;
                color: #7247CB;
                font-weight: 200;
            }
        """,
            font=self.extra_light_font,
        )
        check_upd_button = self.ui_factory.create_button(
            text="Check",
            stylesheet="""
            QPushButton {
                background-color: #503684;
                color: #F0F0F0;
                font-size: 16px;
                border-radius: 10px;
                min-height: 35px;
                max-height: 35px;
                min-width: 170px;
                max-width: 170px;
                font-weight: 400;
            }
            QPushButton:hover {
                background-color: #7247CB;
            }
        """,
            font=self.regular_font,
            cursor=True,
            on_click_callback=self.parent.check_updates,
        )
        open_folder_label = self.ui_factory.create_label(
            text="Open game folder",
            stylesheet="""
            QLabel {
                font-size: 16px;
                color: #7247CB;
                font-weight: 200;
            }
        """,
            font=self.extra_light_font,
        )

        open_folder_button = self.ui_factory.create_button(
            text="Open folder",
            stylesheet="""
            QPushButton {
                background-color: #503684;
                color: #F0F0F0;
                font-size: 16px;
                border-radius: 10px;
                min-height: 35px;
                max-height: 35px;
                min-width: 170px;
                max-width: 170px;
                font-weight: 400;
            }
            QPushButton:hover {
                background-color: #7247CB;
            }
        """,
            font=self.regular_font,
            cursor=True,
            on_click_callback=self.parent.open_folder,
        )

        inner_navbar_settings_layout = self.ui_factory.create_layout(
            layout_type=QHBoxLayout,
            alignment=Qt.AlignLeft,
            elements=[{"widget": back_button}],
        )
        frame_layout = self.ui_factory.create_layout(
            layout_type=QVBoxLayout,
            alignment=Qt.AlignTop,
            elements=[
                {
                    "layout": inner_navbar_settings_layout,
                    "spacer": (0, 30, QSizePolicy.Minimum, QSizePolicy.Fixed),
                },
                {"widget": change_account, "alignment": Qt.AlignCenter},
                {
                    "widget": change_button,
                    "alignment": Qt.AlignCenter,
                    "spacer": (0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed),
                },
                {"widget": check_updates_label, "alignment": Qt.AlignCenter},
                {
                    "widget": check_upd_button,
                    "alignment": Qt.AlignCenter,
                    "spacer": (0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed),
                },
                {"widget": open_folder_label, "alignment": Qt.AlignCenter},
                {"widget": open_folder_button, "alignment": Qt.AlignCenter},
            ],
        )
        frame = self.ui_factory.create_frame(
            layout=frame_layout,
            stylesheet="""
            QFrame {
                background-color: #412483;
                border-radius: 10px;
            }
        """,
            fixed_size=(400, 400),
        )
        main_layout = self.ui_factory.create_layout(
            layout_type=QVBoxLayout,
            alignment=Qt.AlignCenter,
            elements=[{"widget": frame, "alignment": Qt.AlignCenter}],
        )
        return main_layout