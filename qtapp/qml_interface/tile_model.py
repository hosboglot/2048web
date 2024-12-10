from PySide6.QtCore import (
    QObject, QPointF, Qt, QByteArray,
    Slot, Signal, Property,
    QAbstractListModel, QModelIndex
)
from PySide6.QtGui import QColor
from PySide6.QtQml import QmlElement

from shared.game import Tile, Cell

QML_IMPORT_NAME = "TileModel"
QML_IMPORT_MAJOR_VERSION = 1


TILE_COLORS = [QColor("red"), QColor("blue"),
               QColor("purple"), QColor("green")]


@QmlElement
class TileModel(QAbstractListModel):

    XRole = Qt.ItemDataRole.UserRole + 1
    YRole = XRole + 1
    ValueRole = YRole + 1
    PlayerIdRole = ValueRole + 1
    ColorRole = PlayerIdRole + 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self._container: list[Tile] = []
        self._color_map: dict[int, QColor] = {}
        self._animation_model = TileAnimationModel(self)

    @Property()
    def animationModel(self):
        return self._animation_model

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._container)

    def roleNames(self):
        ret = super().roleNames()
        ret[TileModel.XRole] = QByteArray(b"x")
        ret[TileModel.YRole] = QByteArray(b"y")
        ret[TileModel.ValueRole] = QByteArray(b"value")
        ret[TileModel.PlayerIdRole] = QByteArray(b"playerId")
        ret[TileModel.ColorRole] = QByteArray(b"color")
        return ret

    def data(self, index: QModelIndex, role: int):
        if not index.isValid():
            return None

        if role == TileModel.XRole:
            return self._container[index.row()].cell.x
        elif role == TileModel.YRole:
            return self._container[index.row()].cell.y
        elif role == TileModel.ValueRole:
            return self._container[index.row()].value
        elif role == TileModel.PlayerIdRole:
            return self._container[index.row()].player_id
        elif role == TileModel.ColorRole:
            p_id = self._container[index.row()].player_id
            if p_id == -1:
                return QColor("goldenrod")
            return self._color_map.setdefault(
                p_id, TILE_COLORS[len(self._color_map)])

    def updateTiles(self, tiles: list[Tile]):
        # self._animation_model.updateTiles(tiles)
        self.beginResetModel()
        self._container = tiles.copy()
        self.endResetModel()

    def findByCell(self, cell: Cell):
        for n, tile in enumerate(self._container):
            if tile.cell == cell:
                return n, tile


# class TileAnimationModel(QAbstractListModel):
#     XFromRole = Qt.ItemDataRole.UserRole + 1
#     YFromRole = XFromRole + 1
#     XToRole = YFromRole + 1
#     YToRole = XToRole + 1
#     ValueRole = YToRole + 1
#     PlayerIdRole = ValueRole + 1
#     ColorRole = PlayerIdRole + 1
#     # create tiles after movement

#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self._container: list[Tile] = []
#         self._color_map: dict[int, QColor] = {}

#     def rowCount(self, parent=QModelIndex()):
#         if parent.isValid():
#             return 0
#         return len(self._container)

#     def roleNames(self):
#         ret = super().roleNames()
#         ret[TileModel.XRole] = QByteArray(b"x")
#         ret[TileModel.YRole] = QByteArray(b"y")
#         ret[TileModel.ValueRole] = QByteArray(b"value")
#         ret[TileModel.PlayerIdRole] = QByteArray(b"playerId")
#         ret[TileModel.ColorRole] = QByteArray(b"color")
#         return ret

#     def data(self, index: QModelIndex, role: int):
#         if not index.isValid():
#             return None

#         if role == TileModel.XRole:
#             return self._container[index.row()].cell.x
#         elif role == TileModel.YRole:
#             return self._container[index.row()].cell.y
#         elif role == TileModel.ValueRole:
#             return self._container[index.row()].value
#         elif role == TileModel.PlayerIdRole:
#             return self._container[index.row()].player_id
#         elif role == TileModel.ColorRole:
#             p_id = self._container[index.row()].player_id
#             if p_id == -1:
#                 return QColor("goldenrod")
#             return self._color_map.setdefault(
#                 p_id, TILE_COLORS[len(self._color_map)])

#     def updateTiles(self, tiles: list[Tile]):
#         self.beginResetModel()
#         self._container = tiles.copy()
#         self.endResetModel()
