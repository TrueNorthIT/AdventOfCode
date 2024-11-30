import sys
import time
from pathlib import Path
from prettytable import PrettyTable


def run_solver(solver_class, input_file):
    solver = solver_class(input_file=input_file)
    start_time = time.time()
    try:
        part1_result = solver.part1()
        part1_time = time.time() - start_time
    except Exception as e:
        part1_result = f"Error: {e}"
        part1_time = "-"
    
    start_time = time.time()
    try:
        part2_result = solver.part2()
        part2_time = time.time() - start_time
    except Exception as e:
        part2_result = f"Error: {e}"
        part2_time = "-"
    
    return part1_result, f"{part1_time:.4f}s", part2_result, f"{part2_time:.4f}s"


def discover_solvers(base_dir):
    base_path = Path(base_dir)
    solvers = {}
    sys.path.append(str(base_path))  # Add the base path to the system path

    for day_dir in sorted(base_path.iterdir()):
        if day_dir.is_dir() and (day_dir / "solve.py").exists():
            day_name = day_dir.name
            try:
                solver_module = __import__(f"{day_name}.solve", fromlist=["solve"])
                SolverClass = next(
                    cls for name, cls in vars(solver_module).items()
                    if isinstance(cls, type) and issubclass(cls, solver_module.JoesAoCSolver)
                    and cls is not solver_module.JoesAoCSolver
                )
                input_file = day_dir / "input.txt"  # Correctly resolve the input file path
                solvers[day_name] = (SolverClass, input_file)
            except Exception as e:
                solvers[day_name] = (None, None, str(e))
    
    return solvers


def run_all_days():
    solvers = discover_solvers("2024")
    results = []

    for day, (solver_class, input_file) in sorted(solvers.items()):
        if solver_class is None:
            results.append((day, "Error", "-", "Error", "-", input_file))
            continue

        if not input_file.exists():
            results.append((day, "Input Missing", "-", "Input Missing", "-"))
            continue

        part1_result, part1_time, part2_result, part2_time = run_solver(solver_class, input_file)
        results.append((day, part1_result, part1_time, part2_result, part2_time))

    return results


if __name__ == "__main__":
    days_results = run_all_days()

    table = PrettyTable()
    table.field_names = ["Day", "Part 1 Result", "Part 1 Time", "Part 2 Result", "Part 2 Time"]

    for result in days_results:
        table.add_row(result)

    print(table)
