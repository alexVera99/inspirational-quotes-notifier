from __future__ import annotations

import logging
from time import sleep
from typing import Any
from typing import Callable

import schedule
from inspi_quote_notifier.notifications.time_utils.application.utils import (
    get_seconds_until_next_hour,
)
from inspi_quote_notifier.notifications.time_utils.application.utils import (
    get_seconds_until_next_minute,
)
from inspi_quote_notifier.scheduler.domain.exceptions import NoScheduleException
from inspi_quote_notifier.scheduler.domain.time_unit import TimeUnit


class Scheduler:
    # TODO: If schedule is set to every minute and then
    # to every minute, it will change the time delta to
    # check pending jobs. This is a BUG :/
    def __init__(self) -> None:
        self.logger = logging.getLogger(Scheduler.__name__)
        self.time_unit: TimeUnit | None = None

    def schedule_every_hour(self, job: Callable, *args: Any, **kwargs: Any) -> None:
        self.time_unit = TimeUnit.HOUR
        schedule.every().hour.at(":00").do(job, *args, **kwargs)

    def schedule_every_minute(self, job: Callable, *args: Any, **kwargs: Any) -> None:
        self.time_unit = TimeUnit.MINUTE
        schedule.every().minute.at(":00").do(job, *args, **kwargs)

    def start(self) -> None:
        while True:
            self.run_pending_jobs()

    def run_pending_jobs(self) -> None:
        self._check_time_unit_is_set()

        self.logger.debug("Checking for pending jobs")
        schedule.run_pending()

        sleep(self._get_seconds_until_next_execution())

    def _check_time_unit_is_set(self) -> None:
        if self.time_unit is None:
            raise NoScheduleException("No job has been scheduled")

    def _get_seconds_until_next_execution(self) -> int:
        seconds = 1

        if self.time_unit == TimeUnit.HOUR:
            seconds = get_seconds_until_next_hour()

        elif self.time_unit == TimeUnit.MINUTE:
            seconds = get_seconds_until_next_minute()

        seconds_next_execution = seconds + 2

        self.logger.debug("Next execution in: %s", seconds_next_execution)

        return seconds_next_execution
