"""Offline self-check: python tests/test_build.py (no network, no pytest)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import build_readme as br
from leaderboard_model import Leaderboard

board = Leaderboard.from_dict(json.loads((ROOT / "tests" / "fixture_leaderboard.json").read_text(encoding="utf-8")))

# Race chart: rebuilt final score must equal the API's local_score
series = br.score_series(board)
for m in board.members.values():
    assert series[m.id][-1][1] == m.local_score, (m.name, series[m.id], m.local_score)
    assert [p[0] for p in series[m.id]] == sorted(p[0] for p in series[m.id]), m.name
assert series[1004] == [[series[1004][0][0], 0]]  # no stars: flat line from day 1 unlock

# Achievements: stub git so Polyglot is offline and deterministic
br.BRANCH_MAPPING = {"1001": "alice-example", "1002": "bob-example"}
files = {"alice-example": ["2025/day01/a.py", "2025/day02/b.cs", "2025/day03/c.rs", "2025/README.md"],
         "bob-example": ["2025/day01/a.py"]}
br.git_list_year_files = lambda branch, year, repo_root: files.get(branch, [])

ach = {a["title"].split()[0]: [(e["name"].split()[0], e["value"]) for e in a["entries"]]
       for a in br.compute_achievements(board)}
assert ach == {
    "Polyglot": [("Alice", "3"), ("Bob", "1")],
    "Early": [("Carol", "3m"), ("Alice", "5m"), ("Bob", "10m")],
    "You": [("Bob", "2m"), ("Carol", "6m"), ("Alice", "10m")],
    "Hackerman": [("Alice", "16"), ("Bob", "13"), ("Carol", "12")],
}, ach

print("OK: score series matches local_score for", len(board.members), "members; achievements in expected order")
