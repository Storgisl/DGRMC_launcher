from logging import addLevelName
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QFrame,
    QHBoxLayout,
)
from PySide6.QtGui import QPixmap, QFont, QFontDatabase
from PySide6.QtCore import Qt

from Factory import LoggerFactory, UIFactory


class BasePageUI:
    def __init__(self):
        self.logger = LoggerFactory("UI").get_logger()
        self.ui_factory = UIFactory()
        self.logger.info("BasePageUI init")
        self.init_ui()

    def init_ui(self):
        self.init_fonts()

    def init_fonts(self):
        self.regular_font_id = QFontDatabase.addApplicationFont(
            "assets/Heebo-Regular.ttf"
        )
        self.medium_font_id = QFontDatabase.addApplicationFont(
            "assets/Heebo-Medium.ttf"
        )
        self.light_font_id = QFontDatabase.addApplicationFont("assets/Heebo-Light.ttf")
        self.bold_font_id = QFontDatabase.addApplicationFont("assets/Heebo-Bold.ttf")
        self.extra_light_font_id = QFontDatabase.addApplicationFont(
            "assets/Heebo-ExtraLight.ttf"
        )
        if self.regular_font_id == -1:
            print("Ошибка: Не удалось загрузить Heebo-Regular.ttf")
        if self.medium_font_id == -1:
            print("Ошибка: Не удалось загрузить Heebo-Medium.ttf")
        if self.light_font_id == -1:
            print("Ошибка: Не удалось загрузить Heebo-Light.ttf")
        if self.bold_font_id == -1:
            print("Ошибка: Не удалось загрузить Heebo-Bold.ttf")
        if self.extra_light_font_id == -1:
            print("Ошибка: Не удалось загрузить Heebo-ExtraLight.ttf")

        self.regular_font = QFont(
            QFontDatabase.applicationFontFamilies(self.regular_font_id)[0]
        )
        self.medium_font = QFont(
            QFontDatabase.applicationFontFamilies(self.medium_font_id)[0]
        )
        self.light_font = QFont(
            QFontDatabase.applicationFontFamilies(self.light_font_id)[0]
        )
        self.bold_font = QFont(
            QFontDatabase.applicationFontFamilies(self.bold_font_id)[0]
        )
        self.extra_light_font = QFont(
            QFontDatabase.applicationFontFamilies(self.extra_light_font_id)[0]
        )

    def create_navbar_frame(self):
        logo_label = self.ui_factory.create_label(pixmap="assets/Logo.png")

        version_label = self.ui_factory.create_label(
            text="V 1.0",
            stylesheet="font-size: 16px; color: #F0F0F0;",
            font=self.medium_font,
        )

        navbar_layout = self.ui_factory.create_layout(
            layout_type=QHBoxLayout,
            elements=[
                {"widget": logo_label, "alignment": Qt.AlignmentFlag.AlignLeft},
                {"widget": version_label, "alignment": Qt.AlignmentFlag.AlignRight},
            ],
        )

        navbar_frame = self.ui_factory.create_frame(layout=navbar_layout, fixed_size=44)

        self.logger.info("BasePage UI navbar frame complete")
        return navbar_frame

    def create_footer_layout(self):
        made_by_label = self.ui_factory.create_label(
            text="Made by Kivaari",
            stylesheet="""
            QLabel {
                font-size: 14px;
                font-weight: 200;
                color: rgba(255, 255, 255, 20);
            }
        """,
            font=self.extra_light_font,
        )

        footer_layout = self.ui_factory.create_layout(
            layout_type=QHBoxLayout,
            contents_margins=(40, 0, 40, 0),
            elements=[{"widget": made_by_label, "alignment": Qt.AlignCenter}],
        )

        self.logger.info("BasePage UI footer frame complete")
        return footer_layout
