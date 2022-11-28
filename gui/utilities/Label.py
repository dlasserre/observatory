from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


class Label(QLabel):
    """ LABEL """

    def __init__(self, text: str = None, style: str = None):
        super().__init__()
        if text is not None:
            self.setText(text)
        if style is not None:
            self.setStyleSheet(style)
