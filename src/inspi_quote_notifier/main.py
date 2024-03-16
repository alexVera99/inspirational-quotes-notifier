import logging

from inspi_quote_notifier.logging import configure_logging
from inspi_quote_notifier.notifications.factory import create_notifier
from inspi_quote_notifier.quotes.application.quote_getter import QuoteGetter
from inspi_quote_notifier.quotes.application.validators.factory import (
    create_validator_chain,
)
from inspi_quote_notifier.quotes.infrastructure.type_fit_consumer import (
    TypeFitQuoteConsumer,
)


def main() -> None:
    configure_logging()
    logger = logging.getLogger("main")

    notifier = create_notifier()
    validator = create_validator_chain()

    consumer = TypeFitQuoteConsumer()
    quote_getter = QuoteGetter(consumer, validator)

    quote = quote_getter.get_quote()
    logger.debug(f"Notifying the following quote: {quote}")

    notifier.notify(quote)
