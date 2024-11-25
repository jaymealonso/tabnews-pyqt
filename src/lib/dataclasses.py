from dataclasses import dataclass


@dataclass
class ColumnData:
    actual_index = -1

    fieldname: str = ""
    descricao: str = ""
    visible: bool = False
    index: int = -1

    def __init__(self, fieldname, descricao, visible: bool = False, index: int | None = None) -> None:
        if not index:
            ColumnData.actual_index += 1
            self.index = ColumnData.actual_index
        else:
            self.index = index
        self.fieldname = fieldname
        self.descricao = descricao
        self.visible = visible
