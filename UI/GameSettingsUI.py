from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QSpacerItem,
    QSizePolicy,
    QSlider,
    QLineEdit,
    QCheckBox,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from Factory import LoggerFactory
from .BasePageUI import BasePageUI


class GameSettingsUI(BasePageUI):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.logger = LoggerFactory("UI").get_logger()
        self.setup_ui()
        self.logger.info("GameSettingsUI init")

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
            emit_signal=self.parent.emit_signal,
            signal_args=[self.parent.to_launcher_settings],
        )
        game_settings_button = self.ui_factory.create_button(
            text="Game settings",
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
            cursor=True,
        )

        logo_label = self.ui_factory.create_label(pixmap=QPixmap("assets/Logo.png"))

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

        memory_label = self.ui_factory.create_label(
            text="Game memory amount",
            stylesheet="""
            QLabel {
                font-size: 16px;
                color: #7247CB;
                font-weight: 200;
            }
        """,
            font=self.extra_light_font,
        )

        max_ram = self.parent.get_max_system_ram()

        memory_slider = self.ui_factory.create_slider(
            alignment=Qt.Horizontal,
            min_value=2048,
            max_value=max_ram,
            value=self.parent.ram_value,
            step=512,
            stylesheet="""
            QSlider {
                height: 8px;
                width: 350px;
                background-color: #503684;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background-color: #905DF3;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QSlider::add-page:horizontal {
                background-color: #503684;
            }
            QSlider::sub-page:horizontal {
                background-color: #503684;
            }
        """,
            on_value_changed=self.update_value_line,
        )

        min_value_label = self.ui_factory.create_label(
            text="2048",
            stylesheet="""
            QLabel {
                font-size: 14px;
                color: #7247CB;
                font-weight: 200;
            }
        """,
            font=self.extra_light_font,
        )

        value_line = self.ui_factory.create_line_edit(
            text=f"{str(self.parent.ram_value)} MiB",
            alignment=Qt.AlignCenter,
            stylesheet="""
            QLineEdit {
                background-color: #503684;
                color: #F0F0F0;
                font-size: 12px;
                font-weight: 200;
                border-radius: 8px;
                min-height: 20px;
                max-height: 20px;
                max-width: 70px;
                min-width: 70px;
            }
        """,
            font=self.light_font,
            on_editing_finished=self.update_slider_value,
        )

        max_value_label = self.ui_factory.create_label(
            text=f"{max_ram}",
            stylesheet="""
            QLabel {
                font-size: 14px;
                color: #7247CB;
                font-weight: 200;
            }
        """,
            font=self.extra_light_font,
        )

        resolution_label = self.ui_factory.create_label(
            text="Window resolution",
            stylesheet="""
            QLabel {
                font-size: 16px;
                color: #7247CB;
                font-weight: 200;
            }
        """,
            font=self.extra_light_font,
        )

        self.width_line = self.ui_factory.create_line_edit(
            text=str(self.parent.res_width),
            alignment=Qt.AlignCenter,
            stylesheet="""
            QLineEdit {
                background-color: #503684;
                color: #F0F0F0;
                font-size: 14px;
                font-weight: 400;
                border-radius: 8px;
                min-height: 30px;
                max-height: 30px;
                max-width: 70px;
                min-width: 70px;
            }
        """,
            font=self.regular_font,
        )

        x_label = self.ui_factory.create_label(
            text="x",
            stylesheet="""
            QLabel {
                font-size: 14px;
                color: #7247CB;
                font-weight: 200;
            }
        """,
            font=self.extra_light_font,
        )

        self.height_line = self.ui_factory.create_line_edit(
            text=str(self.parent.res_height),
            alignment=Qt.AlignCenter,
            stylesheet="""
            QLineEdit {
                background-color: #503684;
                color: #F0F0F0;
                font-size: 14px;
                font-weight: 400;
                border-radius: 8px;
                min-height: 30px;
                max-height: 30px;
                max-width: 70px;
                min-width: 70px;
            }
        """,
            font=self.regular_font,
        )

        fs_label = self.ui_factory.create_label(
            text="Fullscreen mode",
            stylesheet="""
            QLabel {
                font-size: 14px;
                color: #7247CB;
                font-weight: 200;
            }
        """,
            font=self.extra_light_font,
        )

        checkbox = self.ui_factory.create_checkbox(
            text="",
            stylesheet="""
            QCheckBox {
                background-color: #503684;
                border-radius: 8px;
                max-width: 19px;
                min-width: 19px;
                max-height: 19px;
                min-height: 19px;
            }
            QCheckBox::indicator {
                width: 19px;
                height: 19px;
            }
            QCheckBox::indicator:unchecked {
                image: url(assets/checkbox_unchecked.png);
            }
            QCheckBox::indicator:checked {
                image: url(assets/checkbox_checked.png);
            }
        """,
            on_state_change=self.parent.on_checkbox_state_changed,
        )

        delete_label = self.ui_factory.create_label(
            text="Delete minecraft",
            stylesheet="""
            QLabel {
                font-size: 14px;
                color: #7247CB;
                font-weight: 200;
            }
        """,
            font=self.extra_light_font,
        )

        self.delete_line = self.ui_factory.create_line_edit(
            placeholder_text='Type "delete"',
            alignment=Qt.AlignCenter,
            stylesheet="""
            QLineEdit {
                background-color: #503684;
                color: #F0F0F0;
                font-size: 14px;
                font-weight: 400;
                border-radius: 8px;
                min-height: 30px;
                max-height: 30px;
                max-width: 128px;
                min-width: 128px;
            }
        """,
            font=self.regular_font,
        )

        delete_button = self.ui_factory.create_button(
            stylesheet="""
            QPushButton {
                background-image: url(assets/delete_button.png);
                background-repeat: no-repeat;
                background-position: left;
                background-color: transparent;
                border: none;
                min-height: 30px;
                max-height: 30px;
                min-width: 34px;
                max-width: 34px;
            }
            QPushButton:hover {
                background-image: url(assets/delete_button_hover.png);
            }
        """,
            cursor=True,
            on_click_callback=self.parent.delete_mc,
        )

        save_button = self.ui_factory.create_button(
            text="Save",
            stylesheet="""
            QPushButton {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                color: #F0F0F0;
                font-size: 16px;
                font-weight: 400;
                min-height: 45px;
                max-height: 45px;
                min-width: 45px;
                max-width: 45px;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """,
            font=self.regular_font,
            cursor=True,
            on_click_callback=self.parent.save_config,
        )

        delete_layout = self.ui_factory.create_layout(
            layout_type=QHBoxLayout,
            alignment=Qt.AlignCenter,
            contents_margins=(17, 0, 17, 0),
            elements=[
                {"widget": delete_label, "stretch": True},
                {"widget": self.delete_line, "stretch": True},
                {"widget": delete_button},
            ],
        )

        resolution_layout = self.ui_factory.create_layout(
            layout_type=QHBoxLayout,
            alignment=Qt.AlignCenter,
            contents_margins=(17, 0, 17, 0),
            elements=[
                {"widget": self.width_line},
                {"widget": x_label},
                {"widget": self.height_line, "stretch": True},
                {"widget": fs_label, "spacing": 0},
                {"widget": checkbox},
            ],
        )

        labels_layout = self.ui_factory.create_layout(
            layout_type=QHBoxLayout,
            contents_margins=(17, 0, 17, 0),
            alignment=Qt.AlignCenter,
            elements=[
                {"widget": min_value_label, "stretch": True},
                {"widget": value_line, "stretch": True},
                {
                    "widget": max_value_label,
                    "spacer": (0, 20, QSizePolicy.Minimum, QSizePolicy.Fixed),
                },
            ],
        )

        inner_navbar_layout = self.ui_factory.create_layout(
            layout_type=QHBoxLayout,
            alignment=Qt.AlignLeft,
            elements=[{"widget": back_button}],
        )
        self.ram_error_label = self.ui_factory.create_label(text="")
        self.res_error_label = self.ui_factory.create_label(text="")
        frame_layout = self.ui_factory.create_layout(
            layout_type=QVBoxLayout,
            alignment=Qt.AlignTop,
            elements=[
                {
                    "layout": inner_navbar_layout,
                    "spacer": (0, 30, QSizePolicy.Minimum, QSizePolicy.Fixed),
                },
                {
                    "widget": memory_label,
                    "alignment": Qt.AlignCenter,
                    "spacer": (0, 5, QSizePolicy.Minimum, QSizePolicy.Fixed),
                },
                {
                    "widget": memory_slider,
                    "alignment": Qt.AlignCenter,
                    "spacer": (0, 5, QSizePolicy.Minimum, QSizePolicy.Fixed),
                },
                {"layout": labels_layout},
                {
                    "widget": resolution_label,
                    "alignment": Qt.AlignCenter,
                    "spacer": (0, 5, QSizePolicy.Minimum, QSizePolicy.Fixed),
                },
                {
                    "layout": resolution_layout,
                    "spacer": (0, 40, QSizePolicy.Minimum, QSizePolicy.Fixed),
                },
                {
                    "layout": delete_layout,
                    "spacer": (0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed),
                },
                {"widget": save_button, "alignment": Qt.AlignmentFlag.AlignCenter},
                {"widget": self.ram_error_label},
                {"widget": self.res_error_label},
            ],
        )

        frame = self.ui_factory.create_frame(
            layout=frame_layout,
            fixed_size=(400, 400),
            stylesheet="""
            QFrame {
                background-color: #412483;
                border-radius: 10px;
            }
        """,
        )

        main_layout = self.ui_factory.create_layout(
            layout_type=QVBoxLayout,
            elements=[
                {
                    "widget": frame,
                    "alignment": Qt.AlignCenter,
                }
            ],
        )
        self.memory_slider = memory_slider
        self.value_line = value_line
        return main_layout

    def update_value_line(self, value):
        self.value_line.setText(f"{str(value)} MiB")
        self.logger.info(f"updating value_line - {value}")

    def update_slider_value(self):
        try:
            new_value = int(self.value_line.text().replace(" MiB", ""))
            new_value = max(
                self.memory_slider.minimum(),
                min(new_value, self.memory_slider.maximum()),
            )
            self.memory_slider.setValue(new_value)
            self.value = new_value
            self.value_line.setText(f"{self.value} MiB")
            self.logger.info(f"updating memory_slider - {self.value}")
        except ValueError:
            self.value_line.setText(f"{self.memory_slider.value()} MiB")

    def update_resolution_value(self):
        new_width = self.width_line.text().strip()
        new_height = self.height_line.text().strip()

        self.parent.set_resolution(new_width, new_height)

        self.logger.info(f"Updated resolution to {new_width} x {new_height}")
