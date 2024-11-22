from PyQt5 import QtWidgets
from model.model import PostDescription

class MyPostContent(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = ...) -> None:
        super(MyPostContent, self).__init__(parent)

        self.layout:QtWidgets.QBoxLayout = QtWidgets.QVBoxLayout()
        self.text_browser = QtWidgets.QTextBrowser()
        self.text_browser.zoomIn(3)
        self.layout.addWidget(self.text_browser)
        self.setLayout(self.layout)


    def setContent(self, user:str, slug:str):
        content = PostDescription(user, slug)
        post = content.operation()
        if post:
            self.text_browser.setText(post.get("body"))
            

