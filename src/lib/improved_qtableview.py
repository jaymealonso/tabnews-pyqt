from dataclasses import dataclass
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QSize

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
        self.columns:list[ColumnData] = []

    def by_fieldname(self, fieldname: str) -> ColumnData:
        return next((column for column in self.columns if column.fieldname == fieldname))
    

class ImprTableToolbar(QtWidgets.QToolBar):
    def __init__(self):
        super(ImprTableToolbar, self).__init__()

        self.setIconSize(QSize(24, 24))
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.title = QtWidgets.QLabel()
        self.title.setText("Title")
        self.addWidget(self.title)

        self.addWidget(QtWidgets.QPushButton("V"))

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.addWidget(spacer)

        self.act_config = self.addAction("Config Table")
        # self.act_config.triggered.connect()    


class ImprTableTable(QtWidgets.QTableView):
    def __init__(self, parent: QtWidgets.QWidget | None = ...) -> None:
        super(ImprTableTable, self).__init__(parent)

        self.custom_model:QtGui.QStandardItemModel = QtGui.QStandardItemModel(0, 0)
        self.description_widget:QtWidgets.QWidget = None
        self.setModel(self.custom_model)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)


class ImprTableWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = ...) -> None:
        super(ImprTableWidget, self).__init__(parent)

        self.header_row = ImprTableToolbar()
        self.table = ImprTableTable(self)
        self.fields = ColumnsData()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.header_row)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def fill_data(self, lines: list):
        model:QtGui.QStandardItemModel = self.table.model()
        model.setRowCount(len(lines))
        model.setColumnCount(len(self.fields.columns))
        model.setHorizontalHeaderLabels([column.descricao for column in self.fields.columns])

        for row_no, line in enumerate(lines):
            for column in self.fields.columns:           
                index = model.index(row_no, column.index)
                model.setData(index, line.get(column.fieldname))

        self.table.resizeColumnsToContents()

        for field in self.fields.columns:
            self.table.setColumnHidden(field.index, not field.first_display)

