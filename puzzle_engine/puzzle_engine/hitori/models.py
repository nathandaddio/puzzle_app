from collections import namedtuple
from itertools import combinations


class Board(object):
    def __init__(self, number_of_rows, number_of_columns, cells):
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.cells = cells


class Cell(object):
    def __init__(self, row_number, column_number, value):
        self.row_number = row_number
        self.column_number = column_number
        self.value = value

    def __repr__(self):
        return "Cell(row={},column={},value={})".format(
            self.row_number, self.column_number, self.value)


class EngineData(object):
    def __init__(self, board):
        self.board = board

        self.cell_incompatibilities = cell_incompatibility_factory(board.cells)
        self.cell_adjacencies = cell_adjacency_factory(board.cells)
        self.cell_neighbourhoods = cell_neighbourhood_factory(board.cells)


CellIncompatibility = namedtuple('CellIncompatability', ['cell_1', 'cell_2'])


def cell_incompatibility_factory(cells):
    return [
        CellIncompatibility(cell_1, cell_2)
        for cell_1, cell_2 in combinations(cells, 2)
        if are_incompatible_cells(cell_1, cell_2)
    ]


def are_incompatible_cells(cell_1, cell_2):
    return (
        cell_1.value == cell_2.value
        and (
            cell_1.row_number == cell_2.row_number or
            cell_1.column_number == cell_2.column_number
        )
    )


CellAdjacency = namedtuple('CellAdjacency', ['cell_1', 'cell_2'])


def cell_adjacency_factory(cells):
    return [
        CellAdjacency(cell_1, cell_2)
        for cell_1, cell_2 in combinations(cells, 2)
        if are_adjacent_cells(cell_1, cell_2)
    ]


def are_adjacent_cells(cell_1, cell_2):
    """
    Cells are adjacent if their Manhattan distance
    is less than or equal to 1.
    """
    return manhattan_distance(
        cell_1.row_number,
        cell_1.column_number,
        cell_2.row_number,
        cell_2.column_number
    ) <= 1


def manhattan_distance(x_1, y_1, x_2, y_2):
    return abs(x_1 - x_2) + abs(y_1 - y_2)


class CellNeighbourhood(object):
    def __init__(self, cell, neighbours):
        self.cell = cell
        self.neighbours = neighbours


def cell_neighbourhood_factory(cells):
    return [
        CellNeighbourhood(
            cell=cell_1,
            neighbours=[
                cell_2 for cell_2 in cells
                if are_adjacent_cells(cell_1, cell_2)
                and cell_1 != cell_2
            ]
        )
        for cell_1 in cells
    ]
