import sys
import os

from PySide6.QtWidgets import QVBoxLayout, QPushButton, QFileDialog, QLabel, QVBoxLayout, QFrame, QSpacerItem, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Signal, Qt
from icecream import ic

from .Page import Page
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manip_data.save_user_data import save_user_data


class DownloadPage(Page):
    go_to_install = Signal()

    def __init__(self, stacked_widget):
        super().__init__()
        self.setObjectName("download_page")
        self.stacked_widget = stacked_widget
        self.init_ui()

    def init_ui(self):
        # Центральная часть страницы
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Фрейм с размером 427x418
        frame = QFrame(self)
        frame.setFixedSize(427, 418)
        frame.setStyleSheet("""
            QFrame {
                background-color: #412483;
                border-radius: 10px;
            }
        """)
        frame_layout = QVBoxLayout()
        frame_layout.setAlignment(Qt.AlignTop)  # Выравниваем элементы по верхней части фрейма
        frame_layout.setSpacing(10)  # Устанавливаем меньший отступ между элементами
        
        # Картинка
        text_image_label = QLabel(self)
        text_image_pixmap = QPixmap("assets/Text.png")
        text_image_label.setPixmap(text_image_pixmap)
        frame_layout.addWidget(text_image_label, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        # Добавляем небольшой отступ между картинкой и надписью
        top_spacer = QSpacerItem(0, 110, QSizePolicy.Minimum, QSizePolicy.Fixed)
        frame_layout.addItem(top_spacer)
        
        label = QLabel("Please, choose installation folder", self)
        label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #7247CB;
            }
        """)
        label.setFont(self.light_font)
        frame_layout.addWidget(label, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        choose_dir_button = QPushButton("Choose", self)
        choose_dir_button.setStyleSheet("""
            QPushButton {
                background-color: #503684;
                color: #F0F0F0;
                font-size: 14px;
                border-radius: 8px;
                min-height: 30px;
                max-height: 30px;
                min-width: 150px;
                max-width: 150px;
            }
            QPushButton:hover {
                background-color: #7247CB;
            }
        """)
        choose_dir_button.setFont(self.regular_font)
        choose_dir_button.setCursor(Qt.PointingHandCursor)
        choose_dir_button.clicked.connect(self.choose_directory)
        frame_layout.addWidget(choose_dir_button, alignment=Qt.AlignTop | Qt.AlignHCenter)
        
        frame.setLayout(frame_layout)
        main_layout.addWidget(frame, alignment=Qt.AlignCenter)
        
        # Объединяем все части в один макет
        layout = QVBoxLayout()
        layout.addSpacing(20)  # Добавляем отступ сверху для navbar
        layout.addWidget(self.navbar_frame)
        layout.addSpacing(20)  # Добавляем отступ после navbar
        layout.addLayout(main_layout)
        layout.addStretch()
        layout.addLayout(self.footer_layout)
        self.setLayout(layout)

    def choose_directory(self) -> None:
        mc_dir = QFileDialog.getExistingDirectory(self, "Choose Minecraft Directory")
        if mc_dir:
            self.mc_dir = mc_dir
            print(f"Selected directory: {mc_dir}")
            save_user_data(
                new_data={"mc_dir": mc_dir},
                directory=self.config_dir,
                json_file=self.user_data_json
            )
            self.go_to_install.emit()
        else:
            print("No directory chosen!")

    def check_dirs(self, directory: str, folders: list) -> bool:
        try:
            contents = os.listdir(directory)
            for folder in folders:
                if folder not in contents:
                    ic(f"folder '{folder}' is missing")
                    return False
            return True
        except FileNotFoundError:
            print(f"Directory '{directory}' not found.")
            return False

    def download_status(self) -> bool:
        dgrmc_dir = os.path.join(self.mc_dir, "DGRMClauncher")

        required_folders = ["assets", "libraries", "runtime", "versions"]
        if self.check_dirs(directory=dgrmc_dir, folders=required_folders):
            ic(dgrmc_dir)
            return True
        else:
            if (dgrmc_dir is False and self.username_var not in ("", None) and
                    self.password_var not in ("", None)):
                return True
            else:
                ic(f"Missing required folders in {self.username_var, self.password_var,dgrmc_dir}")
                return False
