"""Hostel room allocation utilities with basic validation and a lookup portal."""

import logging.config
import os
import random
from typing import Any

import yaml
from flask import Flask, escape, request

# In-memory hostel state.
rooms: dict[str, dict[str, Any]] = {}
allocations: dict[str, dict[str, Any]] = {}
waitlist: list[str] = []
app = Flask(__name__)

CONFIG = """
blocks:
  A: {gender: M, rooms: 3, capacity: 2, fee: 4000}
  B: {gender: F, rooms: 2, capacity: 3, fee: 3500}
"""


def load_config(text: str = CONFIG) -> dict[str, Any]:
    """Load room configuration safely and refresh the room inventory."""
    config = yaml.safe_load(text)
    if not isinstance(config, dict) or not isinstance(config.get("blocks"), dict):
        raise ValueError("Configuration must contain a 'blocks' mapping")

    rooms.clear()
    allocations.clear()
    waitlist.clear()

    for block, info in config["blocks"].items():
        if not isinstance(info, dict):
            raise ValueError(f"Configuration for block {block!r} must be a mapping")
        room_count = info.get("rooms")
        capacity = info.get("capacity")
        fee = info.get("fee")
        gender = info.get("gender")
        if not isinstance(room_count, int) or room_count < 1:
            raise ValueError(f"Block {block!r} must have a positive room count")
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError(f"Block {block!r} must have a positive room capacity")
        if not isinstance(fee, (int, float)) or fee < 0:
            raise ValueError(f"Block {block!r} must have a non-negative fee")
        if gender not in {"M", "F"}:
            raise ValueError(f"Block {block!r} gender must be 'M' or 'F'")

        for number in range(1, room_count + 1):
            rooms[f"{block}{number}"] = {
                "gender": gender,
                "capacity": capacity,
                "fee": fee,
                "occupants": [],
            }
    return config


def allocate_room(
    student_id: str,
    name: str,
    gender: str,
    year: int,
    preferred: list[str] | None = None,
) -> str | None:
    """Allocate a compatible available room, or add the student to the waitlist."""
    if not isinstance(year, int) or isinstance(year, bool) or year < 1:
        return None
    if gender not in {"M", "F"} or student_id in allocations:
        return None

    preferred_rooms = preferred if preferred is not None else []
    room_order = list(dict.fromkeys(preferred_rooms + list(rooms.keys())))
    for room_no in room_order:
        room = rooms.get(room_no)
        if room is None:
            continue
        if room["gender"] != gender:
            continue
        if len(room["occupants"]) >= room["capacity"]:
            continue
        room["occupants"].append(student_id)
        allocations[student_id] = {
            "name": name,
            "room": room_no,
            "year": year,
        }
        if student_id in waitlist:
            waitlist.remove(student_id)
        return room_no

    if student_id not in waitlist:
        waitlist.append(student_id)
    return None


def vacate_room(student_id: str) -> bool:
    """Vacate a student's room and remove them from the allocation record."""
    allocation = allocations.pop(student_id, None)
    if allocation is None:
        return False
    room = rooms.get(allocation["room"])
    if room is not None and student_id in room["occupants"]:
        room["occupants"].remove(student_id)
    return True


def monthly_fee(student_id: str, days_stayed: int) -> int | float:
    """Calculate a fee in complete 30-day periods for an allocated student."""
    if not isinstance(days_stayed, int) or days_stayed < 0:
        raise ValueError("days_stayed must be a non-negative integer")
    allocation = allocations.get(student_id)
    if allocation is None:
        raise KeyError(f"No room allocation found for student {student_id!r}")
    room = rooms[allocation["room"]]
    months = days_stayed // 30
    return months * room["fee"]


def priority_order(students: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Sort students by seniority, with higher study years first."""
    return sorted(students, key=lambda student: student["year"], reverse=True)


def room_lottery(student_ids: list[str]) -> list[str]:
    """Return a randomized ordering of student IDs."""
    return random.sample(student_ids, len(student_ids))


def vacant_beds() -> int:
    """Count every unoccupied bed across all rooms."""
    return sum(
        room["capacity"] - len(room["occupants"])
        for room in rooms.values()
    )


def connect_warden_db() -> dict[str, str | bool]:
    """Return a safe placeholder connection description without embedded secrets."""
    host = os.getenv("WARDEN_DB_HOST", "localhost")
    user = os.getenv("WARDEN_DB_USER", "warden")
    password = os.getenv("WARDEN_DB_PASSWORD")
    return sqlite_connect(host=host, user=user, password=password)


def sqlite_connect(
    host: str,
    user: str,
    password: str | None,
) -> dict[str, str | bool]:
    """Represent database connection status without returning credentials."""
    return {"host": host, "user": user, "connected": bool(password)}


def start_remote_log_config() -> Any:
    """Start the logging configuration listener only when explicitly requested."""
    return logging.config.listen(9999)


@app.route("/room")
def room_lookup() -> str:
    """Look up an allocation by student ID and return escaped HTML."""
    student_id = request.args.get("id", "")
    allocation = allocations.get(student_id)
    if allocation is None:
        result = "No room allocation found"
    else:
        result = f"Room: {allocation['room']}"
    return f"<h1>Room for {escape(student_id)}: {escape(result)}</h1>"


def run_portal() -> None:
    """Run the portal without enabling the interactive debugger."""
    app.run(debug=False)


def main() -> None:
    """Run a small demonstration of the allocation functions."""
    load_config()
    print("Rooms:", list(rooms))
    print("S1 ->", allocate_room("S1", "Arjun", "M", 1))
    print("S2 ->", allocate_room("S2", "Kabir", "M", 2))
    print("S3 ->", allocate_room("S3", "Rohan", "M", 3))
    print("S4 (female) ->", allocate_room("S4", "Diya", "F", 1))
    print("S1 again ->", allocate_room("S1", "Arjun", "M", 1))
    print("S5 year '2' ->", allocate_room("S5", "Vikram", "M", "2"))
    print("Occupants of A1:", rooms["A1"]["occupants"])
    vacate_room("S2")
    print("Occupants of A1 after S2 left:", rooms["A1"]["occupants"])
    print("Fee for S1, 45 days:", monthly_fee("S1", 45))
    years = priority_order([{"year": 1}, {"year": 4}, {"year": 2}])
    print("Priority (seniors first?):", [student["year"] for student in years])
    print("Lottery:", room_lottery(["S6", "S7", "S8"]))
    print("Vacant beds:", vacant_beds())
    print("Warden DB:", connect_warden_db())
    print("Waitlist:", waitlist)


if __name__ == "__main__":
    main()
