import random
from typing import Any


class InvalidDistinationFor42Path(Exception):
    pass


class InvalidEntryExitPoint(Exception):
    pass


class Cell:
    def __init__(self) -> None:
        self.north: bool = True
        self.west: bool = True
        self.south: bool = True
        self.east: bool = True
        self.visited = False
        self._42_path = False


class MazeGenerator:
    def __init__(self, cols: int, rows: int, Entry: Any, EXIT: Any, out_file
                 ) -> None:
        self.x = cols
        self.y = rows
        self.maze:  list[list[Cell]] = self.creat_grid()
        self.stack: list[list[Cell]] = []
        self.entry = Entry
        self.exit = EXIT
        self.out_file = out_file

    def creat_grid(self) -> list[list[Cell]]:
        return [[Cell() for _ in range(self.x)] for _ in range(self.y)]

    def find_nighbors(self, cell: Any) -> list[tuple[int, int, str]]:
        x, y = cell
        maze = self.maze
        unvisited_cells = []
        if (x - 1 >= 0 and not maze[y][x-1].visited
                and not self.maze[y][x - 1]._42_path):
            unvisited_cells.append((x-1, y, "left"))
        if (x + 1 < self.x and not maze[y][x+1].visited
                and not self.maze[y][x + 1]._42_path):
            unvisited_cells.append((x+1, y, "right"))
        if (y - 1 >= 0 and not maze[y-1][x].visited
                and not self.maze[y - 1][x]._42_path):
            unvisited_cells.append((x, y-1, "top"))
        if (y + 1 < self.y and not maze[y+1][x].visited
                and not self.maze[y + 1][x]._42_path):
            unvisited_cells.append((x, y+1, "bottom"))
        return unvisited_cells

    def creat_maze_bakctracker_algo(self) -> None:
        entry = self.entry
        exit = self.exit
        # print(exit)
        if (self.x < 9 or self.y < 9):
            str = "Warning: invalid path for 42 pathern.\n'we will \
generat maze without 42 pathern'"
            raise InvalidDistinationFor42Path(str)
        self.creat_42_pathren()
        if (self.maze[entry[1]][entry[0]]._42_path or
           self.maze[exit[1]][exit[0]]._42_path):
            raise InvalidEntryExitPoint("Try other exit or entry point it's \
invalid (inside '42 path')")
        self.remove_walls_backtracker_algo()

    def creat_maze_prims_algo(self) -> None:
        entry = self.entry
        exit = self.exit
        print(exit)
        if (self.x < 9 or self.y < 9):
            str = "Warning: invalid path \
for 42 pathern.\n'we will generat maze without 42 pathern'"
            raise InvalidDistinationFor42Path(str)
        self.creat_42_pathren()
        if (self.maze[entry[1]][entry[0]]._42_path is True or
           self.maze[exit[1]][exit[0]]._42_path is True):
            raise InvalidEntryExitPoint("Try other exit or entry point it's \
invalid (inside '42 path')")
        self.remove_walls_prims_algo()

    def remove_walls_backtracker_algo(self, i: int = 0, j: int = 0) -> None:
        self.maze[j][i].visited = True
        neighbors = self.find_nighbors((i, j))
        while neighbors:
            next_cell = random.choice(neighbors)
            new_x, new_y, direction = next_cell
            self.maze[new_y][new_x].visited = True
            if direction == "left":
                self.maze[j][i].west = False
                self.maze[new_y][new_x].east = False
            elif direction == "right":
                self.maze[j][i].east = False
                self.maze[new_y][new_x].west = False
            elif direction == "top":
                self.maze[j][i].north = False
                self.maze[new_y][new_x].south = False
            elif direction == "bottom":
                self.maze[j][i].south = False
                self.maze[new_y][new_x].north = False
            self.remove_walls_backtracker_algo(new_x, new_y)
            neighbors = self.find_nighbors((i, j))

    def find_visited_cell(self, cell: tuple[int, int]) -> Any:
        x, y = cell
        maze = self.maze
        visited_cells = []
        if x - 1 >= 0 and maze[y][x-1].visited:
            visited_cells.append((x-1, y, "left"))
        if x + 1 < self.x and maze[y][x+1].visited:
            visited_cells.append((x+1, y, "right"))
        if y - 1 >= 0 and maze[y-1][x].visited:
            visited_cells.append((x, y-1, "top"))
        if y + 1 < self.y and maze[y+1][x].visited:
            visited_cells.append((x, y+1, "bottom"))
        # if visited_cells != []:
        return visited_cells
        # return None

    @staticmethod
    def remove_duplicate_and_visited(items: Any) -> Any:
        none_duplicate: Any = []
        for item in items:
            if item not in none_duplicate:
                none_duplicate.append(item)
        return none_duplicate

    def remove_wall(self, cell1: tuple[int, int, str], cell2: Any) -> None:
        x1 = cell1[0]
        y1 = cell1[1]
        x2 = cell2[0]
        y2 = cell2[1]

        if x1 - 1 == x2 and y1 == y2:
            self.maze[y1][x1].west = False
            self.maze[y2][x2].east = False
        elif x1 + 1 == x2 and y1 == y2:
            self.maze[y1][x1].east = False
            self.maze[y2][x2].west = False
        elif x1 == x2 and y1 + 1 == y2:
            self.maze[y1][x1].south = False
            self.maze[y2][x2].north = False
        elif x1 == x2 and y1 - 1 == y2:
            self.maze[y1][x1].north = False
            self.maze[y2][x2].south = False

    def remove_walls_prims_algo(self, i: int = 0, j: int = 0) -> None:
        self.maze[j][i].visited = True

        frentier_cells = self.find_nighbors((i, j))
        while frentier_cells:
            target_cell = random.choice(frentier_cells)
            new_x, new_y, old_direction = target_cell
            self.maze[new_y][new_x].visited = True
            frentier_cells.extend(self.find_nighbors((new_x, new_y)))
            frentier_cells = self.remove_duplicate_and_visited(frentier_cells)
            cell = self.find_visited_cell((new_x, new_y))
            if len(cell) == 1:
                i, j, new_direction = cell[0][0], cell[0][1], cell[0][2]
                if old_direction == "left" and new_direction == "right":
                    self.maze[j][i].west = False
                    self.maze[new_y][new_x].east = False
                elif old_direction == "right" and new_direction == "left":
                    self.maze[j][i].east = False
                    self.maze[new_y][new_x].west = False
                elif old_direction == "top" and new_direction == "bottom":
                    self.maze[j][i].north = False
                    self.maze[new_y][new_x].south = False
                elif old_direction == "bottom" and new_direction == "top":
                    self.maze[j][i].south = False
                    self.maze[new_y][new_x].north = False
                    i = new_x
                    j = new_y
            else:
                cell = random.choice(cell)
                self.remove_wall(target_cell, cell)
                i = cell[0]
                j = cell[1]

            frentier_cells.remove(target_cell)

    def creat_42_pathren(self) -> None:
        x = self.x // 2 - 3
        y = self.y // 2 - 3
        first_y = y
        # show 4
        for move in range(0, 4):
            self.maze[y + move][x]._42_path = True
            last_y = move
        y += last_y
        for move in range(1, 3):
            self.maze[y][x + move]._42_path = True
            last_x = move
        x += last_x
        for move in range(1, 4):
            self.maze[y + move][x]._42_path = True
            last_y = move
        y += last_y
        y = first_y
        x += 2
        # show 2
        for move in range(0, 3):
            self.maze[y][x + move]._42_path = True
            last_x = move
        x += last_x
        for move in range(1, 4):
            self.maze[y + move][x]._42_path = True
            last_y = move
        y += last_y
        for move in range(1, 3):
            self.maze[y][x - move]._42_path = True
            last_x = move
        x -= last_x
        for move in range(1, 4):
            self.maze[y + move][x]._42_path = True
            last_y = move
        y += last_y
        for move in range(1, 3):
            self.maze[y][x + move]._42_path = True
            last_x = move
        x += last_x

    #  i need to fix return
    @staticmethod
    def print_walls_as_hex(cell: Cell) -> str:
        if (cell.north and cell.east and cell.south and cell.west):
            return "F"
        elif (not cell.north and cell.east and cell.south and cell.west):
            return "E"
        elif (cell.north and not cell.east and cell.south and cell.west):
            return "D"
        elif (not cell.north and not cell.east and cell.south
              and cell.west):
            return "C"
        elif (cell.north and cell.east and not cell.south and cell.west):
            return "B"
        elif (not cell.north and cell.east and not cell.south and cell.west):
            return "A"
        elif (cell.north and not cell.east and not cell.south and cell.west):
            return "9"
        elif (not cell.north and not cell.east and not cell.south
              and cell.west):
            return "8"
        elif (cell.north and cell.east and cell.south and not cell.west):
            return "7"
        elif (not cell.north and cell.east and cell.south and not cell.west):
            return "6"
        elif (cell.north and not cell.east and cell.south and not cell.west):
            return "5"
        elif (not cell.north and not cell.east and cell.south
              and not cell.west):
            return "4"
        elif (cell.north and cell.east and not cell.south and not cell.west):
            return "3"
        elif (not cell.north and cell.east and not cell.south
              and not cell.west):
            return "2"
        elif (cell.north and not cell.east and not cell.south
              and not cell.west):
            return "1"
        elif (not cell.north and not cell.east and not cell.south
              and not cell.west):
            return "0"

    # this function those not finish
    def creat_output_file(self, path: str) -> None:
        with open(self.out_file, "w") as file:
            for y in range(self.y):
                for x in range(self.x):
                    file.write(f"{self.print_walls_as_hex(self.maze[y][x])}")
                file.write("\n")
            file.write("\n")
            file.write(f"{self.entry[0]}, {self.entry[1]}\n"
                       f"{self.exit[0]}, {self.exit[1]}\n")
            file.write(f"{self.print_path(path)}\n")

    @staticmethod
    def print_path(path: list[tuple[int, int]]) -> str:
        # prev move
        x1, y1 = path[0]
        path_directions = ""
        for i in range(1, len(path)):
            # next move
            x2, y2 = path[i]
            if x1 == x2 and y1 - 1 == y2:
                path_directions += "N"
            elif x1 == x2 and y1 + 1 == y2:
                path_directions += "S"
            elif x1 - 1 == x2 and y1 == y2:
                path_directions += "W"
            elif x1 + 1 == x2 and y1 == y2:
                path_directions += "E"
            x1, y1 = path[i]
        return path_directions

    def debug_print(self) -> None:
        for y in range(self.y):
            # top walls
            for x in range(self.x):
                print("====" if self.maze[y][x].north else "=   ", end="")
            print("=")

            # side walls
            for x in range(self.x):
                print("||  " if self.maze[y][x].west else "    ", end="")
            print("||")

        # bottom border
        print("====" * self.x + "=")


if __name__ == "__main__":
    # her we creat our maze with closed walls
    print("\n#######################  Maze 1 #########################\n")
    a = MazeGenerator(30, 12)
    try:
        a.creat_maze_bakctracker_algo()
    except InvalidDistinationFor42Path:
        a.remove_walls_backtracker_algo()
    a.debug_print()
    b = MazeGenerator(30, 12)
    print("\n#######################  Maze 2  #########################\n")
    try:
        b.creat_maze_prims_algo()
    except InvalidDistinationFor42Path:
        b.remove_walls_prims_algo()

    #  this method show our maze in terminal use it to test
    b.debug_print()
    a.output_file()
