from unittest.mock import Mock
from unittest.mock import patch

from apiReader import ApiReader
from requests import RequestException

API_URL = "http://www.test.invalid"
AUTHOR = "Some author"


@patch("requests.get")
def test_read_quotes_from_api_happy_path(mock_requests_get: Mock):
    api_reader = ApiReader(api_url=API_URL)

    mock_response = Mock()
    mock_response.status_code = 200

    mock_requests_get.return_value = mock_response

    res = api_reader.read_quotes_from_api()

    assert mock_response == res


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
    assert api_reader.status_code == status_code


@patch("requests.get", side_effect=RequestException)
def test_read_quotes_from_api_raise_request_exception(mock_requests_get: Mock):
    api_reader = ApiReader(api_url=API_URL)

    res = api_reader.read_quotes_from_api()

    assert res is None
    assert mock_requests_get.call_count == api_reader.max_num_requests
    assert api_reader.status_code == -1


@patch("requests.get")
def test_get_one_quote_happy_path(mock_requests_get: Mock):
    api_reader = ApiReader(api_url=API_URL)

    status_code = 200
    expected_text = "Some text"
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = [{"text": expected_text, "author": AUTHOR}]

    mock_requests_get.return_value = mock_response
    q_text, q_author = api_reader.get_one_quote()

    assert expected_text == q_text
    assert AUTHOR == q_author


@patch("requests.get")
def test_get_one_quote_cannot_generate_proper_quote(mock_requests_get: Mock):
    api_reader = ApiReader(api_url=API_URL)

    status_code = 200
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = [{"text": None, "author": AUTHOR}]

    mock_requests_get.return_value = mock_response
    q_text, q_author = api_reader.get_one_quote()

    assert "" == q_text
    assert "" == q_author


@patch("requests.get")
def test_get_one_quote_too_large(mock_requests_get: Mock):
    api_reader = ApiReader(api_url=API_URL)

    status_code = 200
    too_large_quote_text = "a" * (api_reader.max_size_quote + 1)
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = [{"text": too_large_quote_text, "author": AUTHOR}]

    mock_requests_get.return_value = mock_response
    q_text, q_author = api_reader.get_one_quote()

    assert ApiReader.DEFAULT_QUOTE_TEXT == q_text
    assert ApiReader.DEFAULT_QUOTE_AUTHOR == q_author


@patch("requests.get", side_effect=RequestException)
def test_get_one_quote_no_internet_connection(mock_requests_get: Mock):
    api_reader = ApiReader(api_url=API_URL)

    q_text, q_author = api_reader.get_one_quote()

    assert ApiReader.DEFAULT_QUOTE_TEXT == q_text
    assert ApiReader.DEFAULT_QUOTE_AUTHOR == q_author
