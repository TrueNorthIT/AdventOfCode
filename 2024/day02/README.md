# Day 02


## Solutions:

### Part 1:

#### Initial Solution
```python
     def part1(self):

        count = 0        
        lines = (list(map(int, x.split())) for x in self.input_data.splitlines())
        for line in lines:
            incremeting = False
            decrementing = False
            for i, p_char in enumerate(line):
                if i == len(line) - 1:
                    continue
                n_char = line[i+1]
                if p_char == n_char:
                    print(f"Line {line} is not incremeting or decrementing. Skipping")
                    break
                
                if abs(p_char - n_char) > 3:
                    print(f"Line {line} has a difference greater than 3. Skipping")
                    break
                    
                elif p_char < n_char:
                    if i == 0:
                        incremeting = True
                    if decrementing:
                        print(f"Line {line} changed direction. Skipping")
                        break
                elif p_char > n_char:
                    if i == 0:
                        decrementing = True
                    if incremeting:
                        print(f"Line {line} changed direction. Skipping")
                        break
            else:                
                count += 1
        print(count)
        return count
```
After completing Part 1 and seeing Part 2 I realsied I should probably refactor this as part 2 required the same logic.

#### Refactored Solution

```python

    def get_diffs(self, line: list[int]):
        diffs = [a-b for a,b in zip(line, line[1:])]

        # If all the differences are between -3 and -1 or 1 and 3, then the line is valid 
        # this checks that they are all increasing or decreasing AND that the difference is between 1 and 3
        return all(-3 <= x <= -1 for x in diffs) or all(1 <= x <= 3 for x in diffs)
        
    def part1(self):
        count = 0 
        lines = (list(map(int, x.split())) for x in self.input_data.splitlines())
        for line in lines:
            count += self.get_diffs(line)
        return count
```

### Part 2:

#### Solution
```python

    def get_diffs(self, line: list[int]):
        diffs = [a-b for a,b in zip(line, line[1:])]

        # If all the differences are between -3 and -1 or 1 and 3, then the line is valid 
        # this checks that they are all increasing or decreasing AND that the difference is between 1 and 3
        return all(-3 <= x <= -1 for x in diffs) or all(1 <= x <= 3 for x in diffs)

    def part2(self):
        count = 0        
        lines = (list(map(int, x.split())) for x in self.input_data.splitlines())
        
        for line in lines:
            # We just have to try by removing one element at a time and checking if the line is valid
            permitations = [line[:i] + line[i+1:] for i in range(len(line))]
            for p in permitations:
                if self.get_diffs(p):
                    count += 1
                    break
        return count
```
Part 2 just runs the get_diffs code on every permetation of the input line, first the original, then with the first element removed, then the second etc. As soon as one is valid it starts procsessing the next.


## Benchmark 1000 Iterations

| Part   | Avg Time | Median   | 95th %ile | 99th %ile | Unit |
|--------|----------|----------|-----------|-----------|------|
| Part 1 | 1.626493 | 1.994371 | 2.019882  | 2.117863  | ms   |
| Part 2 | 4.242305 | 4.004240 | 5.006778  | 5.026813  | ms   |
