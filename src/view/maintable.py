import os
import logging
import json
import requests
from PyQt5 import QtWidgets, QtGui 
from PyQt5.QtCore import Qt, QSize

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

class MyTable(QtWidgets.QTableView):
    def __init__(self, parent: QtWidgets.QWidget | None = ...) -> None:
        super(MyTable, self).__init__(parent)

        self.important_columns = ["title", "status", "created_at", "updated_at", "owner_username"]
        self.model:QtGui.QStandardItemModel = QtGui.QStandardItemModel(0, 0)
        self.setModel(self.model)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        self.load_data(False)

    def load_data(self, all_columns:bool = True):
        # response = requests.get("../mockdata/content.json")
        # response = requests.get("https://www.tabnews.com.br/api/v1/contents?page=1&per_page=100")
        # lines = response.json()
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            with open( f"{current_directory}../../mockdata/content.json", encoding="utf8") as file:
                lines = json.load(file)
            if len(lines) == 0:
                logging.debug("no data on the file")
                return
        except FileNotFoundError:
            logging.debug("File not found")
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
            self.parent.centralWidget().layout().addWidget()
            pass


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