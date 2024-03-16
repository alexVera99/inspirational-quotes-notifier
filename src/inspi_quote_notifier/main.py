import logging

from inspi_quote_notifier.api_reader import ApiReader
from inspi_quote_notifier.logging import configure_logging
from inspi_quote_notifier.notifications.factory import create_notifier


def main() -> None:
    configure_logging()
    logger = logging.getLogger("main")

    notifier = create_notifier()

    default_author = "Someone"
    ar = ApiReader(default_author)

    quote = ar.get_one_quote()
    logger.debug(f"Notifying the following quote: {quote}")

    notifier.notify(quote)
