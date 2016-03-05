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

        self.main_window = main_window
        self.item = item
        self.inputs = []

        hbox = QHBoxLayout()
        self.setLayout(hbox)
        hbox.setSpacing(0)
        hbox.addSpacing(25)

        rows = 5
        for i, arg_name in enumerate(item):
            if i % rows == 0:
                try:
                    vbox.addStretch(10)
                except NameError:
                    pass
                vbox = QVBoxLayout()
                vbox.addSpacing(main_window.TOP_MARGIN)
                vbox.setSpacing(0)
                vbox.setContentsMargins(0, 0, 0, 0)

                hbox.addLayout(vbox)

            self.inputs.append(InputWidget(self, arg_name))
            vbox.addWidget(self.inputs[-1])

        try:
            vbox.addStretch()
        except NameError:
            pass

        hbox.addStretch(100)

    def input_changed(self, label, value):
        self.item.set(label, value)
        self.item.calculate()

        for each in self.inputs:
            if label != each.label_text:
                each.set_value(self.item[each.label_text])

        self.main_window.input_changed(self.item)
