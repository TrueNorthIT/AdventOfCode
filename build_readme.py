import os
import requests
import json
from tabulate import tabulate

# Constants
YEAR = 2024
LEADERBOARD_URL = f"https://adventofcode.com/2023/leaderboard/private/view/353270.json"

# Fetch SESSION_COOKIE from environment variables
SESSION_COOKIE = os.getenv("SESSION_COOKIE")
if not SESSION_COOKIE:
    raise ValueError("SESSION_COOKIE is not set. Please provide it as an environment variable.")

# Fetch leaderboard data
def fetch_leaderboard_data(url, session_cookie):
    cookies = {"session": session_cookie}
    response = requests.get(url, cookies=cookies)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch data (status code: {response.status_code})")
        return None

# Generate markdown table with hyperlinks
def generate_markdown_table(data, branch_mapping):
    # Prepare table data
    table_data = []
    headers = ["Rank", "Name", "Local Score", "Stars"] + [str(day) for day in range(1, 26)]

    rank = 1
    for member_id, details in sorted(data["members"].items(), key=lambda x: -x[1]["local_score"]):
        name = details.get("name", "Unknown")
        local_score = details.get("local_score", 0)
        stars = details.get("stars", 0)
        completion = details.get("completion_day_level", {})
        branch = branch_mapping.get(member_id, None)

        # Build star progress with hyperlinks
        star_progress = []
        for day in range(1, 26):
            day_str = str(day)
            if day_str in completion:
                stars_for_day = completion[day_str]
                if "2" in stars_for_day:
                    star_progress.append(f"[★](https://github.com/TrueNorthIT/AdventOfCode/tree/{branch}/{YEAR}/day{day:02})")
                elif "1" in stars_for_day:
                    star_progress.append(f"[✩](https://github.com/TrueNorthIT/AdventOfCode/tree/{branch}/{YEAR}/day{day:02})")
            else:
                star_progress.append("·")

        table_data.append([rank, name, local_score, stars] + star_progress)
        rank += 1

    # Generate markdown table
    return tabulate(table_data, headers=headers, tablefmt="github")

# Main script
if __name__ == "__main__":
    # Replace this with your actual branch mapping
    branch_mapping = {
        "1427047": "christian-waters",
        "353270": "joe-pitts",
        "3292198": "josh-cottrell",
        "3357259": "alex-radice",
        "4264967": "rich-kelsey",
        "4265041": "kade-hennessy"
    }

    # Fetch data
    leaderboard_data = fetch_leaderboard_data(LEADERBOARD_URL, SESSION_COOKIE)

    if leaderboard_data:
        # Generate and print markdown table
        markdown_table = generate_markdown_table(leaderboard_data, branch_mapping)
        print(markdown_table)
                
        # template readme
        with open('README.template', encoding='utf-8') as f:
            readme_stub = f.read()

        # simple replacement, use whatever stand-in value is useful for you.
        readme = readme_stub.replace('{lob}',markdown_table)

        with open('README.md','w', encoding='utf-8') as f:
            f.write(readme)
