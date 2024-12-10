from dataclasses import dataclass
from enum import Enum


class id_gen:
    next_id = 1001

    @classmethod
    def get(cls):
        cls.next_id += 1


class Direction(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4


@dataclass
class UserInput:
    time: int
    direction: Direction
    player_id: int

    def to_json(self):
        return {
            'time': self.time,
            'direction': self.direction.value,
            'player': self.player_id
        }

    @classmethod
    def from_json(cls, json: dict):
        pkg = cls(
            time=json['time'],
            direction=Direction(json['direction']),
            player_id=json['player_id']
        )
        return pkg


@dataclass
class Snapshot:
    time: int
    tiles: list['Tile']

    def to_json(self):
        return {
            'time': self.time,
            'tiles': [tile.to_json() for tile in self.tiles]
        }

    @classmethod
    def from_json(cls, json: dict):
        s = cls(
            time=json['time'],
            tiles=[Tile.from_json(tile) for tile in json['tiles']]
        )
        return s


@dataclass
class Cell:
    x: int
    y: int
    valid: bool = True

    def __bool__(self):
        return self.valid

    def __eq__(self, c: 'Cell'):
        return self.x == c.x and self.y == c.y

    def to_json(self):
        return {
            'x': self.x,
            'y': self.y,
            'valid': self.valid
        }

    @classmethod
    def from_json(cls, json: dict) -> 'Cell':
        cell = cls(
            x=json['x'],
            y=json['y'],
            valid=json['valid']
        )
        return cell


null_cell = Cell(0, 0, False)


@dataclass
class Tile:
    cell: Cell
    'null_cell if tile is null'
    value: int
    '-1 if tile is null'
    player_id: int
    '-1 if not player owned'
    previous: Cell = null_cell
    merged_from: tuple[Cell, Cell] = (null_cell, null_cell)

    @property
    def is_empty(self):
        return not self.cell or self.value == -1

    def __bool__(self):
        return self.is_empty

    def __eq__(self, other: 'Tile'):
        return self.cell == other.cell and \
            self.player_id == other.player_id and \
            self.value == other.value

    @property
    def merged(self):
        return not self.merged_from[0] and not self.merged_from[1]

    def save_position(self):
        self.merged_from = (null_cell, null_cell)
        self.previous = self.cell

    def to_json(self):
        return {
            'cell': self.cell.to_json(),
            'previous': self.previous.to_json(),
            'merged_from': [t.to_json() for t in self.merged_from],
            'value': self.value,
            'player_id': self.player_id
        }

    @classmethod
    def from_json(cls, json: dict) -> 'Tile':
        tile = cls(
            cell=Cell.from_json(json['cell']),
            previous=Cell.from_json(json['previous']),
            merged_from=[Cell.from_json(t) for t in json['merged_from']],
            value=json['value'],
            player_id=json['player_id']
        )
        return tile


class Grid:
    def __init__(self, rows=8, cols=8):
        self._rows = rows
        self._cols = cols
        # empty grid
        self._grid = [[
                null_tile
                for j in range(cols)
            ] for i in range(rows)]

    def move(self, player_id: int, direction: Direction):
        vector = self._get_vector(direction)
        traversals = self._build_traversals(vector)
        moved = False

        self._prepare_tiles()

        for t_x in traversals[0]:
            for t_y in traversals[1]:
                cell = Cell(t_x, t_y)
                tile = self._grid[t_x][t_y]

                if not tile or tile.player_id != player_id:
                    continue

                pos_far, pos_next = self._find_farthest_position(cell, vector)
                next = self._grid[pos_next.x][pos_next.y]

                if next and not next.merged and \
                        next.value == tile.value and \
                        next.player_id in (-1, player_id):
                    merged = Tile(pos_next, tile.value * 2)
                    merged.merged_from = (tile, next)

                    self._insert_tile(merged)
                    self._remove_tile(tile)
                    tile.cell = pos_next
                else:
                    self._move_tile(tile, pos_far)

                if cell != tile.cell:
                    moved = True

        return moved

    def _prepare_tiles(self):
        for row in self._grid:
            for tile in row:
                if tile:
                    tile.save_position()

    @staticmethod
    def _get_vector(direction: Direction):
        match direction:
            case Direction.Up:
                return 0, -1
            case Direction.Down:
                return 0, 1
            case Direction.Left:
                return -1, 0
            case Direction.Right:
                return 1, 0

    def _build_traversals(self, vector: tuple[int, int]
                          ) -> tuple[list[int], list[int]]:
        traversals = (
            [i for i in range(self._rows)],
            [j for j in range(self._cols)]
        )

        if vector[0] == 1:
            traversals[0].reverse()
        if vector[1] == 1:
            traversals[1].reverse()

        return traversals

    def _find_farthest_position(self, cell: Cell,
                                vector: tuple[int, int]):
        while True:
            previous = cell
            cell = Cell(cell.x + vector[0], cell.y + vector[1])
            if not (self._cell_within_bounds(cell) and
                    self._cell_available(cell)):
                break
        return previous, cell

    def _cell_within_bounds(self, cell: Cell):
        return 0 <= cell.x < self._cols and 0 <= cell.y < self._rows

    def _cell_available(self, cell: Cell):
        return bool(self._grid[cell.x][cell.y])

    def _clear(self):
        self._grid = [[
                null_tile
                for j in range(self._cols)
            ] for i in range(self._rows)]

    def _insert_tile(self, tile: Tile):
        self._grid[tile.cell.x][tile.cell.y] = tile

    def _remove_tile(self, tile: Tile):
        self._grid[tile.cell.x][tile.cell.y] = null_tile

    def _move_tile(self, tile: Tile, cell: Cell):
        self._grid[tile.cell.x][tile.cell.y] = null_tile
        self._grid[cell.x][cell.y] = tile
        tile.cell = cell

    def tiles(self):
        res = []
        for row in self._grid:
            for tile in row:
                if tile:
                    res.append(tile)
        return tile

    def from_tiles(self, ts: list[Tile]):
        self._clear()
        for tile in ts:
            self._grid[tile.cell.x][tile.cell.y] = tile


null_tile = Tile(null_cell, -1, -1)
