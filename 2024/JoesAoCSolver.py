import time
from pathlib import Path
from typing import Optional, Any, List, Tuple, Callable
import inspect
from prettytable import PrettyTable
from colorama import Fore, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)


class JoesAoCSolver:
    TRACE_LEVELS = {
        "INFO": Fore.BLUE,
        "DEBUG": Fore.CYAN,
        "SUCCESS": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
    }

    def __init__(self, input_file: Optional[str] = None, trace_level: str = "INFO"):
        self.trace_level = trace_level.upper()
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        if module is None or not hasattr(module, "__file__"):
            raise RuntimeError("Could not determine the calling script location.")
        self.script_path = Path(module.__file__).resolve()
        self.day = self.script_path.parent.name

        self.input_file = (
            Path(input_file).resolve() if input_file else self.script_path.parent / "input.txt"
        )
        self.input_data = self.read_input()

    def log(self, message: str, level: str = "INFO"):
        if self.TRACE_LEVELS.get(level.upper()):
            print(f"{self.TRACE_LEVELS[level.upper()]}[{level.upper()}] {message}")
        else:
            print(f"[{level.upper()}] {message}")

    def read_input(self) -> str:
        input_path = self.input_file
        self.log(f"Reading input from {input_path.absolute()}", "DEBUG")
        if not input_path.exists():
            self.log(f"Input file not found: {input_path}", "ERROR")
            raise FileNotFoundError(f"Input file not found: {input_path}")
        with open(input_path, "r") as f:
            return f.read().strip()

    def part1(self) -> Any:
        raise NotImplementedError("Part 1 solution must be implemented.")

    def part2(self) -> Any:
        raise NotImplementedError("Part 2 solution must be implemented.")

    def time_function(self, func: Callable[[], Any]) -> Tuple[Any, float]:
        start_time = time.time()
        result = func()
        elapsed_time = time.time() - start_time
        return result, elapsed_time

    def assert_examples(self, examples: List[Tuple[str, Any]], solver: Callable[[str], Any]):
        table = PrettyTable()
        table.field_names = ["Example Input", "Expected Output", "Actual Output", "Status"]
        for i, (example_input, expected_output) in enumerate(examples, start=1):
            actual_output = solver(example_input)
            status = "PASS" if actual_output == expected_output else "FAIL"
            color = "SUCCESS" if status == "PASS" else "ERROR"
            table.add_row([example_input, expected_output, actual_output, status])
            self.log(f"Example {i}: {status}", color)
            if status == "FAIL":
                raise AssertionError(
                    f"Example {i} failed: input={example_input}, expected={expected_output}, got={actual_output}"
                )
        print(table)

    def run(self):
        self.log(f"Advent of Code - {self.day}", "INFO")
        print("=" * 40)

        try:
            self.log("Testing Part 1 Examples...", "INFO")
            self.assert_examples(self.part1_examples(), lambda inp: self.part1_on_input(inp))
            self.log("Part 1 Examples Passed!", "SUCCESS")
            part1_result, part1_time = self.time_function(self.part1)
            print("\n")
            self.log(f"Part 1 Result: {part1_result} (took {part1_time:.4f} seconds)", "SUCCESS")
        except NotImplementedError:
            self.log("Part 1: Not implemented.", "WARNING")
        except AssertionError as e:
            self.log(f"Part 1: Example Test Failed - {e}", "ERROR")
        except Exception as e:
            self.log(f"Part 1: Error - {e}", "ERROR")

        print("-" * 40)

        try:
            self.log("Testing Part 2 Examples...", "INFO")
            self.assert_examples(self.part2_examples(), lambda inp: self.part2_on_input(inp))
            self.log("Part 2 Examples Passed!", "SUCCESS")
            part2_result, part2_time = self.time_function(self.part2)
            print("\n")
            self.log(f"Part 2 Result: {part2_result} (took {part2_time:.4f} seconds)", "SUCCESS")
        except NotImplementedError:
            self.log("Part 2: Not implemented.", "WARNING")
        except AssertionError as e:
            self.log(f"Part 2: Example Test Failed - {e}", "ERROR")
        except Exception as e:
            self.log(f"Part 2: Error - {e}", "ERROR")

        print("=" * 40)

    def part1_on_input(self, input_data: str) -> Any:
        self.input_data = input_data
        return self.part1()

    def part2_on_input(self, input_data: str) -> Any:
        self.input_data = input_data
        return self.part2()

    def part1_examples(self) -> List[Tuple[str, Any]]:
        return []

    def part2_examples(self) -> List[Tuple[str, Any]]:
        return []
