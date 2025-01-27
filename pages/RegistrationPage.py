from PySide6.QtWidgets import QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy, QCheckBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manip_data import save_user_data, load_user_data
from .Page import Page

class RegistrationPage(Page):
    registration_complete = Signal()
    go_to_login = Signal()
    
    def __init__(self, stacked_widget):
        super().__init__()
        self.setObjectName("registration_page")
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        # Navbar
        navbar_layout = QHBoxLayout()
        navbar_layout.setContentsMargins(40, 0, 40, 0)

        logo_label = QLabel(self)
        logo_pixmap = QPixmap("assets/Logo.png")
        logo_label.setPixmap(logo_pixmap)
        navbar_layout.addWidget(logo_label, alignment=Qt.AlignLeft)

        navbar_layout.addSpacing(165)

        # Кнопка Sign in
        sign_in_button = QPushButton("Sign In", self)
        sign_in_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #F0F0F0;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        sign_in_button.setCursor(Qt.PointingHandCursor)
        sign_in_button.clicked.connect(self.show_sign_in_page)
        sign_in_button.setFont(self.medium_font)
        navbar_layout.addWidget(sign_in_button)

        # Добавляем растяжку для равномерного распределения элементов
        navbar_layout.addStretch()

        # Кнопка Sign Up
        sign_up_button = QPushButton("Sign Up", self)
        sign_up_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #7C58FF;
                font-size: 16px;
                border: none;
            }
        """)
        sign_up_button.setFont(self.medium_font)
        navbar_layout.addWidget(sign_up_button)

        # Добавляем растяжку для равномерного распределения элементов
        navbar_layout.addStretch()

        version_label = QLabel("v2.1.1", self)
        version_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #F0F0F0;
                padding: 0;
                vertical-align: middle;
            }
        """)
        version_label.setFont(self.medium_font)
        navbar_layout.addWidget(version_label, alignment=Qt.AlignCenter)

        # Создаем рамку для navbar
        navbar_frame = QFrame(self)
        navbar_frame.setLayout(navbar_layout)
        navbar_frame.setFixedHeight(44)

        # Центральная часть страницы
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Фрейм с размером 440x300
        frame = QFrame(self)
        frame.setFixedSize(440, 300)
        frame.setStyleSheet("""
            QFrame {
                background-color: #412483;
                border-radius: 10px;
            }
        """)
        frame_layout = QVBoxLayout()
        frame_layout.setAlignment(Qt.AlignCenter)

        # Картинка
        text_image_label = QLabel(self)
        text_image_pixmap = QPixmap("assets/TextRegister.png")
        text_image_label.setPixmap(text_image_pixmap)
        frame_layout.addWidget(text_image_label, alignment=Qt.AlignTop | Qt.AlignHCenter)

        # Добавляем растяжку между картинкой и полями ввода
        top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        frame_layout.addItem(top_spacer)

        # Надпись Nickname
        nickname_label = QLabel("Nickname", self)
        nickname_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #B3A1C7;
            }
        """)
        nickname_label.setFont(self.regular_font)
        frame_layout.addWidget(nickname_label, alignment=Qt.AlignLeft | Qt.AlignHCenter)

        # Поле для ввода никнейма
        self.username_text = QLineEdit(self)
        self.username_text.setPlaceholderText("")
        self.username_text.setAlignment(Qt.AlignCenter)
        self.username_text.setStyleSheet("""
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
        """)
        self.username_text.setFont(self.regular_font)
        frame_layout.addWidget(self.username_text, alignment=Qt.AlignTop | Qt.AlignHCenter)

        # Надпись Password
        password_label = QLabel("Password", self)
        password_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #B3A1C7;
            }
        """)
        password_label.setFont(self.regular_font)
        frame_layout.addWidget(password_label, alignment=Qt.AlignLeft | Qt.AlignHCenter)

        # Поле для ввода пароля
        self.password_text = QLineEdit(self)
        self.password_text.setPlaceholderText("")
        self.password_text.setAlignment(Qt.AlignCenter)
        self.password_text.setEchoMode(QLineEdit.Password)
        self.password_text.setStyleSheet("""
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
        """)
        self.password_text.setFont(self.regular_font)
        frame_layout.addWidget(self.password_text, alignment=Qt.AlignTop | Qt.AlignHCenter)

        # Добавляем растяжку между картинкой и полями ввода
        top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        frame_layout.addItem(top_spacer)

        # Кнопка Enter
        enter_button = QPushButton("Register", self)
        enter_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #F0F0F0;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        enter_button.setFont(self.regular_font)
        enter_button.setCursor(Qt.PointingHandCursor)
        enter_button.clicked.connect(self.handle_registration)
        frame_layout.addWidget(enter_button, alignment=Qt.AlignTop | Qt.AlignHCenter)

        # Добавляем растяжку между картинкой и полями ввода
        top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        frame_layout.addItem(top_spacer)

        frame.setLayout(frame_layout)
        main_layout.addWidget(frame, alignment=Qt.AlignCenter)

        # Объединяем все части в один макет
        layout = QVBoxLayout()
        layout.addSpacing(20)
        layout.addWidget(navbar_frame)
        layout.addSpacing(60)
        layout.addLayout(main_layout)
        layout.addStretch()
        layout.addLayout(self.footer_layout)
        self.setLayout(layout)

    def handle_registration(self) -> None:
        username = self.username_text.text()
        password = self.password_text.text()
        # Проверка данных для регистрации
        if username and password:
            print(f"Регистрация прошла успешно: {username}")
            self.user_data = {"username": username,
                              "password": password
                             }
            save_user_data(
                new_data=self.user_data,
                directory=self.config_dir,
                json_file=self.user_data_json
            )
            self.registration_complete.emit()
        else:
            self.show_error("Заполните все поля.")

    def user_status(self) -> bool:
        self.user_data = load_user_data(
            directory=self.config_dir,
            json_file=self.user_data_json
        )
        self.username_var = self.user_data.get("username", "")
        self.password_var = self.user_data.get("password", "")
        if (self.username_var not in ("", None)
                and self.password_var not in ("", None)):
            return True
        else:
            return False

    def show_error(self, message: str) -> None:
        if not self.error_label:
            self.error_label = QLabel()
            self.error_label.setStyleSheet("color: red;")
            self.layout().addWidget(self.error_label)
        self.error_label.setText(message)

    def show_sign_in_page(self):
        self.go_to_login.emit()