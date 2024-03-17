import logging
from argparse import ArgumentParser
from dataclasses import dataclass

from inspi_quote_notifier.logging import configure_logging
from inspi_quote_notifier.notifications.factory import create_notifier
from inspi_quote_notifier.notifications.notifier import Notifier
from inspi_quote_notifier.quotes.application.quote_getter import QuoteGetter
from inspi_quote_notifier.quotes.application.validators.factory import (
    create_validator_chain,
)
from inspi_quote_notifier.quotes.infrastructure.type_fit_consumer import (
    TypeFitQuoteConsumer,
)
from inspi_quote_notifier.scheduler.application.scheduler import Scheduler


def main() -> None:
    args = parse_args()

    configure_logging()

    notifier = create_notifier()
    validator = create_validator_chain()

    consumer = TypeFitQuoteConsumer()
    quote_getter = QuoteGetter(consumer, validator)

    scheduler = Scheduler()

    if args.every_hour:
        scheduler.schedule_every_hour(notify_quote, quote_getter, notifier)
        scheduler.start()
    elif args.every_minute:
        scheduler.schedule_every_minute(notify_quote, quote_getter, notifier)
        scheduler.start()
    else:
        notify_quote(quote_getter, notifier)


@dataclass
class Arguments:
    every_hour: bool
    every_minute: bool


def parse_args() -> Arguments:
    parser = ArgumentParser(
        prog="Inspirational Quotes Notifier", description="Notify inspirational quotes."
    )

    parser.add_argument("--every-hour", action="store_true")
    parser.add_argument("--every-minute", action="store_true")

    raw_args = parser.parse_args()

    return Arguments(raw_args.every_hour, raw_args.every_minute)


def notify_quote(quote_getter: QuoteGetter, notifier: Notifier) -> None:
    logger = logging.getLogger("notify_quote")

    quote = quote_getter.get_quote()

    logger.debug(f"Notifying the following quote: {quote}")

    notifier.notify(quote)
