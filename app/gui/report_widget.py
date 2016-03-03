from PyQt5.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout


class ReportWidget(QFrame):

    def __init__(self, main_window, items, templates):

        super().__init__()

        self.main_window = main_window
        self.templates = templates

        hbox = QHBoxLayout()
        self.setLayout(hbox)

        for item in items:
            vbox = QVBoxLayout()
            hbox.addLayout(vbox)
            vbox.addWidget(QLabel(_(item.name)))
            for each in templates[item.id]:
                vbox.addWidget(QLabel(each.name))
