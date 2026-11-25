import os
from leaderboard_model import Leaderboard
from datetime import datetime, timezone
from typing import Dict, Tuple
from tabulate import tabulate
import requests
import json

import subprocess
import sys
import argparse
from pathlib import Path

EXT_TO_LANG = {
    ".py": "Python",
    ".cs": "C#",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".rs": "Rust",
    ".go": "Go",
    ".rb": "Ruby",
    ".kt": "Kotlin",
    ".java": "Java",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".c": "C",
    ".fs": "F#",
    ".fsx": "F#",
    ".hs": "Haskell",
    ".php": "PHP",
    ".swift": "Swift",
    ".scala": "Scala",
    ".jl": "Julia",
    ".xlsx": "Excel",
    ".ps1": "PowerShell",
    ".sql": "SQL",
    ".vb": "VB.NET",
    ".vbs": "VBScript",
    ".xslt": "XSLT",
    ".sh": "Bash",
    ".asm": "Assembly",
    ".powerautomate": "PowerAutomate",
    ".gd": "Godot"
}



# Constants
YEAR = 2025  # current competition year: the only year that updates README and the webhook
LEADERBOARD_URL = "https://adventofcode.com/{year}/leaderboard/private/view/353270.json"
DATA_DIR = Path("docs/data")

BRANCH_MAPPING = {
    "1427047": "christian-waters",
    "353270": "joe-pitts",
    "4472230": "josh-cottrell",
    "4947218": "alex-radice",
    "4264967": "rich-kelsey",
    "4265041": "kade-hennessy",
    "5105599": "sam-hatts",
    "5156198": "bogdan-michon",
    "5175448": "muhamad-hewa-rahim",
}
    

# Secrets come from the environment and are only needed for a live fetch (checked in main)
SESSION_COOKIE = os.getenv("SESSION_COOKIE")
WEBHOOK_ENDPOINT = os.getenv("WEBHOOK_ENDPOINT")

def git_list_year_files(branch: str, year: int, repo_root: Path) -> list[str]:
    """
    Return all tracked file paths under <year>/ for the given branch,
    e.g. '2024/day01/solution.py'.
    """
    ref = f"origin/{branch}"  # <-- IMPORTANT

    cmd = [
        "git", "ls-tree", "-r", "--name-only",
        ref, "--", str(year)
    ]
    try:
        result = subprocess.run(
            cmd,
            cwd=repo_root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Warning: failed to list files for branch {branch}: {e.stderr.strip()}")
        return []

    files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    return files



def compute_polyglot_scores_git(board: Leaderboard,) -> Dict[str, tuple[int, set[str]]]:
    """
    For each member that has a branch in branch_mapping, look at the files
    under <year>/ on that branch and count distinct languages by extension.

    Returns:
        { member_name: (num_languages, {language_names}) }
    """
    repo_root = Path(".").resolve()

    scores: Dict[str, tuple[int, set[str]]] = {}

    for member in board.members.values():
        member_id_str = str(member.id)
        branch = BRANCH_MAPPING.get(member_id_str)
        if not branch:
            continue  # no branch configured for this member

        file_paths = git_list_year_files(branch, int(board.event), repo_root)
        if not file_paths:
            continue

        langs: set[str] = set()
        for path in file_paths:
            _, ext = os.path.splitext(path)
            lang = EXT_TO_LANG.get(ext.lower())
            if lang:
                langs.add(lang)

        if not langs:
            continue

        name = member.name or member_id_str
        scores[name] = (len(langs), langs)
        print(f"Member {name} uses {len(langs)} languages: {', '.join(sorted(langs))}")

    return scores


def format_duration_full(seconds: int) -> str:
    seconds = int(seconds)

    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    parts = []
    if days: parts.append(f"{days}d")
    if hours: parts.append(f"{hours}h")
    if minutes: parts.append(f"{minutes}m")
    if seconds or not parts: parts.append(f"{seconds}s")

    return " ".join(parts)


# Fetch leaderboard data
def fetch_leaderboard_data(url, session_cookie):
    cookies = {"session": session_cookie}
    response = requests.get(url, cookies=cookies, timeout=60)
    if response.status_code == 200:
        data = response.json()
        return Leaderboard.from_dict(data), data
    else:
        sys.exit(f"Error: Unable to fetch data (status code: {response.status_code})")

# Generate markdown table with hyperlinks   
def generate_markdown_table(data: Leaderboard):
    # Prepare table data
    table_data = []
    headers = ["Rank", "Name", "Local Score", "Stars"] + [str(day) for day in range(1, data.num_days + 1)]

    rank = 1
    for _, details in sorted(data.members.items(), key=lambda x: -x[1].local_score):
        name = details.name
        local_score = details.local_score
        stars = details.stars
        completion = details.completion_day_level
        branch = BRANCH_MAPPING.get(str(details.id), None)

        # Build star progress with hyperlinks
        star_progress = []
        for day in range(1, data.num_days + 1):
            if day in completion:
                stars_for_day = completion[day]
                if 2 in stars_for_day:
                    star_progress.append(f"[★](https://github.com/TrueNorthIT/AdventOfCode/tree/{branch}/{data.event}/day{day:02})")
                elif 1 in stars_for_day:
                    star_progress.append(f"[✩](https://github.com/TrueNorthIT/AdventOfCode/tree/{branch}/{data.event}/day{day:02})")
            else:
                star_progress.append("·")

        table_data.append([rank, name, local_score, stars] + star_progress)
        rank += 1

    # Generate markdown table
    return tabulate(table_data, headers=headers, tablefmt="github")


def fastest_delta_per_member(board: Leaderboard) -> dict[str, tuple[int, int]]:
    result: dict[str, tuple[int, int]] = {}

    for member in board.members.values():
        best_delta: int | None = None
        best_day: int | None = None

        for day, parts in member.completion_day_level.items():
            star1 = parts.get(1)
            star2 = parts.get(2)

            if not (star1 and star2):
                continue

            delta = star2.get_star_ts - star1.get_star_ts
            # Just in case of weird negative timestamps, ignore those
            if delta < 0:
                continue

            if (day != board.num_days):
                if best_delta is None or delta < best_delta:
                    best_delta = delta
                    best_day = day

        if best_delta is not None and best_day is not None:
            key = member.name or str(member.id)
            result[key] = (best_day, best_delta)

    return result

def fastest_p1_per_member(board: Leaderboard) -> Dict[str, Tuple[int, int]]:
    per_member: Dict[str, Tuple[int, int]] = {}

    for member in board.members.values():
        best_delta: int | None = None
        best_day: int | None = None
    
        for day in range(1, board.num_days + 1):
            parts = member.completion_day_level.get(day, {})
            star1 = parts.get(1)
            if not star1:
                continue

            # AoC unlock: midnight US Eastern => 05:00 UTC
            star_release_time = datetime(int(board.event), 12, day, 5, 0, 0, tzinfo=timezone.utc).timestamp()
            time_diff = int(star1.get_star_ts - star_release_time)

            # ignore weird negatives just in case
            if time_diff < 0:
                continue

            if best_delta is None or time_diff < best_delta:
                best_delta = time_diff
                best_day = day

        if best_delta is not None and best_day is not None:
            name = member.name or str(member.id)
            per_member[name] = (best_day, best_delta)

    return per_member



def ordinal(n: int) -> str:
    """Return 1 -> '1st', 2 -> '2nd', etc."""
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

def calculate_hackerman(board):
    hackerman_entries = []
    for member in board.members.values():
        name = member.name or str(member.id)
        if member.local_score > 0:
            hackerman_entries.append((name, member.local_score))
    hackerman_entries.sort(key=lambda x: -x[1])  # highest score first
    return hackerman_entries
def number_of_stars(board):
    starsentries = []
    for member in board.members.values():
        name = member.name or str(member.id)
        if member.local_score > 0:
            starsentries.append((name, member.local_score,member.stars))
    starsentries.sort(key=lambda x: -x[1])  # highest score first
    return starsentries

def compute_achievements(board: Leaderboard) -> list[dict]:
    """
    Ranked achievements, shared by the README table and the site:
    [{"title", "description", "entries": [{"name", "value", "langs"?}]}]
    """
    # --- Polyglot: most distinct languages per member via git ---
    polyglot = sorted(compute_polyglot_scores_git(board).items(), key=lambda x: -x[1][0])
    # --- Early Bird: fastest P1 after unlock ---
    early_bird = sorted(fastest_p1_per_member(board).items(), key=lambda x: x[1][1])
    # --- You Are Gonna Need It: fastest P2-P1 delta ---
    need_it = sorted(fastest_delta_per_member(board).items(), key=lambda x: x[1][1])

    return [
        {"title": "Polyglot 🤓", "description": "Most distinct programming languages used.",
         "entries": [{"name": name, "value": str(count), "langs": sorted(langs)} for name, (count, langs) in polyglot]},
        {"title": "Early Bird ⏰", "description": "Fastest time to complete Star 1 after unlock.",
         "entries": [{"name": name, "value": format_duration_full(delta)} for name, (_day, delta) in early_bird]},
        {"title": "You Are Gonna Need It 🛠️", "description": "Fastest time between Star 1 and Star 2.",
         "entries": [{"name": name, "value": format_duration_full(delta)} for name, (_day, delta) in need_it]},
        # --- Hackerman: local_score (descending) ---
        {"title": "Hackerman 💻", "description": "Highest local score on the private leaderboard.",
         "entries": [{"name": name, "value": str(score)} for name, score in calculate_hackerman(board)]},
    ]


def generate_achievements_table(achievements: list[dict]) -> str:
    max_len = max(len(a["entries"]) for a in achievements)

    # headers: "", "1st", "2nd", ..., "Nth"
    headers = [""] + [ordinal(i) for i in range(1, max_len + 1)]
    rows = []
    for a in achievements:
        cells = []
        for e in a["entries"]:
            if "langs" in e:  # multiline inside <details>
                cells.append(f"<details><summary>{e['name']} ({e['value']})</summary>{'<br>'.join(e['langs'])}</details>")
            else:
                cells.append(f"{e['name']} ({e['value']})")
        cells += [""] * (max_len - len(cells))
        rows.append([f"<details><summary>{a['title']}</summary>{a['description']}<br></details>"] + cells)

    return tabulate(rows, headers=headers, tablefmt="github")


def score_series(board: Leaderboard) -> dict[int, list[list[int]]]:
    """
    Rebuild each member's cumulative local score over time: {member_id: [[timestamp, score], ...]}.
    For each (day, part) the first member to get the star scores N points, the next N-1, and so on,
    where N is the number of members. Starts every line at 0 when day 1 unlocks.
    """
    n = len(board.members)
    events = []  # (ts, member_id, points)
    for day in range(1, board.num_days + 1):
        for part in (1, 2):
            got = sorted(
                (s.get_star_ts, s.star_index, m.id)
                for m in board.members.values()
                if (s := m.completion_day_level.get(day, {}).get(part))
            )
            events += [(ts, mid, n - pos) for pos, (ts, _idx, mid) in enumerate(got)]

    start = int(datetime(int(board.event), 12, 1, 5, tzinfo=timezone.utc).timestamp())
    series = {mid: [[start, 0]] for mid in board.members}
    for ts, mid, points in sorted(events):
        series[mid].append([ts, series[mid][-1][1] + points])

    for m in board.members.values():
        if series[m.id][-1][1] != m.local_score:
            # AoC sometimes zeroes a day's points, so this is a warning, not an error
            print(f"Warning: rebuilt score {series[m.id][-1][1]} != local_score {m.local_score} for member {m.id}")
    return series


def write_site_data(raw: dict, board: Leaderboard, achievements: list[dict]) -> None:
    """Write docs/data/<year>.json (raw AoC JSON plus a "tn" key) and refresh docs/data/years.json."""
    order = [m.id for m in sorted(board.members.values(), key=lambda m: -m.local_score)]  # same order as README
    raw = dict(raw, tn={
        "branches": BRANCH_MAPPING,
        "order": order,
        "achievements": achievements,
        "languages": {e["name"]: e["langs"] for e in achievements[0]["entries"]},
        "series": score_series(board),
    })
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_DIR / f"{board.event}.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(raw, f, ensure_ascii=False, indent=1)
        f.write("\n")
    years = sorted(int(p.stem) for p in DATA_DIR.glob("*.json") if p.stem.isdigit())
    with open(DATA_DIR / "years.json", "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(years) + "\n")


def post_to_haWebhook(leaderboard):
    sortedhackman = number_of_stars(leaderboard)
    webhookstring = str(WEBHOOK_ENDPOINT)
    requests.post(
        "https://ha.tnapps.co.uk/api/webhook/"+webhookstring,
        data=json.dumps(sortedhackman),
        headers={"Content-Type": "application/json"},
        timeout=60
    )

# Main script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build README.md and docs/data from the AoC private leaderboard.")
    parser.add_argument("--year", type=int, default=int(os.getenv("AOC_YEAR") or 0) or None,
                        help=f"year to fetch (default: AOC_YEAR env var, else {YEAR})")
    parser.add_argument("--input", type=Path,
                        help="read the leaderboard JSON from this file instead of fetching it; skips the webhook")
    args = parser.parse_args()

    if args.input:
        raw_data = json.loads(args.input.read_text(encoding="utf-8"))
        leaderboard_data = Leaderboard.from_dict(raw_data)
    else:
        if not SESSION_COOKIE:
            raise ValueError("SESSION_COOKIE is not set. Please provide it as an environment variable.")
        args.year = args.year or YEAR
        if args.year == YEAR and not WEBHOOK_ENDPOINT:
            raise ValueError("WEBHOOK_ENDPOINT is not set. Please provide it as an environment variable.")
        leaderboard_data, raw_data = fetch_leaderboard_data(LEADERBOARD_URL.format(year=args.year), SESSION_COOKIE)
        # Post Leaderboard data to home assitant (current year only, not a backfill)
        if args.year == YEAR:
            post_to_haWebhook(leaderboard_data)

    year = int(leaderboard_data.event)
    if args.year and year != args.year:
        print(f"Warning: --year {args.year} but the data is for {year}; using {year}")

    achievements = compute_achievements(leaderboard_data)
    write_site_data(raw_data, leaderboard_data, achievements)

    # README only tracks the current competition year
    if year == YEAR:
        markdown_table = generate_markdown_table(leaderboard_data)
        achievements_table = generate_achievements_table(achievements)

        with open('README.template', encoding='utf-8') as f:
            readme_stub = f.read()

        # simple replacement, use whatever stand-in value is useful for you.
        readme = readme_stub.replace('{lob}',markdown_table).replace('{ach}', achievements_table)

        with open('README.md','w', encoding='utf-8') as f:
            f.write(readme)
