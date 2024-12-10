# Day 09

## BY FAR my worst AOC performance :) 

## Solutions:

#### Part 1 Solution


```python
    def part1(self):
        files, empty_space = self.parse_input()
        
        for index in sorted(files.keys(), reverse=True):
            file_start_pos, file_len = files[index]
            remaining_file_len = file_len
            current_pos = file_start_pos
        
            new_file_positions = []

            while remaining_file_len > 0:
                # Dynamically create a list of possible gaps (to the left of the file's current position)
                possible_gaps = sorted(
                    [[empty_space[gap_len][0], gap_len] for gap_len in empty_space if gap_len > 0 and empty_space[gap_len][0] < current_pos]
                )
                
                if not possible_gaps:
                    # No more gaps available; keep the remaining part of the file in its original position
                    new_file_positions.append((current_pos, remaining_file_len))
                    break

                # Pick the leftmost gap
                gap_start_pos, gap_len = possible_gaps[0]

                # Calculate how much of the file can fit in the current gap
                used_space = min(remaining_file_len, gap_len)
                new_file_positions.append((gap_start_pos, used_space))
                
                remaining_file_len -= used_space
                remaining_gap_len = gap_len - used_space
                
                # Update the empty space data structure
                heapq.heappop(empty_space[gap_len])
                if not empty_space[gap_len]:
                    del empty_space[gap_len]
                if remaining_gap_len > 0:
                    heapq.heappush(empty_space[remaining_gap_len], gap_start_pos + used_space)
                
                

            # Update the file position in `files` to reflect the new (potentially split) positions
            files[index] = new_file_positions
            
        checksum = 0
        for index, file_parts in files.items():
            for file_start_pos, file_len in file_parts:
                for j in range(file_len):
                    checksum += index * (file_start_pos + j)

        return checksum
```

The heap lets us quickly find and update the smallest gaps

#### Part 2 Solution

``` python

```def part2(self):
        files, empty_space = self.parse_input()
        
        
        for index in sorted(files.keys(),reverse=True):
            
            file_start_pos, file_len = files[index]            
            
            # Get the first gap that is big enough to fit the file that is after the file, or None
            possible_gaps = sorted([[empty_space[gap_len][0],gap_len] for gap_len in empty_space if gap_len>=file_len and file_start_pos > empty_space[gap_len][0]])

            if possible_gaps:
                gap_start_pos, gap_len = possible_gaps[0]
                # Remap the file to the gap
                files[index] = [gap_start_pos,file_len]
                # Remove the amount of space that the file takes up from the gap
                remaining_gap_len = gap_len-file_len
                heapq.heappop(empty_space[gap_len])
                if not empty_space[gap_len]:
                    del empty_space[gap_len]
                if remaining_gap_len:
                    heapq.heappush(empty_space[remaining_gap_len],gap_start_pos+file_len)
                    
            

        checksum = 0 
        for index, (file_start_pos, file_len) in files.items():
            for j in range(file_len):
                checksum += index * (file_start_pos + j)
                
        return checksum
```

Part 2 here looks so so simple! This is like my 8th attempt 🤦. The heaps really help. Also just keeping track of the file start position is so much better than what i was originally doing

## Benchmark 1000 Iterations (PyPy)

| Part   | Avg Time   | Median    | 95th %ile | 99th %ile | Unit |
|--------|------------|-----------|-----------|-----------|------|
| Part 1 | 29.501684  | 27.070642 | 40.897214 | 57.197785 | ms   |
| Part 2 | 12.022142  | 10.398984 | 19.481170 | 27.977397 | ms   |
