from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, Any


@dataclass
class Star:
    star_index: int
    get_star_ts: int

    @property
    def completed_at(self) -> datetime:
        return datetime.fromtimestamp(self.get_star_ts)


@dataclass
class Member:
    id: int
    name: Optional[str]
    stars: int
    local_score: int
    global_score: int
    last_star_ts: Optional[int]
    # completion_day_level[day][part] = Star
    completion_day_level: Dict[int, Dict[int, Star]] = field(default_factory=dict)


@dataclass
class Leaderboard:
    event: str
    owner_id: int
    num_days: int
    members: Dict[int, Member]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Leaderboard":
        members: Dict[int, Member] = {}

        for member_id_str, member_data in data.get("members", {}).items():
            member_id = int(member_id_str)

            # Parse completion_day_level
            completion: Dict[int, Dict[int, Star]] = {}

            for day_str, parts_dict in member_data.get("completion_day_level", {}).items():
                day = int(day_str)
                completion[day] = {}

                for part_str, star_info in parts_dict.items():
                    part = int(part_str)
                    star = Star(
                        star_index=int(star_info.get("star_index", 0)),
                        get_star_ts=int(star_info.get("get_star_ts", 0)),
                    )
                    completion[day][part] = star

            member = Member(
                id=int(member_data["id"]),
                name=member_data.get("name"),
                stars=int(member_data.get("stars", 0)),
                local_score=int(member_data.get("local_score", 0)),
                global_score=int(member_data.get("global_score", 0)),
                last_star_ts=int(member_data["last_star_ts"]) if "last_star_ts" in member_data else None,
                completion_day_level=completion,
            )

            members[member_id] = member

        return cls(
            event=str(data["event"]),
            owner_id=int(data["owner_id"]),
            num_days=int(data.get("num_days", 25)),
            members=members,
        )
