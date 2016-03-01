from PyQt5.QtWidgets import QFrame, QStackedLayout

from gui.attributes_frame import AttributesFrame


class DataWidget(QFrame):

    def __init__(self, main_window, items):

        super().__init__()

        self.main_window = main_window
        self.stacked_layout = QStackedLayout()
        self.setLayout(self.stacked_layout)

        for item in items:
            frame = AttributesFrame(main_window=self, item=item)
            self.stacked_layout.addWidget(frame)

    def select_item(self, index):
        self.stacked_layout.setCurrentIndex(index)
