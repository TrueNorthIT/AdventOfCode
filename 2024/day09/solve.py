from collections import defaultdict
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver


class Block:
    def __init__(self, size: int):
        self.size = size
        self.remaining_space = size
        self.files = []

    def has_files(self) -> bool:
        return len(self.files) > 0

    def can_fit(self, file_size: int) -> bool:
        return file_size <= self.remaining_space

    def add_file(self, file: list[int]):
        self.files.extend(file)
        self.remaining_space -= len(file)

    def file_size(self) -> int:
        return len(self.files)

    def pop_num(self, num: int):
        popped = self.files[:num]
        self.files = self.files[num:]
        self.remaining_space += num
        return popped

    def __repr__(self):
        return "".join(map(str, self.files)) + "." * self.remaining_space

class Day09Solver(JoesAoCSolver):

    def parse_input(self) -> list[Block]:

        hard_drive = []

        for i, value in enumerate(self.input_data.rstrip()):
            if i % 2 == 0:
                # This is a file
                file = Block(int(value))
                file.add_file([i//2] * int(value))
                hard_drive.append(file)
            else:
                # This is a space
                space = Block(int(value))
                hard_drive.append(space)


        return hard_drive

    def part1(self):
        hard_drive = self.parse_input()
        # Start from the rightmost block and move files left
        space_index = 0
        for block in hard_drive[::-1]:  # Process blocks from right to left
            print(f"Processing block: {block}")
            while block.has_files():
                print(f"Processing file in block: {block.files}")
                # Skip to the next free space if the current space is full
                while space_index < len(hard_drive) and hard_drive[space_index].remaining_space == 0:
                    print(f"Block {hard_drive[space_index]} is full, moving to the next block.")
                    space_index += 1
                
                # If space_index exceeds the array length, no more free space is available
                if space_index >= len(hard_drive):
                    print("Error: No more free space available.")
                    return
                
                # Move as many files as possible into the current free space
                to_add = min(hard_drive[space_index].remaining_space, block.file_size())
                moved_files = block.pop_num(to_add)  # Get the files being moved
                hard_drive[space_index].add_file(moved_files)  # Move the files
                print(f"Moved {moved_files} to block {space_index}.")
                print(f"Updated block {space_index}: {hard_drive[space_index]}")
                print(f"Remaining files in current block: {block}")

        print("Final state of hard drive:")
        print("".join(map(str, hard_drive)))

    def part1_examples(self):
        return [("2333133121414131402", 1928)]
    
    # def build_drive(self, file_dict, space_dict):
    #     final_drive = []
    #     for key, value in file_dict.items():
    #         final_drive.extend([chr(key)] * value)
    #         if key in space_dict:
    #             final_drive.extend([chr(ord("."))] * space_dict[key][0])
    #             if space_dict[key][0] == 0:
    #                 print("YEEHAW")
    #                 final_drive.extend(chr(ord("!"))) # This is a separator
    #     return "".join(final_drive)
    
    # def parse_drive(self, drive):
    #     # Need to also support the separator !
    #     def parse(x):
    #         if x == "!":
    #             return "!"
    #         if x == ".":
    #             return "."
    #         return str(ord(x))
    #     return "".join(map(parse, drive))

    # def part2(self):            
    #     def swap_substrings(s: str, file: str, space: str) -> tuple[bool,str]:
    #         idx2 = s.find(space)
    #         # We want the last index of the file
    #         idx1 = s.rfind(file)
            
    #         if idx1 == -1 or idx2 == -1: return False, s
    #         if idx1 < idx2: return False, s
    #         return True, s[:idx2] + file + s[idx2 + len(space):idx1] + space + s[idx1 + len(file):]

    #     file_dict, space_dict = self.parse_input()
    #     initial_drive = self.build_drive(file_dict, space_dict)
    #     drive_string = self.build_drive(file_dict, space_dict)
        
        
    #     prev_drive_string = self.parse_drive(drive_string)
    #     print(prev_drive_string)    
        
    #     for file_index, file_size in sorted(file_dict.items(), reverse=True):
    #         # print(f"Trying to move file {file_index} of size {file_size}")
    #         file = str(chr(file_index)) * file_size
    #         empty_space = "." * file_size * len(str(file_index))
    #         did_swap, drive_string = swap_substrings(drive_string, file,  empty_space)
    #         # Print the drive string and prev_drive_string with the differences highlighted in green
    #         # if did_swap:
    #         #     diffs = [f"\033[42m{c1}\033[0m" if c1 != c2 else c1 for c1, c2 in zip(self.parse_drive(drive_string), prev_drive_string)]
    #         #     # Can we make an 'animation' of this,
    #         #     # print("".join(diffs))


    #         prev_drive_string = self.parse_drive(drive_string)

    #     self.parse_drive(drive_string)

    #     # If they are a different length, something went wrong!
    #     assert len(drive_string) == len(initial_drive)
        
    #     # Final score is the sum of index * value for each file in the final drive
    #     total = 0
    #     for i, value in enumerate(drive_string):
    #         if value != "." and value != "!":
    #             # print(f"{i} * {ord(value)} = {i * int(ord(value))}")
    #             total += i * int(ord(value))
    #     return total


    # def part2_examples(self):
    #     return [
    #         ("101", 2858),
    #         ("1313165", 169)
    #     ]


# Part 2: 6363268339304
# Part 2: 14200825782129

if __name__ == "__main__":
    solver = Day09Solver()
    solver.run("assertions")
    # solver.run("real")
    # solver.benchmark(1000)
    