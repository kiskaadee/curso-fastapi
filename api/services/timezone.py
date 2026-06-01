from datetime import datetime
from typing import List
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import pytz

from models.info import TimeResponse


def greet(weekday: int) -> str:

    astros: List[str] = [
        "The Moon",  # 0 - Monday
        "Mars",  # 1 - Tuesday
        "Mercury",  # 2 - Wednesday
        "Jupiter",  # 3 - Saturday
        "Venus",  # 4 - Friday
        "Saturn",  # 5 - Saturday
        "The Sun",  # 6 - Sunday
    ]

    msg: str = f"Greetings from {astros[weekday]}!"
    return msg


def lookup_timezone(iso_code: str) -> ZoneInfo:
    if len(iso_code) != 2:
        raise ValueError("Invalid ISO code format.")

    iso: str = iso_code.upper().strip()
    timezones: list[str] | None = pytz.country_timezones.get(iso)

    if not timezones:
        raise ValueError("Country code not found or has no timezones.")

    target_timezone_name: str = timezones[0]

    try:
        return ZoneInfo(target_timezone_name)
    except ZoneInfoNotFoundError:
        raise RuntimeError("Timezone data missing on server.")


def compute_date_data(iso_code: str) -> dict[str, str]:
    timezone_object: ZoneInfo = lookup_timezone(iso_code)
    current_time: datetime = datetime.now(timezone_object)
    return {
        "iso": iso_code.upper(),
        "day": current_time.strftime("%d"),
        "month": current_time.strftime("%B"),
        "year": current_time.strftime("%Y"),
    }


def compute_time_data(iso_code: str, format: str = "12h") -> TimeResponse:
    allowed_timeformat = ["12h", "24h"]
    if format not in allowed_timeformat:
        raise ValueError("Time format not supported. Enter '12h' or '24h'")

    timezone_object: ZoneInfo = lookup_timezone(iso_code)
    current_time: datetime = datetime.now(timezone_object)

    if format == "12h":
        return TimeResponse(
            hour=current_time.strftime("%I"),
            minute=current_time.strftime("%M"),
            seconds=current_time.strftime("%S"),
            meridian=current_time.strftime("%p"),
        )
    else:  # 24h
        return TimeResponse(
            hour=current_time.strftime("%I"),
            minute=current_time.strftime("%M"),
            seconds=current_time.strftime("%S"),
            meridian=None,
        )
