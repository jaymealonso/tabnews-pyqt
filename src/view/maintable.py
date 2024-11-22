from calendar import firstweekday
from dataclasses import dataclass
import enum
import logging
from xmlrpc.client import Boolean
from PyQt5 import QtWidgets, QtGui 
from PyQt5.QtCore import Qt, QSize
from view.main_side_description import MyPostContent
from model.model import MainPageContent

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

@dataclass
class ColumnData():
    actual_index = -1

    fieldname: str = ""
    descricao: str = ""
    first_display: bool = False
    index: int | None = None

    def __init__(self, fieldname, descricao, first_display:bool = False, index:int | None = None) -> None:
        if not index:
            ColumnData.actual_index += 1
            self.index = ColumnData.actual_index
        else:
            self.index = index
        self.fieldname = fieldname
        self.descricao = descricao
        self.first_display = first_display

class ColumnsData():
    def __init__(self) -> None:
        self.columns = [
            ColumnData(fieldname="title", descricao="Titulo", first_display=True),
            ColumnData(fieldname="status", descricao="Status", first_display=True),
            ColumnData(fieldname="created_at", descricao="Criado em", first_display=True),
            ColumnData(fieldname="updated_at", descricao="Atualizado em", first_display=True),
            ColumnData(fieldname="owner_username", descricao="Usuário", first_display=True),
            ColumnData(fieldname="slug", descricao="Slug", first_display=True),
            ColumnData(fieldname="id", descricao=""),
            ColumnData(fieldname="owner_id", descricao=""),
            ColumnData(fieldname="parent_id", descricao=""),
            ColumnData(fieldname="status", descricao=""),
            ColumnData(fieldname="source_url", descricao=""),
            ColumnData(fieldname="published_at", descricao=""),
            ColumnData(fieldname="deleted_at", descricao=""),
            ColumnData(fieldname="tabcoins", descricao=""),
            ColumnData(fieldname="tabcoins_credit", descricao=""),
            ColumnData(fieldname="tabcoins_debit", descricao=""),
            ColumnData(fieldname="children_deep_count", descricao=""),
            ColumnData(fieldname="type", descricao=""),            
        ]

    def by_fieldname(self, fieldname: str) -> ColumnData:
        return next((column for column in self.columns if column.fieldname == fieldname))


class MyTable(QtWidgets.QTableView):
    def __init__(self, parent: QtWidgets.QWidget | None = ..., parent_mainwindow:QtWidgets.QMainWindow = None) -> None:
        super(MyTable, self).__init__(parent)

        self.fields = ColumnsData() 

        self.parent_mainwindow = parent_mainwindow
        self.model:QtGui.QStandardItemModel = QtGui.QStandardItemModel(0, 0)
        self.description_widget:QtWidgets.QWidget = None
        self.setModel(self.model)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

        self.load_data()

    def load_data(self):
        content = MainPageContent()
        lines = content.operation()
        if len(lines) == 0:
            return

        self.model.clear()
        self.model.setRowCount(len(lines))
        self.model.setColumnCount(len(self.fields.columns))
        self.model.setHorizontalHeaderLabels([column.descricao for column in self.fields.columns])


        for row_no, line in enumerate(lines):
            for column in self.fields.columns:           
                index = self.model.index(row_no, column.index)
                self.model.setData(index, line.get(column.fieldname))

        self.resizeColumnsToContents()

        for field in self.fields.columns:
            self.setColumnHidden(field.index, not field.first_display)

    def mouseDoubleClickEvent(self, e: QtGui.QMouseEvent | None) -> None:
        logging.debug("double click")
        logging.debug(f"indexes {self.selectedIndexes()}")

        indexes = self.selectedIndexes()
        if len(indexes) == 1:
            index = indexes[0]
            layout = self.parent_mainwindow.centralWidget().layout()
            if self.description_widget:
                layout.removeWidget(self.description_widget)
            
            slug = index.siblingAtColumn(self.fields.by_fieldname('slug').index).data(Qt.DisplayRole)
            user = index.siblingAtColumn(self.fields.by_fieldname('owner_username').index).data(Qt.DisplayRole)
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
        self.act_load_data.triggered.connect(lambda: self.parent_table.load_data())

        self.act_load_all_data = self.addAction("Load ALL data")
        self.act_load_all_data.triggered.connect(lambda: self.parent_table.load_data())

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.addWidget(spacer)

        self.act_config = self.addAction("Config Table")
        # self.act_config.triggered.connect()