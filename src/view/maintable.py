import logging
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QSize
from lib.improved_qtableview import ColumnData, ImprTableWidget
from view.main_side_description import MyPostContent
from model.model import MainPageContent

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


class MyTableWidget(ImprTableWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super(MyTableWidget, self).__init__(parent)

        self.fields.columns.extend(
            [
                ColumnData(fieldname="title", descricao="Titulo", visible=True),
                ColumnData(fieldname="status", descricao="Status", visible=True),
                ColumnData(fieldname="created_at", descricao="Criado em", visible=True),
                ColumnData(
                    fieldname="updated_at",
                    descricao="Atualizado em",
                    visible=True,
                ),
                ColumnData(fieldname="owner_username", descricao="Usuário", visible=True),
                ColumnData(fieldname="slug", descricao="Slug"),
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
        )

        self.description_widget: MyPostContent | None = None
        self.load_data()

        self.table.doubleClicked.connect(self.mouseDoubleClickEvent)

        self.header_row.act_config.trigger()

    def load_data(self):
        content = MainPageContent()
        lines = content.operation()
        if len(lines) == 0:
            return

        self.fill_data(lines)

    def mouseDoubleClickEvent(self, e: QtGui.QMouseEvent | None) -> None:
        indexes = self.table.selectedIndexes()

        logging.debug("double click")
        logging.debug(f"indexes {indexes}")

        if len(indexes) == 1:
            index = indexes[0]

            window_main: QtWidgets.QMainWindow = self.parent().parent()
            layout: QtWidgets.QLayout = window_main.centralWidget().layout()
            if self.description_widget:
                layout.removeWidget(self.description_widget)

            slug = index.siblingAtColumn(self.fields.by_fieldname("slug").index).data(Qt.DisplayRole)
            user = index.siblingAtColumn(self.fields.by_fieldname("owner_username").index).data(Qt.DisplayRole)
            self.description_widget = MyPostContent(self)
            self.description_widget.setContent(user, slug)
            layout.addWidget(self.description_widget)


class MyToolbar(QtWidgets.QToolBar):
    def __init__(self, table_widget: MyTableWidget):
        super(MyToolbar, self).__init__()
        self.parent_table: MyTableWidget = table_widget
        self.setIconSize(QSize(24, 24))
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        self.act_load_data = self.addAction("Load data")
        self.act_load_data.triggered.connect(self.parent_table.load_data)

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.addWidget(spacer)
