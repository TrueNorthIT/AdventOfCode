from collections import defaultdict
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

class Day09Solver(JoesAoCSolver):

    def parse_input(self) -> tuple[dict[int, int], dict[int, list[int]]]:
        files = self.input_data[0::2]
        file_dict = defaultdict(int)
        for index, file_length in enumerate(files):
            file_dict[index] = int(file_length)

        empty_space = self.input_data[1::2]
        space_dict = {}
        for index, space in enumerate(empty_space):
            space_dict[index] = [int(space), []]
        
        
        return file_dict, space_dict

    def part1(self):
        file_dict, space_dict = self.parse_input()
        current_free_block = 0
        for file, file_size in sorted(file_dict.items(), reverse=True):
            current_file_size = file_size
            while current_file_size > 0 and current_free_block < len(space_dict):
                if current_free_block > file:
                    # We don't want to move data after where it currently is
                    break

                remaining_space = space_dict[current_free_block][0]  # Get the available space in the current block

                # Determine how much space to use in this block
                to_fill = min(current_file_size, remaining_space)

                # Update the block and file size
                space_dict[current_free_block][1].extend([file] * to_fill)
                space_dict[current_free_block][0] -= to_fill
                current_file_size -= to_fill

                # Now let's clear that many from the file_dict
                file_dict[file] -= to_fill

                # Move to the next block if this one is full
                if space_dict[current_free_block][0] == 0:
                    current_free_block += 1


        final_drive = []

        for key, value in space_dict.items():
            final_drive.extend([key] * file_dict[key])
            final_drive.extend(value[1])

        print(final_drive)#

        # Final score is the sum of index * value for each file in the final drive
        return sum(i * value for i, value in enumerate(final_drive))


    def part1_examples(self):
        return [("2333133121414131402", 1928)]
    
    def build_drive(self, file_dict, space_dict):
        final_drive = []
        for key, value in file_dict.items():
            final_drive.extend([chr(key)] * value)
            if key in space_dict:
                final_drive.extend([chr(ord("."))] * space_dict[key][0])
        return "".join(final_drive)
    
    def print_drive(self, drive):
        print("".join(map(lambda x: str(ord(x)) if not x == '.' else '.', drive)))

    def part2(self):            
        def swap_substrings(s: str, val1: str, val2: str) -> str:
            idx1, idx2 = s.find(val1), s.find(val2)
            if idx1 == -1 or idx2 == -1: return s
            if idx1 < idx2: return s
            return s[:idx2] + val1 + s[idx2 + len(val2):idx1] + val2 + s[idx1 + len(val1):]

        file_dict, space_dict = self.parse_input()
        initial_drive = self.build_drive(file_dict, space_dict)
        drive_string = self.build_drive(file_dict, space_dict)
        self.print_drive(drive_string)

        for file_index, file_size in sorted(file_dict.items(), reverse=True):
            file = str(chr(file_index)) * file_size
            empty_space = "." * file_size * len(str(file_index))
            drive_string = swap_substrings(drive_string, file,  empty_space)

        self.print_drive(drive_string)

        # If they are a different length, something went wrong!
        assert len(drive_string) == len(initial_drive)
        
        # Final score is the sum of index * value for each file in the final drive
        total = 0
        for i, value in enumerate(drive_string):
            if value != ".":
                print(f"{i} * {ord(value)} = {i * int(ord(value))}")
                total += i * int(ord(value))
        return total


    def part2_examples(self):
        return [("243313312141413140202", 2858)]




if __name__ == "__main__":
    solver = Day09Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
    