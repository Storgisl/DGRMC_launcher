from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal
from .Page import Page

class HomePage(Page):
    go_to_account = Signal()

    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        # Центральная часть страницы
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)  # Центрируем элементы

        main_image_label = QLabel(self)
        main_image_pixmap = QPixmap("assets/Main.png")
        main_image_label.setPixmap(main_image_pixmap)
        main_layout.addWidget(main_image_label, alignment=Qt.AlignCenter)

        top_spacer = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        main_layout.addItem(top_spacer)

        text_image_label = QLabel(self)
        text_image_pixmap = QPixmap("assets/Text.png")
        text_image_label.setPixmap(text_image_pixmap)
        main_layout.addWidget(text_image_label, alignment=Qt.AlignCenter)

        top_spacer = QSpacerItem(5, 30, QSizePolicy.Minimum, QSizePolicy.Fixed)
        main_layout.addItem(top_spacer)

        start_button = QPushButton("Start Journey", self)
        start_button.setStyleSheet("""
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
        """)
        start_button.setFont(self.bold_font)
        start_button.setCursor(Qt.PointingHandCursor)
        start_button.clicked.connect(self.go_to_account_page)
        main_layout.addWidget(start_button, alignment=Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addSpacing(20)
        layout.addWidget(self.navbar_frame)
        layout.addSpacing(60)
        layout.addLayout(main_layout)
        layout.addStretch()
        layout.addLayout(self.footer_layout)
        self.setLayout(layout)

    def go_to_account_page(self):
        self.go_to_account.emit()