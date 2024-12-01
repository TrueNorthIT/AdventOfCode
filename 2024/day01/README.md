# Day 01


## Solutions:

### Part 1:

#### Initial Solution
```python
   def part1(self):
        L1, L2 = self.parse_input()
        total = 0
        while L1:
            x = min(L1)
            y = min(L2)
            L1.remove(x)
            L2.remove(y)
            # We only care about the distance between them, so use abs to negate any +- 
            total += abs(x - y)
        return total
```
On a second look i realised if we itterate over the sorted lists we don't need to mins. Zip is great for itterating over two lists at once.

#### Refactored Solution

```python
    def part1(self):
        L1, L2 = self.parse_input()
        return sum(abs(x - y) for x, y in zip(sorted(L1), sorted(L2)))
```

### Part 2:

#### Initial Solution
```python
    def part2(self):

        L1, L2 = self.parse_input()
        total_similarity = 0

        for i in L1:
            count = L2.count(i)
            total_similarity += i * count

        return total_similarity
```
No real imporvement made in the refactor, just condensed into a list comprehension

#### Refactored Solution

```python
    def part2(self):
        L1, L2 = self.parse_input()
        return sum([i * L2.count(i) for i in L1])
```

## Benchmark 1000 Iterations

| Part   | Avg Time   | Median     | 95th %ile | 99th %ile | Unit |
|--------|------------|------------|-----------|-----------|------|
| Part 1 | 548.262119 | 972.270966 | 1.052821  | 1.428754  | µs   |
| Part 2 | 5.859317   | 5.999088   | 7.007957  | 9.008093  | ms   |
