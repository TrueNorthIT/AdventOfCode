# Day 10

## Solved Part 2 due to a bug in Part 1 :) 

## Solutions:

#### Part 1 Solution


```python
    def count_trails(self, currentPos: complex, grid: dict[complex, int], visited: set[complex]) -> int:
        current_value = grid[currentPos]

        if currentPos in visited:
            return 0

        visited.add(currentPos)

        if current_value == 9:
            return 1

        # Directions
        directions = [UP, DOWN, LEFT, RIGHT]

        # Recurse into all valid neighbors
        trail_count = 0
        for direction in directions:
            neighbor = currentPos + direction
            if grid.get(neighbor) == current_value + 1:
                trail_count += self.count_trails(neighbor, grid, visited)

        return trail_count

    def part1(self):
        grid, lookup = self.parse_input()
        return sum(self.count_trails(trailhead, grid, set()) for trailhead in lookup[0])
```

Recursively explore the trails stoping if we have already visited it

#### Part 2 Solution

``` python

    def calculate_trails_ratings(self, currentPos: complex, grid: dict[complex, int]) -> int:
        current_value = grid[currentPos]

        if current_value == 9:
            return 1

        # Directions
        directions = [UP, DOWN, LEFT, RIGHT]

        # Recurse into all valid neighbors
        trail_count = 0
        for direction in directions:
            neighbor = currentPos + direction
            if grid.get(neighbor) == current_value + 1:
                trail_count += self.calculate_trails_ratings(neighbor, grid)

        return trail_count

    def part2(self):
        grid, lookup = self.parse_input()
        return sum(self.calculate_trails_ratings(trailhead, grid) for trailhead in lookup[0])
```

Part 2 here is Part 1 but without the visited check :) 

## Benchmark 1000 Iterations (PyPy)

| Part   | Avg Time   | Median    | 95th %ile | 99th %ile | Unit |
|--------|------------|-----------|-----------|-----------|------|
| Part 1 | 16.208382  | 15.525103 | 21.986711 | 30.239782 | ms   |
| Part 2 | 16.614810  | 14.720678 | 25.178528 | 39.875073 | ms   |
