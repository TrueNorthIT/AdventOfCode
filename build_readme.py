import os
from leaderboard_model import Leaderboard
from datetime import datetime, timezone
from typing import Dict, Tuple
from tabulate import tabulate
import requests
import json

import subprocess
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
    ".fs": "F#",
    ".asm": "Assembly",
    ".powerautomate.json": "Power Automate",
}



# Constants
YEAR = 2025
LEADERBOARD_URL = f"https://adventofcode.com/{YEAR}/leaderboard/private/view/353270.json"

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
    

# Fetch SESSION_COOKIE from environment variables
SESSION_COOKIE = "53616c7465645f5f5750dd84293ff1181dac00b5785c953aef7b1644be3fc4c6e1a78b0f0366b518b9ff3cfdaed5d5b62f56802e395baabb14bb1ba000635cc6" #os.getenv("SESSION_COOKIE")
if not SESSION_COOKIE:
    raise ValueError("SESSION_COOKIE is not set. Please provide it as an environment variable.")

WEBHOOK_ENDPOINT = os.getenv("WEBHOOK_ENDPOINT")
if not WEBHOOK_ENDPOINT:
    raise ValueError("WEBHOOK_ENDPOINT is not set. Please provide it as an environment variable.")

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

        file_paths = git_list_year_files(branch, YEAR, repo_root)
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
    response = requests.get(url, cookies=cookies)
    if response.status_code == 200:
        data = response.json()
        return Leaderboard.from_dict(data), data
    else:
        print(f"Error: Unable to fetch data (status code: {response.status_code})")
        return None

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
                    star_progress.append(f"[★](https://github.com/TrueNorthIT/AdventOfCode/tree/{branch}/{YEAR}/day{day:02})")
                elif 1 in stars_for_day:
                    star_progress.append(f"[✩](https://github.com/TrueNorthIT/AdventOfCode/tree/{branch}/{YEAR}/day{day:02})")
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
            star_release_time = datetime(YEAR, 12, day, 5, 0, 0, tzinfo=timezone.utc).timestamp()
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

def generate_achievements_table(board: Leaderboard) -> str:
    num_members = len(board.members)

    # --- Early Bird: fastest P1 after unlock ---
    p1_per_member = fastest_p1_per_member(board)  # {name: (day, delta)}
    early_bird_sorted = sorted(
        p1_per_member.items(),
        key=lambda x: x[1][1]  # sort by delta ascending
    )
    # convert to (name, score) where score is delta (seconds)
    early_bird_entries = [(name, delta) for name, (_day, delta) in early_bird_sorted]

    # --- You Are Gonna Need It: fastest P2-P1 delta ---
    p2_p1_per_member = fastest_delta_per_member(board)  # {name: (day, delta)}
    need_it_sorted = sorted(
        p2_p1_per_member.items(),
        key=lambda x: x[1][1]
    )
    need_it_entries = [(name, delta) for name, (_day, delta) in need_it_sorted]

    # --- Hackerman: local_score (descending) ---
    hackerman_entries = []
    hackerman_entries = calculate_hackerman(board)
    
    # --- Polyglot: most distinct languages per member via git ---
    polyglot_scores = compute_polyglot_scores_git(board)
    # polyglot_scores: { name: (count, langs_set) }

    polyglot_entries = [
        (name, count, langs)
        for name, (count, langs) in polyglot_scores.items()
    ]
    polyglot_entries.sort(key=lambda x: -x[1])  # sort by language count desc
    
    max_len = max(len(early_bird_entries), len(need_it_entries), len(hackerman_entries), len(polyglot_entries))
    
    
    # headers: "", "1st", "2nd", ..., "Nth"
    headers = [""] + [ordinal(i) for i in range(1, max_len + 1)]
    rows = []

    def cells_from_entries(entries, fmt_score, num_slots: int) -> list[str]:
        """
        Take list[(name, score)] and return up to num_slots 'Name (score)' cells.
        Pad with "" if fewer than num_slots.
        """
        cells: list[str] = []
        for name, score in entries[:num_slots]:
            cells.append(f"{name} ({fmt_score(score)})")
        # pad with blanks if we have fewer entries
        while len(cells) < num_slots:
            cells.append("")
        return cells
    
    def cells_for_polyglot(entries, num_slots):
        cells = []
        for name, count, langs in entries[:num_slots]:
            lang_list = "<br>".join(sorted(langs))  # multiline inside <details>
            cell = (
                f"<details>"
                f"<summary>{name} ({count})</summary>"
                f"{lang_list}"
                f"</details>"
            )
            cells.append(cell)
        while len(cells) < num_slots:
            cells.append("")
        return cells

    rows.append(
        [(
            f"<details>"
            f"<summary>Polyglot 🤓</summary>"
            f"Most distinct programming languages used.<br>"
            f"</details>"
        )]
        + cells_for_polyglot(polyglot_entries, max_len)
    )

    rows.append(
        [(
            f"<details>"
            f"<summary>Early Bird ⏰</summary>"
            f"Fastest time to complete Star 1 after unlock.<br>"
            f"</details>"
        )]
        + cells_from_entries(early_bird_entries, lambda s: format_duration_full(s), max_len)
    )

    rows.append(
        [(
            f"<details>"
            f"<summary>You Are Gonna Need It 🛠️</summary>"
            f"Fastest time between Star 1 and Star 2.<br>"
            f"</details>"
        )]
        + cells_from_entries(need_it_entries, lambda s: format_duration_full(s), max_len)
    )

    rows.append(
        [(
            f"<details>"
            f"<summary>Hackerman 💻</summary>"
            f"Highest local score on the private leaderboard.<br>"
            f"</details>"
        ) ]
        + cells_from_entries(hackerman_entries, lambda s: str(s), max_len)
    )

    return tabulate(rows, headers=headers, tablefmt="github")


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

    # Fetch data
    leaderboard_data, raw_data = fetch_leaderboard_data(LEADERBOARD_URL, SESSION_COOKIE)

    if leaderboard_data:
        # Post Leaderboard data to home assitant
        post_to_haWebhook(leaderboard_data)

        # Generate and print markdown table
        markdown_table = generate_markdown_table(leaderboard_data)
        achievements_table = generate_achievements_table(leaderboard_data)
        
        with open('README.template', encoding='utf-8') as f:
            readme_stub = f.read()

        # simple replacement, use whatever stand-in value is useful for you.
        readme = readme_stub.replace('{lob}',markdown_table).replace('{ach}', achievements_table)

        with open('README.md','w', encoding='utf-8') as f:
            f.write(readme)
