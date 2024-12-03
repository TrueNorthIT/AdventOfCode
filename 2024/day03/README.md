# Day 03


## Solutions:

### Part 1:

#### Solution

```python
    mult_regex = "mul\(\d{1,3},\d{1,3}\)"

    def prod_of_simple_mult_string(self, capture):
        return sum(math.prod(extract_ints_from_string(instruction)) for instruction in re.findall(self.mult_regex, capture))

    def part1(self):
        return self.prod_of_simple_mult_string(self.input_data)
```

### Part 2:

#### Solution
```python
    disregard_mult_regex = "don't\(\).*?mul\(\d{1,3},\d{1,3}\).*?(?:do\(\)|$)"
    mult_regex = "mul\(\d{1,3},\d{1,3}\)"

    def prod_of_simple_mult_string(self, capture):
        return sum(math.prod(extract_ints_from_string(instruction)) for instruction in re.findall(self.mult_regex, capture))

    def part2(self):
        doctored_input = re.sub(self.disregard_mult_regex, "", self.input_data.replace("\n", ""))
        return self.prod_of_simple_mult_string(doctored_input)
```

Replace all strings that are are surronded in don't() and do() or the end of the input, then run the `prod_of_simple_mult_string` function

##### GOTCHYAS! 

The input has newlines in it, since my disregard regex looks for the end of line ($) this was returrning many false positives. Took me ages to figure it out but the `.replace("\n", "")` fixed it


## Benchmark 1000 Iterations

| Part   | Avg Time     | Median     | 95th %ile | 99th %ile | Unit |
|--------|--------------|------------|-----------|-----------|------|
| Part 1 | 897.588730 µs | 999.450684 µs | 1.022100 µs  | 1.090782 µs  | µs  |
| Part 2 | 457.984924 µs | 0.000000 µs   | 1.019239 µs  | 1.069536 µs  | µs  |
