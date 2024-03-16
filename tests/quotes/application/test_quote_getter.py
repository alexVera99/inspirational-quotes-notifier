from unittest.mock import Mock

from inspi_quote_notifier.quotes.application.quote_getter import DEFAULT_QUOTE
from inspi_quote_notifier.quotes.application.quote_getter import QuoteGetter
from inspi_quote_notifier.quotes.domain.consumer import QuoteConsumer
from inspi_quote_notifier.quotes.domain.exceptions import QuoteNotFoundException
from inspi_quote_notifier.quotes.domain.quote import Quote
from inspi_quote_notifier.quotes.domain.validator import Validator

QUOTE = Quote("Some author", "text")
INVALID_QUOTE = Quote(None, None)


def test_get_quote():
    consumer = Mock(spec=QuoteConsumer)
    consumer.get_quotes.return_value = [QUOTE]

    mock_validator = Mock(spec=Validator)

    quote_getter = QuoteGetter(consumer, mock_validator)

    quote = quote_getter.get_quote()

    assert QUOTE == quote


def test_get_quote_quote_not_found_exception():
    consumer = Mock(spec=QuoteConsumer)
    consumer.get_quotes.side_effect = QuoteNotFoundException()

    mock_validator = Mock(spec=Validator)

    quote_getter = QuoteGetter(consumer, mock_validator)

    quote = quote_getter.get_quote()

    assert DEFAULT_QUOTE == quote


def test_get_quote_could_not_get_random_quote():
    consumer = Mock(spec=QuoteConsumer)
    consumer.get_quotes.return_value = [INVALID_QUOTE]

    mock_validator = Mock(spec=Validator)
    mock_validator.validate.return_value = False

    quote_getter = QuoteGetter(consumer, mock_validator)

    quote = quote_getter.get_quote()

    assert DEFAULT_QUOTE == quote
