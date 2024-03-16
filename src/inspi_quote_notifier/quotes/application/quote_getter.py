from __future__ import annotations

import logging
import random

from inspi_quote_notifier.quotes.domain.consumer import QuoteConsumer
from inspi_quote_notifier.quotes.domain.exceptions import QuoteNotFoundException
from inspi_quote_notifier.quotes.domain.quote import Quote
from inspi_quote_notifier.quotes.domain.validator import Validator

DEFAULT_QUOTE_TEXT = "Play wisely the cards life gave you."
DEFAULT_QUOTE_AUTHOR = "Yourself"

DEFAULT_QUOTE = Quote(DEFAULT_QUOTE_AUTHOR, DEFAULT_QUOTE_TEXT)


class QuoteGetter:
    def __init__(self, consumer: QuoteConsumer, validator: Validator) -> None:
        self.consumer = consumer
        self.max_retries_to_get_random_quote = 10
        self.validator = validator
        self.logger = logging.getLogger(QuoteGetter.__name__)

    def get_quote(self) -> Quote:
        quotes = self._get_quotes_from_consumer()

        if not quotes:
            return DEFAULT_QUOTE

        return self._get_random_quote(quotes)

    def _get_quotes_from_consumer(self) -> list[Quote] | None:
        try:
            return self.consumer.get_quotes()
        except QuoteNotFoundException as e:
            self.logger.error("Could not obtain quote from consumer. Error: %s", e)
            return None

    def _get_random_quote(self, quotes: list[Quote]) -> Quote:
        num_quotes = len(quotes)
        for _ in range(0, self.max_retries_to_get_random_quote):
            seed = random.randint(0, num_quotes - 1)

            quote = quotes[seed]
            if self.validator.validate(quote):
                return quote

        self.logger.error(
            "Could not a valid random quote after %s tries",
            self.max_retries_to_get_random_quote,
        )
        return DEFAULT_QUOTE
