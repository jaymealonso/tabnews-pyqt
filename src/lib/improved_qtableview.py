from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from lib.items_select_popup import ItemsSelectDialog
from lib.dataclasses import ColumnData


class ImprTableColumns:
    def __init__(self) -> None:
        self.columns: list[ColumnData] = []

    def by_fieldname(self, fieldname: str) -> ColumnData:
        return next((column for column in self.columns if column.fieldname == fieldname))


class ImprTableToolbar(QtWidgets.QToolBar):
    config_clicked = pyqtSignal()

    def __init__(self):
        super(ImprTableToolbar, self).__init__()

        self.setIconSize(QSize(24, 24))
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.title_value: str = None

        self.title_label = QtWidgets.QLabel()
        self.set_title("Title")
        self.addWidget(self.title_label)
        self.addSeparator()
        self.addWidget(QtWidgets.QPushButton("<layout>"))

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.addWidget(spacer)

        self.act_config = self.addAction("Config Table")
        self.act_config.triggered.connect(self.on_config)

    def set_title(self, title: str | None = None, row_count: int = 0):
        if title:
            self.title_value = title
        self.title_label.setText(f"{self.title_value} ({str(row_count)})")

    def on_config(self):
        self.config_clicked.emit()


class ImprTableTable(QtWidgets.QTableView):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(ImprTableTable, self).__init__(parent)

        self.custom_model: QtGui.QStandardItemModel = QtGui.QStandardItemModel(0, 0)
        self.description_widget: QtWidgets.QWidget | None = None
        self.setModel(self.custom_model)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)


class ImprTableWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super(ImprTableWidget, self).__init__(parent)

        self.config_popup: ItemsSelectDialog = None
        self.header_row = ImprTableToolbar()
        self.table = ImprTableTable(self)
        self.fields = ImprTableColumns()

        self.header_row.config_clicked.connect(self.open_config)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.header_row)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def open_config(self):
        self.config_popup = ItemsSelectDialog(self, self.fields.columns)
        self.config_popup.show()

    def fill_data(self, lines: list):
        model: QtGui.QStandardItemModel = self.table.model()  # type: ignore
        model.setRowCount(len(lines))
        model.setColumnCount(len(self.fields.columns))
        model.setHorizontalHeaderLabels([column.descricao for column in self.fields.columns])
        self.header_row.set_title(row_count=len(lines))

        for row_no, line in enumerate(lines):
            for column in self.fields.columns:
                index = model.index(row_no, column.index)
                model.setData(index, line.get(column.fieldname))

        self.table.resizeColumnsToContents()

        for field in self.fields.columns:
            self.table.setColumnHidden(field.index, not field.visible)
