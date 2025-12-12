import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from JoesAoCSolver import JoesAoCSolver
from collections import defaultdict, deque
from functools import lru_cache


VIABLE = "Yes"
NOT_VIABLE = "No"
POTENTIALY_VIABLE = "Unknown"


class Shape:
    width: int
    height: int
    shape: list[tuple[int, int]] = []

    def __init__(self, shape: list[tuple[int, int]]):
        self.shape = shape
        self.width = max(x for x, y in shape) + 1
        self.height = max(y for x, y in shape) + 1

    def area(self) -> int:
        return self.width * self.height

    def occupied_area(self) -> int:
        return len(self.shape)

    def return_rotated(self, rotation: int) -> "Shape":
        if rotation % 4 == 0:
            return Shape(self.shape)
        elif rotation % 4 == 1:
            new_shape = [(self.height - 1 - y, x) for x, y in self.shape]
            return Shape(new_shape)
        elif rotation % 4 == 2:
            new_shape = [
                (self.width - 1 - x, self.height - 1 - y) for x, y in self.shape
            ]
            return Shape(new_shape)
        elif rotation % 4 == 3:
            new_shape = [(y, self.width - 1 - x) for x, y in self.shape]
            return Shape(new_shape)

    def __str__(self) -> str:
        rows = []
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                if (x, y) in self.shape:
                    row += "#"
                else:
                    row += "."
            rows.append(row)
        return "\n".join(rows)


class Region:
    width: int
    height: int

    desired_shapes: dict[int, int] = {}
    added_shapes: dict[Shape, int] = {}
    current_config: dict[int, int] = {}

    viable: str = POTENTIALY_VIABLE

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.desired_shapes = {}
        self.current_config = {}

    def reset_config(self):
        self.current_config = {}
        self.viable = POTENTIALY_VIABLE
        self.added_shapes = {}

    def get_free_spaces(self) -> int:
        occupied = 0
        total = self.width * self.height
        for shape, times in self.added_shapes.items():
            occupied += shape.occupied_area() * times
        free_spaces = total - occupied
        return free_spaces

    def add_shape_check(self, shape: Shape, shapeId: int) -> bool:
        # This is just used to prune impossible configurations quickly, it does not check for actual placement

        free_spaces = self.get_free_spaces()
        if free_spaces < shape.occupied_area():
            self.viable = NOT_VIABLE
            return False

        # Now if it's bounding box fit's then we can fit it without overlap
        if free_spaces < shape.area():
            self.viable = NOT_VIABLE
            return False

        # Maybe we can fit it, so add it to our added shapes and return True
        self.added_shapes[shape] = self.added_shapes.get(shape, 0) + 1
        # Also decrement the desired shapes count
        self.desired_shapes[shapeId] = self.desired_shapes.get(shapeId, 0) - 1
        return True

    def pack_shapes(self) -> str:
        # We should now have a dict of added_shapes that are somewhat feesible to fit in the region
        # and we need to try and actually fit them in without overlap

        # We can now see if it's 100% viable by comparing the bounding box area to the region area
        occupied = 0
        total = self.width * self.height
        for shape, times in self.added_shapes.items():
            occupied += shape.area() * times

        print(f"Region {self.width}x{self.height} occupied area: {occupied} / {total}")
        if occupied <= total:
            self.viable = VIABLE

        return self.viable


class Day12Solver(JoesAoCSolver):

    def parse_input(self):
        shapes = {}
        regions = []
        sections = self.input_data.strip().split("\n\n")
        for section in sections[:-1]:
            lines = section.strip().split("\n")
            shape_id = lines[0].rstrip(":")
            shape_coords = []
            for y, line in enumerate(lines[1:]):
                for x, char in enumerate(line):
                    if char == "#":
                        shape_coords.append((x, y))
            shapes[int(shape_id)] = Shape(shape_coords)

        regions_section = sections[-1].strip().split("\n")
        for line in regions_section:
            parts = line.split(":")
            size_part = parts[0].strip()
            shape_parts = list(map(int, parts[1].strip().split()))
            width, height = map(int, size_part.split("x"))
            region = Region(width, height)
            for shape_id, count in enumerate(shape_parts):
                region.desired_shapes[int(shape_id)] = int(count)
            regions.append(region)
        return shapes, regions

    def part1_examples(self):
        return [
            (
                """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2""",
                2,
            )
        ]

    def part1(self):
        shapes, regions = self.parse_input()

        YES_COUNT = 0
        NO_COUNT = 0
        UNKOWN_COUNT = 0

        for region in regions:
            print(
                f"Packing region {region.width}x{region.height} with desired shapes {region.desired_shapes}"
            )
            region.reset_config()

            for shape_id, desired_count in region.desired_shapes.items():
                if desired_count == 0:
                    continue
                shape = shapes[shape_id]
                for _ in range(desired_count):
                    region.add_shape_check(shape, shape_id)
                    if region.viable == NOT_VIABLE:
                        continue

            region.pack_shapes()
            if region.viable == VIABLE:
                YES_COUNT += 1
            elif region.viable == NOT_VIABLE:
                NO_COUNT += 1
            else:
                UNKOWN_COUNT += 1
        print(
            f"We have {YES_COUNT} viable regions, {NO_COUNT} non-viable regions and {UNKOWN_COUNT} unknown regions"
        )


if __name__ == "__main__":
    solver = Day12Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
