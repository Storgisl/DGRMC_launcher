from PySide6.QtWidgets import (
    QLineEdit,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PySide6.QtCore import Qt

from Factory import LoggerFactory

from .BasePageUI import BasePageUI


class RegistrationPageUI(BasePageUI):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.logger = LoggerFactory("UI").get_logger()
        self.setup_ui()
        self.logger.info("RegistrationPageUI init")

    def setup_ui(self):
        layout = self.ui_factory.create_layout(
            layout_type=QVBoxLayout,
            spacing=20,
            elements=[
                {"widget": self.create_reg_navbar_frame(), "spacing": 60},
                {
                    "layout": self.create_main_layout(),
                    "stretch": True,
                },
                {"layout": self.create_footer_layout()},
            ],
        )
        self.parent.setLayout(layout)

    def create_reg_navbar_frame(self):
        logo_label = self.ui_factory.create_label(pixmap="assets/Logo.png")

        sign_in_button = self.ui_factory.create_button(
            text="Sign In",
            stylesheet="""
            QPushButton {
                background-color: transparent;
                color: #F0F0F0;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """,
            cursor=True,
            emit_signal=self.parent.emit_signal,
            signal_args=[self.parent.go_to_login],
            font=self.medium_font,
        )

        sign_up_button = self.ui_factory.create_button(
            text="Sign Up",
            stylesheet="""
            QPushButton {
                background-color: transparent;
                color: #7C58FF;
                font-size: 16px;
                border: none;
            }
        """,
            font=self.medium_font,
        )

        version_label = self.ui_factory.create_label(
            text="v2.1.1",
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
        navbar_reg_layout = self.ui_factory.create_layout(
            layout_type=QHBoxLayout,
            contents_margins=(40, 0, 40, 0),
            elements=[
                {"widget": logo_label, "alignment": Qt.AlignLeft, "spacing": 165},
                {"widget": sign_in_button, "stretch": True},
                {"widget": sign_up_button, "stretch": True},
                {"widget": version_label, "alignment": Qt.AlignCenter},
            ],
        )

        navbar_reg_frame = self.ui_factory.create_frame(
            layout=navbar_reg_layout, fixed_size=44
        )
        return navbar_reg_frame

    def create_main_layout(self):
        text_image_label = self.ui_factory.create_label(
            pixmap="assets/TextRegister.png"
        )

        nickname_label = self.ui_factory.create_label(
            text="Nickname",
            stylesheet="""
            QLabel {
                font-size: 14px;
                color: #B3A1C7;
            }
        """,
            font=self.regular_font,
        )

        self.username_text = self.ui_factory.create_line_edit(
            placeholder_text="",
            alignment=Qt.AlignCenter,
            stylesheet="""
            QLineEdit {
                background-color: #503684;
                color: #B3A1C7;
                font-size: 14px;
                border-radius: 5px;
                min-height: 30px;
                max-height: 30px;
                max-width: 360px;
                min-width: 360px;
            }
        """,
            font=self.regular_font,
        )

        password_label = self.ui_factory.create_label(
            text="Password",
            stylesheet="""
            QLabel {
                font-size: 14px;
                color: #B3A1C7;
            }
        """,
            font=self.regular_font,
        )

        self.password_text = self.ui_factory.create_line_edit(
            placeholder_text="",
            alignment=Qt.AlignCenter,
            echo_mode=QLineEdit.Password,
            stylesheet="""
            QLineEdit {
                background-color: #503684;
                color: #B3A1C7;
                font-size: 14px;
                border-radius: 5px;
                min-height: 30px;
                max-height: 30px;
                max-width: 360px;
                min-width: 360px;
            }
        """,
            font=self.regular_font,
        )

        enter_button = self.ui_factory.create_button(
            text="Register",
            stylesheet="""
            QPushButton {
                background-color: transparent;
                color: #F0F0F0;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """,
            font=self.regular_font,
            cursor=True,
            on_click_callback=self.parent.handle_registration,
        )

        frame_layout = self.ui_factory.create_layout(
            layout_type=QVBoxLayout,
            alignment=Qt.AlignCenter,
            elements=[
                {
                    "widget": text_image_label,
                    "alignment": Qt.AlignTop | Qt.AlignHCenter,
                    "spacer": (20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding),
                },
                {"widget": nickname_label, "alignment": Qt.AlignLeft | Qt.AlignHCenter},
                {
                    "widget": self.username_text,
                    "alignment": Qt.AlignTop | Qt.AlignHCenter,
                },
                {"widget": password_label, "alignment": Qt.AlignLeft | Qt.AlignHCenter},
                {
                    "widget": self.password_text,
                    "alignment": Qt.AlignTop | Qt.AlignHCenter,
                    "spacer": (20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding),
                },
                {
                    "widget": enter_button,
                    "alignment": Qt.AlignTop | Qt.AlignHCenter,
                    "spacer": (20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding),
                },
            ],
        )

        frame = self.ui_factory.create_frame(
            layout=frame_layout,
            fixed_size=(440, 300),
            stylesheet="""
            QFrame {
                background-color: #412483;
                border-radius: 10px;
            }
        """,
        )

        main_layout = self.ui_factory.create_layout(
            layout_type=QVBoxLayout,
            alignment=Qt.AlignCenter,
            elements=[{"widget": frame, "alignment": Qt.AlignCenter}],
        )

        main_layout.addWidget(frame, alignment=Qt.AlignCenter)
        return main_layout
