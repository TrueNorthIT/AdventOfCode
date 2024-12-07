# Day 07

## Solutions:

#### Solution

```python
    def can_values_reach_target(self, target: int, values: Tuple[int], current: int, digit_lengths,  part2=False):
        length = len(values)

        def helper(current, index):
            if index == length:
                return current == target
            if current > target:
                return False

            # Add, multiply, and concatenate
            if helper(current + values[index], index + 1):
                return True
            if helper(current * values[index], index + 1):
                return True
            if part2 and helper(current * (10**digit_lengths[index]) + values[index], index + 1):
                return True

            return False

        return helper(current, 0)
```

## Benchmark 100 Iterations

| Part   | Avg Time  | Median    | 95th %ile | 99th %ile | Unit |
|--------|-----------|-----------|-----------|-----------|------|
| Part 1 | 2.716922  | 2.258717  | 6.530397  | 7.802292  | s    |
| Part 2 | 6.679797  | 6.608963  | 7.748628  | 10.149164 | ms   |
