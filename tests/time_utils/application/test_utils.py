from datetime import datetime
from unittest.mock import patch

import pytest
from inspi_quote_notifier.notifications.time_utils.application.utils import (
    get_next_hour,
)
from inspi_quote_notifier.notifications.time_utils.application.utils import (
    get_next_minute,
)
from inspi_quote_notifier.notifications.time_utils.application.utils import (
    get_seconds_until_next_hour,
)
from inspi_quote_notifier.notifications.time_utils.application.utils import (
    get_seconds_until_next_minute,
)


@pytest.mark.parametrize(
    "timestamp",
    [
        datetime(year=2020, month=10, day=1, hour=10, minute=0),
        datetime(year=2020, month=10, day=1, hour=10, minute=10),
        datetime(year=2020, month=10, day=1, hour=10, minute=30),
        datetime(year=2020, month=10, day=1, hour=10, minute=50),
    ],
)
def test_get_next_hour(timestamp: datetime):
    expected_timestamp = datetime(
        year=2020, month=10, day=1, hour=11, minute=0, second=0
    )

    result = get_next_hour(timestamp)

    assert expected_timestamp == result


@pytest.mark.parametrize(
    "timestamp",
    [
        datetime(year=2020, month=10, day=1, hour=10, minute=0, second=0),
        datetime(year=2020, month=10, day=1, hour=10, minute=0, second=10),
        datetime(year=2020, month=10, day=1, hour=10, minute=0, second=30),
        datetime(year=2020, month=10, day=1, hour=10, minute=0, second=50),
    ],
)
def test_get_next_minute(timestamp: datetime):
    expected_timestamp = datetime(year=2020, month=10, day=1, hour=10, minute=1)

    result = get_next_minute(timestamp)

    assert expected_timestamp == result


@pytest.mark.parametrize(
    "timestamp,expected_seconds",
    [
        (datetime(year=2020, month=10, day=1, hour=10, minute=0), 3600),
        (datetime(year=2020, month=10, day=1, hour=10, minute=10), 3000),
        (datetime(year=2020, month=10, day=1, hour=10, minute=30), 1800),
        (datetime(year=2020, month=10, day=1, hour=10, minute=50), 600),
    ],
)
def test_get_seconds_until_next_hour(timestamp: datetime, expected_seconds: int):
    with patch(
        "inspi_quote_notifier.notifications.time_utils.application.utils.datetime"
    ) as mock_datetime:
        mock_datetime.now.return_value = timestamp

        result = get_seconds_until_next_hour()

    assert expected_seconds == result


@pytest.mark.parametrize(
    "timestamp,expected_seconds",
    [
        (datetime(year=2020, month=10, day=1, hour=10, minute=0, second=0), 60),
        (datetime(year=2020, month=10, day=1, hour=10, minute=0, second=10), 50),
        (datetime(year=2020, month=10, day=1, hour=10, minute=0, second=30), 30),
        (datetime(year=2020, month=10, day=1, hour=10, minute=0, second=50), 10),
    ],
)
def test_get_seconds_until_next_minute(timestamp: datetime, expected_seconds: int):
    with patch(
        "inspi_quote_notifier.notifications.time_utils.application.utils.datetime"
    ) as mock_datetime:
        mock_datetime.now.return_value = timestamp

        result = get_seconds_until_next_minute()

    assert expected_seconds == result
