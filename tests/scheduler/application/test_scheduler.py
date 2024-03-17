from unittest.mock import Mock
from unittest.mock import patch

from inspi_quote_notifier.scheduler.application.scheduler import Scheduler
from inspi_quote_notifier.scheduler.domain.time_unit import TimeUnit


@patch("inspi_quote_notifier.scheduler.application.scheduler.schedule")
def test_schedule_every_hour(mock_schedule: Mock):
    scheduler = Scheduler()

    argument = "hello"
    scheduler.schedule_every_hour(dummy_function, argument)

    mock_schedule.every.return_value.hour.at.assert_called_once_with(":00")
    mock_schedule.every.return_value.hour.at.return_value.do.assert_called_once_with(
        dummy_function, argument
    )


@patch("inspi_quote_notifier.scheduler.application.scheduler.schedule")
def test_schedule_every_minute(mock_schedule: Mock):
    scheduler = Scheduler()

    argument = "hello"
    scheduler.schedule_every_minute(dummy_function, argument)

    mock_schedule.every.return_value.minute.at.assert_called_once_with(":00")
    mock_schedule.every.return_value.minute.at.return_value.do.assert_called_once_with(
        dummy_function, argument
    )


@patch("inspi_quote_notifier.scheduler.application.scheduler.sleep")
@patch("inspi_quote_notifier.scheduler.application.scheduler.schedule")
def test_run_pending_jobs(mock_schedule: Mock, mock_sleep: Mock):
    scheduler = Scheduler()

    scheduler._check_time_unit_is_set = Mock()

    expected_seconds = 10
    scheduler._get_seconds_until_next_execution = Mock(return_value=expected_seconds)

    scheduler.run_pending_jobs()

    mock_schedule.run_pending.assert_called_once()
    scheduler._get_seconds_until_next_execution.assert_called_once()
    mock_sleep.assert_called_once_with(expected_seconds)


@patch(
    "inspi_quote_notifier.scheduler.application.scheduler.get_seconds_until_next_hour"
)
def test__get_seconds_until_next_execution_with_hour(
    mock_get_seconds_until_next_hour: Mock,
):
    expected_seconds = 10
    mock_get_seconds_until_next_hour.return_value = expected_seconds

    scheduler = Scheduler()
    scheduler.time_unit = TimeUnit.HOUR

    seconds = scheduler._get_seconds_until_next_execution()

    assert expected_seconds + 2 == seconds


@patch(
    "inspi_quote_notifier.scheduler.application.scheduler.get_seconds_until_next_minute"
)
def test__get_seconds_until_next_execution_with_minute(
    mock_get_seconds_until_next_minute: Mock,
):
    expected_seconds = 10
    mock_get_seconds_until_next_minute.return_value = expected_seconds

    scheduler = Scheduler()
    scheduler.time_unit = TimeUnit.MINUTE

    seconds = scheduler._get_seconds_until_next_execution()

    assert expected_seconds + 2 == seconds


def dummy_function(argument: str):
    print(argument)
