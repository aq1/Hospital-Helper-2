from PyQt5.QtWidgets import QFrame, QStackedLayout

from gui.attributes_frame import AttributesFrame


class DataWidget(QFrame):

    def __init__(self, main_window, items):

        super().__init__(main_window)

        stacked_layout = QStackedLayout()
        main_window.communication.item_selected.connect(stacked_layout.setCurrentIndex)
        self.setLayout(stacked_layout)

        for item in items:
            frame = AttributesFrame(main_window=main_window, item=item)
            stacked_layout.addWidget(frame)
