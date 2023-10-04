from unittest.mock import Mock
from unittest.mock import patch

from inspi_quote_notifier.api_reader import ApiReader
from inspi_quote_notifier.quotes.domain.quote import Quote
from requests import RequestException

API_URL = "http://www.test.invalid"
QUOTE_AUTHOR = "Some author"
QUOTE_TEXT = "Some text"
API_RESPONSE = [{"text": QUOTE_TEXT, "author": QUOTE_AUTHOR}]
QUOTE = Quote(QUOTE_AUTHOR, QUOTE_TEXT)


@patch("requests.get")
def test_read_quotes_from_api_happy_path(mock_requests_get: Mock):
    api_reader = ApiReader(api_url=API_URL)

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = API_RESPONSE

    mock_requests_get.return_value = mock_response

    res = api_reader.read_quotes_from_api()

    assert [QUOTE] == res
    mock_requests_get.assert_called_once()


@patch("requests.get")
def test_read_quotes_from_api_sad_path(mock_requests_get: Mock):
    api_reader = ApiReader(api_url=API_URL)

    status_code = 400
    mock_response = Mock()
    mock_response.status_code = status_code

    mock_requests_get.return_value = mock_response

    res = api_reader.read_quotes_from_api()

    assert res is None
    assert mock_requests_get.call_count == api_reader.max_num_requests


@patch("requests.get", side_effect=RequestException)
def test_read_quotes_from_api_raise_request_exception(mock_requests_get: Mock):
    api_reader = ApiReader(api_url=API_URL)

    res = api_reader.read_quotes_from_api()

    assert res is None
    assert mock_requests_get.call_count == api_reader.max_num_requests


@patch("requests.get")
def test_get_one_quote_happy_path(mock_requests_get: Mock):
    api_reader = ApiReader(api_url=API_URL)

    status_code = 200
    expected_text = "Some text"
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = API_RESPONSE

    mock_requests_get.return_value = mock_response
    quote = api_reader.get_one_quote()

    assert expected_text == quote.text
    assert QUOTE_AUTHOR == quote.author
    mock_requests_get.assert_called_once()


@patch("requests.get")
def test_get_one_quote_cannot_generate_proper_quote(mock_requests_get: Mock):
    api_reader = ApiReader(api_url=API_URL)

    status_code = 200
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = [{"text": None, "author": QUOTE_AUTHOR}]

    mock_requests_get.return_value = mock_response
    quote = api_reader.get_one_quote()

    assert "" == quote.text
    assert "" == quote.author
    mock_requests_get.assert_called_once()


@patch("requests.get")
def test_get_one_quote_too_large(mock_requests_get: Mock):
    api_reader = ApiReader(api_url=API_URL)

    status_code = 200
    too_large_quote_text = "a" * (api_reader.max_size_quote + 1)
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = [
        {"text": too_large_quote_text, "author": QUOTE_AUTHOR}
    ]

    mock_requests_get.return_value = mock_response
    quote = api_reader.get_one_quote()

    assert ApiReader.DEFAULT_QUOTE_TEXT == quote.text
    assert ApiReader.DEFAULT_QUOTE_AUTHOR == quote.author
    mock_requests_get.assert_called_once()


@patch("requests.get", side_effect=RequestException)
def test_get_one_quote_no_internet_connection(mock_requests_get: Mock):
    api_reader = ApiReader(api_url=API_URL)

    quote = api_reader.get_one_quote()

    assert mock_requests_get.call_count == api_reader.max_num_requests
    assert ApiReader.DEFAULT_QUOTE_TEXT == quote.text
    assert ApiReader.DEFAULT_QUOTE_AUTHOR == quote.author
