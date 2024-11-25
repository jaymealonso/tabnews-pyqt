from typing import Any, Dict
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from lib.dataclasses import ColumnData


class ItemsSelectLayout(QtWidgets.QGridLayout):
    def __init__(self) -> None:
        super(ItemsSelectLayout, self).__init__()

        self.header = QtWidgets.QWidget()
        # self.header.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Maximum)
        self.header.setFixedHeight(50)
        # self.header.setStyleSheet("background-color: red")
        self.header.setLayout(QtWidgets.QVBoxLayout())
        self.header.layout().addWidget(QtWidgets.QLabel("Selecione colunas para aparecer na tabela:"))

        self.middle_left = QtWidgets.QWidget()
        self.middle_left.setLayout(QtWidgets.QVBoxLayout())
        self.middle_left.layout().addWidget(QtWidgets.QLabel("Colunas disponíveis:"))
        self.listview_cols_available = QtWidgets.QListView()
        self.middle_left.layout().addWidget(self.listview_cols_available)

        # self.middle_left.setStyleSheet("background-color: green")

        self.center = QtWidgets.QWidget()
        self.center.setLayout(QtWidgets.QVBoxLayout())
        self.center.layout().addWidget(QtWidgets.QPushButton(">>"))
        self.center.layout().addWidget(QtWidgets.QPushButton(">"))
        self.center.layout().addWidget(QtWidgets.QPushButton("<"))
        self.center.layout().addWidget(QtWidgets.QPushButton("<<"))

        self.middle_right = QtWidgets.QWidget()
        self.middle_right.setLayout(QtWidgets.QVBoxLayout())
        self.middle_right.layout().addWidget(QtWidgets.QLabel("Colunas exibidas:"))
        self.listview_cols_visible = QtWidgets.QListView()
        self.middle_right.layout().addWidget(self.listview_cols_visible)

        # self.middle_right.setStyleSheet("background-color: darkgreen")

        self.footer = QtWidgets.QWidget()
        self.footer.setLayout(QtWidgets.QHBoxLayout())
        self.footer.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Maximum)
        self.footer.layout().addWidget(QtWidgets.QPushButton("Ok"))
        self.footer.layout().addWidget(QtWidgets.QPushButton("Cancel"))

        # self.footer.setStyleSheet("background-color: purple")

        self.addWidget(self.header, 1, 1, 1, 3, Qt.AlignmentFlag.AlignLeft)
        self.addWidget(self.middle_left, 2, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.center, 2, 2, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.middle_right, 2, 3, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.footer, 3, 1, 1, 3, Qt.AlignmentFlag.AlignRight)


class ItemsSelectDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget | None = ..., columns: list[ColumnData] = None) -> None:
        super(ItemsSelectDialog, self).__init__(parent)

        self.columns = columns
        layout = ItemsSelectLayout()
        self.setLayout(layout)

        item_model_available = QtGui.QStandardItemModel(0, 1)
        item_model_visible = QtGui.QStandardItemModel(0, 1)

        for column in self.columns:
            displayrole = column.descricao if column.descricao != "" else column.fieldname
            roles: Dict[int, Any] = {
                Qt.ItemDataRole.DisplayRole: displayrole,
                Qt.ItemDataRole.UserRole: column,
            }

            if not column.visible:
                item_model_available.appendRow(None)
                item_model_available.setItemData(
                    item_model_available.index(item_model_available.rowCount() - 1, 0), roles
                )
            else:
                item_model_visible.appendRow(None)
                item_model_visible.setItemData(item_model_visible.index(item_model_visible.rowCount() - 1, 0), roles)

        layout.listview_cols_available.setModel(item_model_available)
        layout.listview_cols_visible.setModel(item_model_visible)
