from PyQt5 import QtWidgets


class MyPostContent(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = ...) -> None:
        super(MyPostContent, self).__init__(parent)

        self.layout:QtWidgets.QBoxLayout = QtWidgets.QBoxLayout()
        self.layout.addWidget(QtWidgets.QTextBrowser)

    def setContent(self):
        pass
