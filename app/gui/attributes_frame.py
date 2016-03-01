from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from gui.input_widget import InputWidget


class AttributesFrame(QWidget):
    """
    Frame represents attributes of a single item.
    Contains form layouts - labels and inputs
    """

    def __init__(self, main_window, item):
        """
        main_window: MainWindow instance
        item: CalculableObject instance
        """

        super().__init__()
        print(item)

        self.main_window = main_window
        hbox = QHBoxLayout()
        self.setLayout(hbox)
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addSpacing(25)

        rows = 5
        for i, arg_name in enumerate(item):
            if i % rows == 0:
                try:
                    vbox.addStretch(10)
                except NameError:
                    pass
                vbox = QVBoxLayout()
                vbox.setSpacing(0)
                vbox.setContentsMargins(0, 0, 0, 0)

                hbox.addLayout(vbox)

            vbox.addWidget(InputWidget(arg_name))

        try:
            vbox.addStretch()
        except NameError:
            pass

        hbox.addStretch(100)
