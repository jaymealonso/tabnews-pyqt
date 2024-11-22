import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize
from lib.improved_qtableview import ImprTableWidget
from view.maintable import MyTable, MyToolbar

def main():
    new_app = QApplication([])
    new_app.setStyle("Fusion")
    
    window_main = QMainWindow()
    window_main.setMinimumSize(800, 600)
    window_main.resize(QSize(1200,800))

    layout = QVBoxLayout()
    container = QWidget(window_main)
    container.setLayout(layout)

    # table = MyTable(window_main, window_main)
    table_cont = MyTable(window_main)
    toolbar = MyToolbar(window_main)

    layout.addWidget(toolbar)    
    # layout.addWidget(table)
    layout.addWidget(table_cont)

    window_main.setCentralWidget(container)

    window_main.show()

    sys.exit(new_app.exec_())

if __name__ == "__main__":
    main()