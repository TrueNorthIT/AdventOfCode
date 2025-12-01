import time
from pathlib import Path
from typing import Optional, Any, List, Tuple, Callable
import inspect
from prettytable import PrettyTable
from colorama import Fore, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)

import statistics
from typing import Dict


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
        """
        Times the execution of the given function and returns its result and the elapsed time.
        """
        start_time = time.time()
        result = func()  # Capture the result of the function
        elapsed_time = time.time() - start_time
        return result, elapsed_time


    def benchmark(self, times: int = 100):
        self.log(f"Benchmarking Part 1 and Part 2 with {times} iterations...", "INFO")
        results: Dict[str, List[float]] = {"Part 1": [], "Part 2": []}

        # Run benchmarks for Part 1
        if hasattr(self, "part1"):
            for _ in range(times):
                _, elapsed_time = self.time_function(self.part1)
                results["Part 1"].append(elapsed_time)

        # Run benchmarks for Part 2
        if hasattr(self, "part2"):
            for _ in range(times):
                _, elapsed_time = self.time_function(self.part2)
                results["Part 2"].append(elapsed_time)

        # Analyze results
        self.log("Benchmarking complete. Analyzing results...", "INFO")
        print("=" * 50)
        print(f"{Fore.CYAN}{Style.BRIGHT}Benchmark Results for {self.day}")
        print("=" * 50)

        def adjust_units(value: float) -> Tuple[float, str]:
            if value >= 1:
                return value, "s"
            elif value >= 1e-3:
                return value * 1e3, "ms"
            elif value >= 1e-6:
                return value * 1e6, "µs"
            else:
                return value * 1e9, "ns"

        table = PrettyTable()
        table.field_names = ["Part", "Avg Time", "Median", "95th %ile", "99th %ile", "Unit"]

        for part, timings in results.items():
            avg_time = statistics.mean(timings)
            median_time = statistics.median(timings)
            p95 = statistics.quantiles(timings, n=100)[94]  
            p99 = statistics.quantiles(timings, n=100)[98] 

            # Adjust units
            avg_time, unit = adjust_units(avg_time)
            median_time, _ = adjust_units(median_time)
            p95, _ = adjust_units(p95)
            p99, _ = adjust_units(p99)

            table.add_row([part, f"{avg_time:.6f}", f"{median_time:.6f}", f"{p95:.6f}", f"{p99:.6f}", unit])

        print(table)


    def run_phase(
        self,
        phase_name: str,
        solver: Callable[[], Any],
        examples: List[Tuple[str, Any]],
        run_assertions: bool,
        run_real: bool,
    ):
        if run_assertions:
            self.log(f"Testing {phase_name} Examples...", "INFO")
            if examples:
                self.run_examples(examples, solver)
            self.log(f"{phase_name} Examples Passed!", "SUCCESS")

        if run_real:
            result, elapsed_time = self.time_function(solver)
            self.log(f"{phase_name} Result: {result} (took {elapsed_time:.4f} seconds)", "SUCCESS")
            print()

    def run_examples(self, examples: List[Tuple[str, Any]], solver: Callable[[str], Any]):
        original_input_data = self.input_data
        table = PrettyTable()
        table.field_names = ["Example Input", "Expected Output", "Actual Output", "Status"]
        for i, (example_input, expected_output) in enumerate(examples, start=1):
            self.input_data = example_input
            actual_output = solver()
            status = "PASS" if actual_output == expected_output else "FAIL"
            color = "SUCCESS" if status == "PASS" else "ERROR"
            table.add_row([example_input, expected_output, actual_output, status])
            self.log(f"Example {i}: {status}", color)
            if status == "FAIL":
                self.input_data = original_input_data
                raise AssertionError(
                    f"Example {i} failed: input={example_input}, expected={expected_output}, got={actual_output}"
                )
        self.input_data = original_input_data
        print(table)

    def run(self, run_mode: str = "both"):
        run_assertions = run_mode in {"both", "assertions"}
        run_real = run_mode in {"both", "real"}

        self.log(f"Advent of Code - {self.day}", "INFO")
        print("=" * 40)
        try:
            self.run_phase("Part 1", self.part1, self.part1_examples(), run_assertions, run_real)
        except NotImplementedError:
            self.log("Part 1: Not implemented.", "WARNING")
        except AssertionError as e:
            self.log(f"Part 1: Example Test Failed - {e}", "ERROR")
        except Exception as e:
            self.log(f"Part 1: Error - {e}", "ERROR")
            raise e

        print("-" * 40)

        try:
            self.run_phase("Part 2", self.part2, self.part2_examples(), run_assertions, run_real)
        except NotImplementedError:
            self.log("Part 2: Not implemented.", "WARNING")
        except AssertionError as e:
            self.log(f"Part 2: Example Test Failed - {e}", "ERROR")
        except Exception as e:
            self.log(f"Part 2: Error - {e}", "ERROR")
            raise e

        print("=" * 40)

    def part1_examples(self) -> List[Tuple[str, Any]]:
        return []

    def part2_examples(self) -> List[Tuple[str, Any]]:
        return []
