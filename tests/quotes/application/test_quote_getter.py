from unittest.mock import Mock

from inspi_quote_notifier.quotes.application.quote_getter import DEFAULT_QUOTE
from inspi_quote_notifier.quotes.application.quote_getter import QuoteGetter
from inspi_quote_notifier.quotes.domain.consumer import QuoteConsumer
from inspi_quote_notifier.quotes.domain.exceptions import QuoteNotFoundException
from inspi_quote_notifier.quotes.domain.quote import Quote

QUOTE = Quote("Some author", "text")
INVALID_QUOTE = Quote(None, None)


def test_get_quote():
    consumer = Mock(spec=QuoteConsumer)
    consumer.get_quotes.return_value = [QUOTE]

    quote_getter = QuoteGetter(consumer)

    quote = quote_getter.get_quote()

    assert QUOTE == quote


def test_get_quote_quote_not_found_exception():
    consumer = Mock(spec=QuoteConsumer)
    consumer.get_quotes.side_effect = QuoteNotFoundException()

    quote_getter = QuoteGetter(consumer)

    quote = quote_getter.get_quote()

    assert DEFAULT_QUOTE == quote


def test_get_quote_could_not_get_random_quote():
    consumer = Mock(spec=QuoteConsumer)
    consumer.get_quotes.return_value = [INVALID_QUOTE]

    quote_getter = QuoteGetter(consumer)

    quote = quote_getter.get_quote()

    assert DEFAULT_QUOTE == quote
