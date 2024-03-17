from datetime import datetime
from datetime import timedelta


def get_next_hour(timestamp: datetime) -> datetime:
    return timestamp.replace(
        second=0, microsecond=0, minute=0, hour=timestamp.hour
    ) + timedelta(hours=1)


def get_next_minute(timestamp: datetime) -> datetime:
    return timestamp.replace(
        second=0, microsecond=0, minute=timestamp.minute
    ) + timedelta(minutes=1)


def get_seconds_until_next_hour() -> int:
    current_time = datetime.now()

    next_hour = get_next_hour(current_time)

    delta_time: timedelta = next_hour - current_time

    return delta_time.seconds


def get_seconds_until_next_minute() -> int:
    current_time = datetime.now()

    next_hour = get_next_minute(current_time)

    delta_time: timedelta = next_hour - current_time

    return delta_time.seconds
