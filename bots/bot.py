import collections
from dataclasses import dataclass
import itertools
import sys
import math


@dataclass
class Cell:
    x: int
    y: int
    scrap_amount: int
    owner: int
    units: int
    has_recycler: bool
    buildable: bool
    spawnable: bool
    recycler_range: bool

    def available(self):
        return self.owner in [0, -1] and not self.has_recycler and self.scrap_amount != 0

    @property
    def coordinates(self):
        return (self.x, self.y)


class Grid:

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grid = dict()

    def add(self, cell):
        self.grid[(cell.x, cell.y)] = cell

    def get_neighbours(self, x, y, distance=1):
        return itertools.product([x, x - distance, x + distance], [y, y - distance, y + distance])

    def get_my_units(self):
        for cell in self.grid.values():
            if cell.owner == 1 and cell.units != 0:
                yield cell

    def get_territory(self):
        for cell in self.grid.values():
            if cell.owner == 1:
                yield cell

    def move_to_closest_free_cell(self, unit):
        for distance in range(1, 3):
            for cell_x, cell_y in self.get_neighbours(unit.x, unit.y, distance):
                cell = self.grid.get((cell_x, cell_y))
                if cell is not None and cell.available():
                    return f"MOVE 1 {unit.x} {unit.y} {cell_x} {cell_y}"
        return ""

    def middle_lane(self):
        ret = []
        middle = self.width // 2
        for y in range(0, height):
            if self.grid[(middle, y)].scrap_amount != 0:
                ret.append((middle, y))
        return ret


width, height = [int(i) for i in input().split()]

while True:
    my_matter, opp_matter = [int(i) for i in input().split()]
    grid = Grid(height, width)

    for y in range(height):
        for x in range(width):
            # owner: 1 = me, 0 = foe, -1 = neutral
            scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler = [int(k) for k in input().split()]
            grid.add(Cell(x, y, scrap_amount, owner, units, recycler, can_build, can_spawn, in_range_of_recycler))

    middle_lane = grid.middle_lane()
    commands = []
    for cell in grid.get_my_units():
        #        command = grid.move_to_closest_free_cell(cell)
        command = f"MOVE 1 {cell.x} {cell.y} {width // 2} {height // 2}"
        if command:
            commands.append(command)
        else:
            commands.append(f"MOVE 1 {cell.x} {cell.y} {middle_lane[0][0]} {middle_lane[0][1]}")

        if my_matter >= 60:
            commands.append(f"SPAWN 1 {cell.x} {cell.y}")

    if my_matter >= 20:
        for my_cell in grid.get_territory():
            if my_cell.scrap_amount >= 10 or (my_cell.x, my_cell.y) in middle_lane:
                commands.append(f"BUILD {my_cell.x} {my_cell.y}")
                break


    if not commands:
        print("WAIT")
    else:
        print(";".join(commands))