from http import HTTPStatus
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from inspi_quote_notifier.quotes.domain.exceptions import QuoteNotFoundException
from inspi_quote_notifier.quotes.domain.quote import Quote
from inspi_quote_notifier.quotes.infrastructure.type_fit_consumer import (
    MAX_NUMBER_RETRIES,
)
from inspi_quote_notifier.quotes.infrastructure.type_fit_consumer import (
    TypeFitQuoteConsumer,
)
from requests import RequestException

QUOTE_TEXT = "Some text"
QUOTE_AUTHOR = "Some author"
API_RESPONSE = [{"text": QUOTE_TEXT, "author": QUOTE_AUTHOR}]


@patch("requests.get")
def test_get_quotes(mock_requests_get: Mock):
    consumer = TypeFitQuoteConsumer()

    status_code = HTTPStatus.OK
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = API_RESPONSE

    mock_requests_get.return_value = mock_response

    expected_quotes = [Quote(QUOTE_AUTHOR, QUOTE_TEXT)]

    quotes = consumer.get_quotes()

    assert expected_quotes == quotes


@patch("requests.get")
def test_get_quotes_retry_on_not_2xx(mock_requests_get: Mock):
    consumer = TypeFitQuoteConsumer()

    status_code = HTTPStatus.NOT_FOUND
    mock_response = Mock()
    mock_response.status_code = status_code

    mock_requests_get.return_value = mock_response

    with pytest.raises(QuoteNotFoundException):
        _ = consumer.get_quotes()

    assert mock_requests_get.call_count == MAX_NUMBER_RETRIES


@patch("requests.get", side_effect=RequestException)
def test_get_quotes_retry_on_request_exception(mock_requests_get: Mock):
    consumer = TypeFitQuoteConsumer()

    with pytest.raises(QuoteNotFoundException):
        _ = consumer.get_quotes()

    assert mock_requests_get.call_count == MAX_NUMBER_RETRIES
