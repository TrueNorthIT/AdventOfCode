# Day 08

## Solutions:

#### Part 1 Solution

```python
    def part1(self):
        antennas, grid_bounds = self.parse_input()

        antenodes = set()
        for _, positions in antennas.items():
            all_pairs = itertools.combinations(positions, 2)
            for pair in all_pairs:
                delta = pair[0] - pair[1]
                antenodes.add(pair[0] + delta)
                antenodes.add(pair[1] - delta)

        return len({pos for pos in antenodes if in_bounds(pos, grid_bounds)})
```

We add/sub on the difference of each pair to each end then just ensure they are all in bounds

#### Part 2 Solution

```python
    def part2(self):
        antennas, grid_bounds = self.parse_input()
        
        antenodes = set()
        for _, positions in antennas.items():
            all_pairs = itertools.combinations(positions, 2)
            if (len(positions) >= 2): antenodes.update(positions)
            for pair in all_pairs:
                delta = pair[0] - pair[1]

                a_1 = pair[0]
                while in_bounds(a_1 + delta, grid_bounds):
                    a_1 += delta
                    antenodes.add(a_1)

                a_2 = pair[1]
                while in_bounds(a_2 - delta, grid_bounds):
                    a_2 -= delta
                    antenodes.add(a_2)

        return len(antenodes)
```

Part 2 is very similar, we just keep adding antenodes until we are out of bounds. And we add the positions of the antennas themselves as long as there is at least two.

## Benchmark 1000 Iterations (PyPy)

| Part   | Avg Time    | Median      | 95th %ile  | 99th %ile  | Unit  |
|--------|-------------|-------------|------------|------------|-------|
| Part 1 | 731.288910  | 998.735428  | 1.110065   | 3.111265   | μs    |
| Part 2 | 944.929361  | 999.927521  | 1.991856   | 3.295851   | μs    |
