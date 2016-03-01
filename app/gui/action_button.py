from PyQt5.QtWidgets import QFrame, QGraphicsDropShadowEffect


class ActionButton(QFrame):

    def __init__(self, main_window):
        super().__init__(main_window)

        self.main_window = main_window
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        self.setGraphicsEffect(shadow)

        self.move(1300, 210)
