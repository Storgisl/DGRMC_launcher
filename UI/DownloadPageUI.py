from PySide6.QtWidgets import (
    QVBoxLayout,
    QFileDialog,
    QLabel,
    QSizePolicy,
)
from PySide6.QtGui import QMovie
from PySide6.QtCore import Q_ARG, QThread, Qt, QMetaObject, Slot

from Factory import LoggerFactory

from .BasePageUI import BasePageUI

from icecream import ic


class DownloadPageUI(BasePageUI):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.logger = LoggerFactory("UI").get_logger()
        self.setup_ui()
        self.logger.info("DownloadUI init")

    def setup_ui(self):

        self.loading_gif_label = QLabel(self.parent)
        self.loading_gif = QMovie("assets/loading2-40.gif")
        self.loading_gif_label.setMovie(self.loading_gif)
        self.loading_gif_label.setFixedSize(40, 40)
        self.loading_gif.setSpeed(50)  # Slow down animation
        self.loading_gif.setCacheMode(QMovie.CacheAll)

        layout = self.ui_factory.create_layout(
            layout_type=QVBoxLayout,
            spacing=20,
            elements=[
                {
                    "widget": self.create_navbar_frame(),
                    "spacing": 110,
                },
                {"layout": self.create_main_layout(), "stretch": True},
                {
                    "layout": self.create_footer_layout(),
                },
            ],
        )
        self.parent.setLayout(layout)

    def create_main_layout(self):
        text_image_label = self.ui_factory.create_label(pixmap="assets/Text.png")

        self.label = self.ui_factory.create_label(
            text=(
                "Please, choose installation folder"
                if not self.parent.mc_dir
                else self.parent.mc_dir
            ),
            stylesheet="""
            QLabel {
                font-size: 14px;
                color: #7247CB;
                font-weight: 200;
            }
        """,
            font=self.light_font,
        )

        self.choose_dir_button = self.ui_factory.create_button(
            text="Choose",
            stylesheet="""
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
        """,
            font=self.regular_font,
            cursor=True,
            on_click_callback=self.choose_directory,
        )

        self.install_mc_button = self.ui_factory.create_button(
            text="Install",
            stylesheet="""
            QPushButton {
                background-color: #503684;
                color: #F0F0F0;
                font-size: 14px;
                font-weight: 400;
                border-radius: 8px;
                min-height: 30px;
                max-height: 30px;
                min-width: 150px;
                max-width: 150px;
            }
            QPushButton:hover {
                background-color: #7247CB;
            }
        """,
            font=self.regular_font,
            cursor=True,
            on_click_callback=self.start_installation,
        )

        self.frame_layout = self.ui_factory.create_layout(
            layout_type=QVBoxLayout,
            alignment=Qt.AlignTop,
            spacing=10,
            elements=[
                {
                    "widget": text_image_label,
                    "alignment": Qt.AlignTop | Qt.AlignHCenter,
                    "spacer": (0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed),
                },
                {"widget": self.label, "alignment": Qt.AlignTop | Qt.AlignHCenter},
                {
                    "widget": self.choose_dir_button,
                    "alignment": Qt.AlignTop | Qt.AlignHCenter,
                },
                {
                    "widget": self.install_mc_button,
                    "alignment": Qt.AlignTop | Qt.AlignHCenter,
                },
            ],
        )

        frame = self.ui_factory.create_frame(
            self.frame_layout,
            fixed_size=(427, 200),
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
        return main_layout

    def choose_directory(self) -> None:
        mc_dir = QFileDialog.getExistingDirectory(
            self.parent, "Choose Minecraft Directory"
        )
        if mc_dir:
            self.mc_dir = mc_dir
            print(f"Selected directory: {mc_dir}")
            self.parent.data_manip.save_user_data(
                new_data={"mc_dir": mc_dir},
                directory=self.parent.config_dir,
                json_file=self.parent.user_options_json,
            )
            self.label.setText(f"{mc_dir}")
        else:
            self.label.setText("No directory chosen!")

    def start_installation(self) -> None:
        from Utils import InstallWorker

        self.frame_layout.removeWidget(self.choose_dir_button)
        self.frame_layout.removeWidget(self.install_mc_button)
        self.install_mc_button.deleteLater()
        self.choose_dir_button.deleteLater()

        self.label.setText("Starting installation...")

        self.progress_bar = self.ui_factory.create_progress_bar(
            range=(0, 100),
            fixed_size=(385, 5),
            stylesheet="""
            QProgressBar {
                border: none;
                border-radius: 5px;
                text-align: center;
                background-color: #503684;
                color: rgba(0, 0, 0, 0);
            }
            QProgressBar::chunk {
                background-color: #7247CB;
                border: none;
                border-radius: 5px;
            }
        """,
        )

        self.frame_layout.addWidget(
            self.loading_gif_label, alignment=Qt.AlignTop | Qt.AlignHCenter
        )
        self.frame_layout.addWidget(
            self.progress_bar, alignment=Qt.AlignTop | Qt.AlignHCenter
        )
        self._cancelled = False
        self.loading_gif.start()

        self.thread = QThread()
        self.worker = InstallWorker(
            mc_dir=self.parent.mc_dir, base_url=self.parent.base_url
        )
        self.worker.moveToThread(self.thread)

        # Connect signals and slots
        self.thread.started.connect(self.worker.install_mc)
        self.worker.set_status_signal.connect(self.update_status)
        self.worker.set_progress_signal.connect(self.update_progress)
        self.worker.set_max_signal.connect(self.set_progress_max)

        # Handle worker and thread cleanup
        def cleanup():
            """Clean up resources after installation completes or is cancelled."""
            try:
                self.worker.set_status_signal.disconnect()
                self.worker.set_progress_signal.disconnect()
                self.worker.set_max_signal.disconnect()
            except RuntimeError:
                pass  # Signals already disconnected

            self.thread.quit()
            self.thread.wait()
            self.thread.deleteLater()
            self.worker.deleteLater()

            # Stop the loading GIF and clean up
            self.stop_gif()
            # Re-enable the UI
            self.parent.setDisabled(False)
            self.parent.download_complete.emit()

        self.worker.finished.connect(cleanup)

        # Add a "Cancel" button
        # self.cancel_button = self.ui_factory.create_button(
        #     text="Cancel",
        #     stylesheet="""
        #     QPushButton {
        #         background-color: #503684;
        #         color: #F0F0F0;
        #         font-size: 14px;
        #         border-radius: 8px;
        #         min-height: 30px;
        #         max-height: 30px;
        #         min-width: 150px;
        #         max-width: 150px;
        #     }
        #     QPushButton:hover {
        #         background-color: #7247CB;
        #     }
        # """,
        #     on_click_callback=self.cancel_installation,
        #     emit_signal=self.parent.emit_signal,
        #     signal_args=[self.parent.go_to_download_page],
        # )
        # self.frame_layout.addWidget(
        #     self.cancel_button, alignment=Qt.AlignTop | Qt.AlignHCenter
        # )

        # Start the thread
        self.thread.start()

    @Slot(str)
    def update_status(self, status: str) -> None:
        QMetaObject.invokeMethod(
            self.label, "setText", Qt.QueuedConnection, Q_ARG(str, status)
        )

    @Slot(int)
    def update_progress(self, progress: int) -> None:
        ic(f"update_progress - {progress}")
        QMetaObject.invokeMethod(
            self.progress_bar, "setValue", Qt.QueuedConnection, Q_ARG(int, progress)
        )

    @Slot(int)
    def set_progress_max(self, max_value: int) -> None:
        QMetaObject.invokeMethod(
            self.progress_bar, "setMaximum", Qt.QueuedConnection, Q_ARG(int, max_value)
        )

    def stop_gif(self):
        if self.loading_gif:
            self.loading_gif.stop()
            self.loading_gif_label.setMovie(None)
            self.loading_gif.deleteLater()
            self.loading_gif = None

    # def cancel_installation(self):
    #     self.label.setText("Installation cancelled")
    #     self.thread.quit()
    #     self.thread.wait()
