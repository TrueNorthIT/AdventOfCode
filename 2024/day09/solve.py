from collections import defaultdict
import sys; from pathlib import Path; sys.path.append(str(Path(__file__).resolve().parent.parent)); from JoesAoCSolver import JoesAoCSolver

class Day09Solver(JoesAoCSolver):

    def parse_input(self) -> tuple[dict[int, int], dict[int, list[int]]]:
        files = self.input_data[0::2]
        file_dict = {}
        for index, file_length in enumerate(files):
            file_dict[index] = int(file_length)

        empty_space = self.input_data[1::2]
        space_dict = {}
        for index, space in enumerate(empty_space):
            space_dict[index] = [int(space), []]

        
        print(file_dict, space_dict)
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
            final_drive.extend([key] * value)
            try:
                final_drive.extend(space_dict[key][1])
                final_drive.extend(["."] * space_dict[key][0])
            except KeyError:
                pass
        return final_drive

    def part2(self):
        file_dict, space_dict = self.parse_input()

        initial_drive = self.build_drive(file_dict, space_dict)
        print("".join(map(str, initial_drive)))

        for file, file_repeat in sorted(file_dict.items(), reverse=True):
            for block, (space, _) in sorted(space_dict.items()):
                if block > file:
                    break  # Don't move data past its current position
                file_size = len(str(file) * file_repeat)
                if space >= file_size:
                    space_dict[block][1].extend([file] * file_size)
                    space_dict[block][0] -= file_size
                    file_dict[file] = 0
                    if file in space_dict:
                        if file_size == 1 and file-1 in space_dict:
                            space_dict[file-1][0] += file_size
                        else:
                            space_dict[file][0] += file_size
                    else:
                        space_dict[file] = [file_size, []]
                    break

        final_drive = self.build_drive(file_dict, space_dict)
        print("".join(map(str, final_drive)))
        return sum(i * value for i, value in enumerate(final_drive) if value != ".")


    def part2_examples(self):
        return [
            ("2333133121414131402", 2858),
            # ("12345", 79), # 0..111....22222
            # ("233313312", 414)
        ]




if __name__ == "__main__":
    solver = Day09Solver()
    # solver.run("assertions")
    solver.run("real")
    # solver.benchmark(1000)
    