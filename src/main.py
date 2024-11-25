import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize
from view.maintable import MyTableWidget, MyToolbar


def main():
    new_app = QApplication([])
    new_app.setStyle("Fusion")

    window_main = QMainWindow()
    window_main.setMinimumSize(800, 600)
    window_main.resize(QSize(1200, 800))

    layout = QVBoxLayout()
    container = QWidget(window_main)
    container.setLayout(layout)

    table_cont = MyTableWidget(window_main)
    toolbar = MyToolbar(table_cont)

    layout.addWidget(toolbar)
    layout.addWidget(table_cont)

    window_main.setCentralWidget(container)

    window_main.show()

    sys.exit(new_app.exec_())


if __name__ == "__main__":
    main()
