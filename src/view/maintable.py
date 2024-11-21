import logging
from PyQt5 import QtWidgets, QtGui 
from PyQt5.QtCore import Qt, QSize
from view.main_side_description import MyPostContent
from model.model import MainPageContent

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

class MyTable(QtWidgets.QTableView):
    def __init__(self, parent: QtWidgets.QWidget | None = ..., parent_mainwindow:QtWidgets.QMainWindow = None) -> None:
        super(MyTable, self).__init__(parent)

        self.parent_mainwindow = parent_mainwindow
        self.important_columns = ["title", "status", "created_at", "updated_at", "owner_username", "slug"]
        self.model:QtGui.QStandardItemModel = QtGui.QStandardItemModel(0, 0)
        self.description_widget:QtWidgets.QWidget = None
        self.setModel(self.model)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        self.load_data(False)

    def load_data(self, all_columns:bool = True):
        content = MainPageContent()
        lines = content.operation()
        if len(lines) == 0:
            return

        column_names = [colname for colname in lines[0].keys()  
             if all_columns or (not all_columns and colname in self.important_columns)]

        self.model.clear()
        self.model.setRowCount(len(lines))
        self.model.setColumnCount(len(column_names))
        self.model.setHorizontalHeaderLabels([colname for colname in column_names])

        for row_no, line in enumerate(lines):
            column_number = -1
            for column_name in column_names:
                if not all_columns and column_name not in self.important_columns:
                    continue
                column_number += 1
                index = self.model.index(row_no, column_number)
                self.model.setData(index, line.get(column_name))

        self.resizeColumnsToContents()

    def mouseDoubleClickEvent(self, e: QtGui.QMouseEvent | None) -> None:
        logging.debug("double click")
        logging.debug(f"indexes {self.selectedIndexes()}")

        indexes = self.selectedIndexes()
        if len(indexes) == 1:
            index = indexes[0]
            layout = self.parent_mainwindow.centralWidget().layout()
            if self.description_widget:
                layout.removeWidget(self.description_widget)
            
            slug = index.siblingAtColumn(0).data(Qt.DisplayRole)
            user = index.siblingAtColumn(5).data(Qt.DisplayRole)
            self.description_widget = MyPostContent(self) 
            self.description_widget.setContent(user, slug)
            layout.addWidget(self.description_widget)

        return super().mouseDoubleClickEvent(e)

        
class MyToolbar(QtWidgets.QToolBar):
    def __init__(self, table:MyTable):
        super(MyToolbar, self).__init__()
        self.parent_table:MyTable = table
        self.setIconSize(QSize(24, 24))
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.act_load_data = self.addAction("Load data")
        self.act_load_data.triggered.connect(lambda: self.parent_table.load_data(False))

        self.act_load_all_data = self.addAction("Load ALL data")
        self.act_load_all_data.triggered.connect(lambda: self.parent_table.load_data())

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.addWidget(spacer)

        self.act_config = self.addAction("Config Table")
        # self.act_config.triggered.connect()