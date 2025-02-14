from PySide6.QtGui import QMovie, QPixmap
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QLabel,
    QSizePolicy,
    QSlider,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QLayout,
    QSpacerItem,
)
from PySide6.QtCore import Qt, QSize
from typing import Optional, Tuple, List, Union, Dict

from icecream import ic


class UIFactory:
    @staticmethod
    def create_button(
        text=None,
        stylesheet=None,
        font=None,
        cursor=False,
        emit_signal=None,
        on_click_callback=None,
        callback_args=None,
        callback_kwargs=None,
        signal_args=None,
    ) -> QPushButton:
        button = QPushButton(text) if text else QPushButton()

        if stylesheet:
            button.setStyleSheet(stylesheet)
        if font:
            button.setFont(font)
        if cursor:
            button.setCursor(Qt.PointingHandCursor)

        callback_args = callback_args or []
        callback_kwargs = callback_kwargs or {}
        signal_args = signal_args or []

        if on_click_callback:
            button.clicked.connect(
                lambda: on_click_callback(*callback_args, **callback_kwargs)
            )

        if emit_signal:
            ic(f"Connecting signal:  with args {signal_args}")
            button.clicked.connect(lambda: emit_signal(*signal_args))

        return button

    @staticmethod
    def create_label(
        text=None, pixmap=None, stylesheet=None, font=None, movie=None, fixed_size=None
    ) -> QLabel:
        label = QLabel(text) if text else QLabel()

        if pixmap:
            label.setPixmap(QPixmap(pixmap))

        if fixed_size:
            if isinstance(fixed_size, tuple) and len(fixed_size) == 2:
                label.setFixedSize(*fixed_size)
            elif isinstance(fixed_size, QSize):
                label.setFixedSize(fixed_size)
            else:
                ic(f"ERROR: Invalid fixed_size argument: {fixed_size}")

        if movie:
            label.setMovie(QMovie(movie))

        if stylesheet:
            label.setStyleSheet(stylesheet)

        if font:
            label.setFont(font)
        return label

    @staticmethod
    def create_layout(
        layout_type: Union[QVBoxLayout, QHBoxLayout],
        alignment: Optional[Qt.AlignmentFlag] = None,
        contents_margins: Optional[Tuple[int, int, int, int]] = None,
        spacing: Optional[int] = None,
        stretch: bool = False,
        spacer: Tuple[int, QSizePolicy] = None,
        *,
        elements: Optional[
            List[
                Dict[
                    str,
                    Union[
                        QWidget,
                        QLayout,
                        Qt.AlignmentFlag,
                        QSizePolicy,
                        int,
                        bool,
                        Tuple,
                    ],
                ]
            ]
        ] = None,
    ) -> QLayout:
        """
        Creates a layout of the given type and populates it with the specified elements.
        """
        layout = layout_type()

        if contents_margins:
            layout.setContentsMargins(*contents_margins)

        if alignment:
            layout.setAlignment(alignment)

        if spacing:
            layout.addSpacing(spacing)

        if stretch:
            layout.addStretch(stretch)

        if spacer:
            layout.addItem(QSpacerItem(*spacer))

        if elements:
            for element in elements:
                if not isinstance(element, dict):
                    raise TypeError(
                        f"Expected a dictionary in elements list, but got {type(element).__name__}: {element}"
                    )

                widget = element.get("widget")
                sub_layout = element.get("layout")
                element_alignment = element.get("alignment")

                if widget:
                    if element_alignment:
                        layout.addWidget(widget, alignment=element_alignment)
                    else:
                        layout.addWidget(widget)

                    if "spacing" in element:
                        layout.addSpacing(element["spacing"])

                    if "stretch" in element:
                        layout.addStretch(element["stretch"])

                if sub_layout:
                    if isinstance(sub_layout, QLayout):
                        if element_alignment:
                            layout.addLayout(sub_layout, alignment=element_alignment)
                        else:
                            layout.addLayout(sub_layout)

                    if "spacing" in element:
                        layout.addSpacing(element["spacing"])

                    if "stretch" in element:
                        layout.addStretch(element["stretch"])

                if "spacer" in element:
                    spacer_data = element["spacer"]
                    if isinstance(spacer_data, tuple) and len(spacer_data) == 4:
                        layout.addItem(QSpacerItem(*spacer_data))
                    else:
                        raise TypeError(f"Invalid spacer format: {spacer_data}")

        return layout

    @staticmethod
    def create_frame(layout=None, fixed_size=None, stylesheet=None) -> QFrame:
        frame = QFrame()
        if layout:
            frame.setLayout(layout)
        if fixed_size:
            if isinstance(fixed_size, tuple) and len(fixed_size) == 2:
                frame.setFixedSize(*fixed_size)
            elif isinstance(fixed_size, QSize):
                frame.setFixedSize(fixed_size)
            else:
                ic(f"ERROR: Invalid fixed_size argument: {fixed_size}")
        if stylesheet:
            frame.setStyleSheet(stylesheet)
        return frame

    @staticmethod
    def create_slider(
        min_value,
        max_value,
        value,
        step,
        stylesheet=None,
        alignment=None,
        on_value_changed=None,
    ) -> QSlider:
        slider = QSlider(alignment) if alignment else QSlider()

        slider.setMinimum(min_value)
        slider.setMaximum(max_value)
        slider.setValue(int(value))
        slider.setSingleStep(step)
        if stylesheet:
            slider.setStyleSheet(stylesheet)

        if on_value_changed:
            slider.valueChanged.connect(on_value_changed)

        return slider

    @staticmethod
    def create_line_edit(
        text=None,
        placeholder_text=None,
        alignment=None,
        stylesheet=None,
        font=None,
        on_editing_finished=None,
        echo_mode=None,
    ) -> QLineEdit:
        line_edit = QLineEdit(text) if text else QLineEdit()

        if placeholder_text:
            line_edit.setPlaceholderText(placeholder_text)

        if alignment:
            line_edit.setAlignment(alignment)
        if echo_mode:
            line_edit.setEchoMode(echo_mode)
        if stylesheet:
            line_edit.setStyleSheet(stylesheet)

        if font:
            line_edit.setFont(font)

        if on_editing_finished:
            line_edit.editingFinished.connect(on_editing_finished)

        return line_edit

    @staticmethod
    def create_checkbox(text=None, stylesheet=None, on_state_change=None) -> QCheckBox:
        checkbox = QCheckBox(text) if text else QCheckBox()
        if stylesheet:
            checkbox.setStyleSheet(stylesheet)
        if on_state_change:
            checkbox.stateChanged.connect(on_state_change)
        return checkbox

    @staticmethod
    def create_progress_bar(
        range=None, fixed_size=None, stylesheet=None
    ) -> QProgressBar:
        progress_bar = QProgressBar()
        if isinstance(range, Tuple) and len(range) == 2:
            progress_bar.setRange(*range)

        if fixed_size:
            if isinstance(fixed_size, tuple) and len(fixed_size) == 2:
                progress_bar.setFixedSize(*fixed_size)
            elif isinstance(fixed_size, QSize):
                progress_bar.setFixedSize(fixed_size)
            else:
                ic(f"ERROR: Invalid fixed_size argument: {fixed_size}")
        if stylesheet:
            progress_bar.setStyleSheet(stylesheet)
        return progress_bar
