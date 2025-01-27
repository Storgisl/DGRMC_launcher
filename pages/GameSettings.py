import sys
import os
import shutil
import psutil
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy, QSlider, QLineEdit, QCheckBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .Page import Page

class GameSettings(Page):
    to_launcher_settings = Signal()
    delete_complete = Signal()
    go_back = Signal()

    def __init__(self, stacked_widget):
        super().__init__()
        self.setObjectName("game_settings_page")
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

        # Добавляем растяжку для равномерного распределения элементов
        navbar_layout.addSpacing(140)
        sign_in_button = QPushButton("Launcher settings", self)
        sign_in_button.setStyleSheet("""
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
        """)
        sign_in_button.setFont(self.medium_font)
        sign_in_button.clicked.connect(self.show_launcher_settings_page)
        sign_in_button.setCursor(Qt.PointingHandCursor)
        navbar_layout.addWidget(sign_in_button)

        # Добавляем растяжку для равномерного распределения элементов
        navbar_layout.addSpacing(160)
        sign_up_button = QPushButton("Game settings", self)
        sign_up_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #7C58FF;
                font-size: 16px;
                font-weight: 500;
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
                font-weight: 500;
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
        frame.setFixedSize(400, 400)
        frame.setStyleSheet("""
            QFrame {
                background-color: #412483;
                border-radius: 10px;
            }
        """)
        frame_layout = QVBoxLayout()
        frame_layout.setAlignment(Qt.AlignTop)

        inner_navbar_layout = QHBoxLayout()
        inner_navbar_layout.setAlignment(Qt.AlignLeft)

        back_button = QPushButton(self)
        back_button.setStyleSheet("""
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
        """)
        back_button.setCursor(Qt.PointingHandCursor)
        back_button.setText("back")
        back_button.setFont(self.extra_light_font)
        back_button.clicked.connect(self.go_back_to_main)
        inner_navbar_layout.addWidget(back_button)
        frame_layout.addLayout(inner_navbar_layout)

        ###########################################################

        top_spacer = QSpacerItem(0, 30, QSizePolicy.Minimum, QSizePolicy.Fixed)
        frame_layout.addItem(top_spacer)

        memory_label = QLabel("Game memory amount", self)
        memory_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #7247CB;
                font-weight: 200;
            }
        """)
        memory_label.setFont(self.extra_light_font)
        frame_layout.addWidget(memory_label, alignment=Qt.AlignCenter)

        top_spacer = QSpacerItem(0, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        frame_layout.addItem(top_spacer)

        max_ram = self.get_max_system_ram()
        memory_slider = QSlider(Qt.Horizontal)
        memory_slider.setMinimum(2048)
        memory_slider.setMaximum(max_ram)
        memory_slider.setValue(2048)
        memory_slider.setSingleStep(512)
        memory_slider.setStyleSheet("""
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
        """)
        memory_slider.valueChanged.connect(self.update_value_line)
        frame_layout.addWidget(memory_slider, alignment=Qt.AlignCenter)

        top_spacer = QSpacerItem(0, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        frame_layout.addItem(top_spacer)

        labels_layout = QHBoxLayout()
        labels_layout.setContentsMargins(17, 0, 17, 0)
        labels_layout.setAlignment(Qt.AlignCenter)

        label1 = QLabel("2048")
        label1.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #7247CB;
                font-weight: 200;
            }
        """)
        label1.setFont(self.extra_light_font)
        labels_layout.addWidget(label1)

        labels_layout.addStretch()

        value_line = QLineEdit(self)
        value_line.setPlaceholderText(f"{str(memory_slider.value())} MiB")
        value_line.setAlignment(Qt.AlignCenter)
        value_line.setStyleSheet("""
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
        """)
        value_line.setFont(self.light_font)
        value_line.editingFinished.connect(self.update_slider_value)
        labels_layout.addWidget(value_line)

        labels_layout.addStretch()

        label2 = QLabel(f"{max_ram}")
        label2.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #7247CB;
                font-weight: 200;
            }
        """)
        label2.setFont(self.extra_light_font)
        labels_layout.addWidget(label2)
        frame_layout.addLayout(labels_layout)

        top_spacer = QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        frame_layout.addItem(top_spacer)

        ##########################################

        resolution_label = QLabel("Window resolution", self)
        resolution_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #7247CB;
                font-weight: 200;
            }
        """)
        resolution_label.setFont(self.extra_light_font)
        frame_layout.addWidget(resolution_label, alignment=Qt.AlignCenter)

        top_spacer = QSpacerItem(0, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        frame_layout.addItem(top_spacer)

        resolution_layout = QHBoxLayout()
        resolution_layout.setContentsMargins(17, 0, 17, 0)
        resolution_layout.setAlignment(Qt.AlignCenter)

        width_line = QLineEdit(self)
        width_line.setPlaceholderText("1920")
        width_line.setAlignment(Qt.AlignCenter)
        width_line.setStyleSheet("""
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
        """)
        width_line.setFont(self.regular_font)
        resolution_layout.addWidget(width_line)

        x_label = QLabel("x")
        x_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #7247CB;
                font-weight: 200;
            }
        """)
        x_label.setFont(self.extra_light_font)
        resolution_layout.addWidget(x_label)

        height_line = QLineEdit(self)
        height_line.setPlaceholderText("1080")
        height_line.setAlignment(Qt.AlignCenter)
        height_line.setStyleSheet("""
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
        """)
        height_line.setFont(self.regular_font)
        resolution_layout.addWidget(height_line)

        resolution_layout.addStretch()

        fs_label = QLabel("Fullscreen mode")
        fs_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #7247CB;
                font-weight: 200;
            }
        """)
        fs_label.setFont(self.extra_light_font)
        resolution_layout.addWidget(fs_label)

        resolution_layout.addSpacing(0)

        checkbox = QCheckBox("", self)
        checkbox.setStyleSheet("""
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
        """)
        checkbox.stateChanged.connect(self.on_checkbox_state_changed)
        resolution_layout.addWidget(checkbox)

        frame_layout.addLayout(resolution_layout)

        top_spacer = QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        frame_layout.addItem(top_spacer)

        ##########################################

        delete_layout = QHBoxLayout()
        delete_layout.setContentsMargins(17, 0, 17, 0)
        delete_layout.setAlignment(Qt.AlignCenter)

        delete_label = QLabel("Delete minecraft")
        delete_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #7247CB;
                font-weight: 200;
            }
        """)
        delete_label.setFont(self.extra_light_font)
        delete_layout.addWidget(delete_label)

        delete_layout.addStretch()

        self.delete_line = QLineEdit(self)
        self.delete_line.setPlaceholderText('Type "delete"')
        self.delete_line.setAlignment(Qt.AlignCenter)
        self.delete_line.setStyleSheet("""
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
        """)
        self.delete_line.setFont(self.regular_font)
        delete_layout.addWidget(self.delete_line)

        delete_layout.addStretch()

        delete_button = QPushButton(self)
        delete_button.setStyleSheet("""
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
        """)
        delete_button.setCursor(Qt.PointingHandCursor)
        delete_button.clicked.connect(self.delete_mc)
        delete_layout.addWidget(delete_button)

        frame_layout.addLayout(delete_layout)

        frame.setLayout(frame_layout)
        main_layout.addWidget(frame, alignment=Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addSpacing(20)
        layout.addWidget(navbar_frame)
        layout.addSpacing(40)
        layout.addLayout(main_layout)
        layout.addStretch()
        layout.addLayout(self.footer_layout)
        self.setLayout(layout)

        # Сохраняем ссылки на объекты для последующего использования
        self.memory_slider = memory_slider
        self.value_line = value_line


    def update_value_line(self, value):
        self.value_line.setPlaceholderText(f"{str(value)} MiB")

    def get_max_system_ram(self):
        total_ram = psutil.virtual_memory().total
        return total_ram // (1024 * 1024)

    def update_slider_value(self):
        try:
            new_value = int(self.value_line.text())
            if new_value < self.memory_slider.minimum():
                new_value = self.memory_slider.minimum()
            elif new_value > self.memory_slider.maximum():
                new_value = self.memory_slider.maximum()
            self.memory_slider.setValue(new_value)
            self.value_line.setPlaceholderText(f"{str(new_value)} MiB")
        except ValueError:
            # Если введено некорректное значение, оставляем старое значение
            self.value_line.setText("")
            self.value_line.setPlaceholderText(f"{str(self.memory_slider.value())} MiB")

    def generate_jvm_arguments(self):
        pass

    def delete_mc(self):
        if self.delete_line.text().lower() == "delete":
            try:
                shutil.rmtree(os.path.join(self.mc_dir, "DGRMClauncher"))
                self.delete_complete.emit()
            except Exception as e:
                print(f"Error: {e}")
        else:
            pass

    def on_checkbox_state_changed(self, state):
        if state == Qt.Checked:
            print("Checkbox is checked")
        else:
            print("Checkbox is unchecked")

    def show_launcher_settings_page(self):
        self.to_launcher_settings.emit()

    def go_back_to_main(self):
        self.go_back.emit()