# Day 05
## Solutions:

### Part 1:

#### Solution

```python
    def is_queue_sorted(self, rules, queue):
        # The any is checking if a page that should be before the current page is in the queue AFTER the current page, if so, the queue is not sorted 
        # not any lets us break out of the loop as soon as we find a page that is out of order
        return not any(
            must_be_before_page in queue[:page_index]
            for page_index, page in enumerate(queue)
            for must_be_before_page in rules[page]
        )
    
    def part1(self):
        rules, queues = self.parse_input()
        return sum(queue[len(queue) // 2] for queue in queues if self.is_queue_sorted(rules, queue))
```

Checks that for all pages in the queue 
 
### Part 2:

#### Solution
```python
   def is_queue_sorted(self, rules, queue):
        return not any( must_be_before_page in queue[:page_index] for page_index, page in enumerate(queue) for must_be_before_page in rules[page])
        
    # Orders the queue by recursively swapping elements that are out of order based on the rules
    def order_queue(self, rules, queue, depth=0):
        for page_index, page in enumerate(queue):
            for must_be_before_page in rules[page]:
                if must_be_before_page in queue[:page_index]:
                    correct_position = queue.index(must_be_before_page)
                    queue[page_index], queue[correct_position] = queue[correct_position], queue[page_index]
                    break # We only need to swap one element at a time for each rule
            
        if not self.is_queue_sorted(rules, queue):
            return self.order_queue(rules, queue, depth=depth+1)
        return queue
    
    def part2(self):
        rules, queues = self.parse_input()        
        return sum(self.order_queue(rules, queue)[len(queue) // 2] for queue in queues if not self.is_queue_sorted(rules, queue))
```
And for part 2 we recursivly swap un-ordered elements until it's sorted!


## Benchmark 1000 Iterations

| Part   | Avg Time   | Median     | 95th %ile  | 99th %ile   | Unit |
|--------|------------|------------|------------|-------------|------|
| Part 1 | 5.848822   | 5.677938   | 7.577395   | 9.034052    | ms   |
| Part 2 | 50.559352  | 47.520161  | 72.332811  | 101.686089  | ms   |
