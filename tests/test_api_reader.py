
from unittest.mock import Mock, patch
from apiReader import ApiReader
from requests import RequestException


@patch("requests.get")
def test_read_quotes_from_api_happy_path(mock_requests_get: Mock):
    default_author = "Pepe"
    api_url = "http://www.test.invalid"
    api_reader = ApiReader(default_author, api_url)

    mock_response = Mock()
    mock_response.status_code = 200

    mock_requests_get.return_value = mock_response

    res = api_reader.readQuotesFromAPI()

    assert mock_response == res


@patch("requests.get")
def test_read_quotes_from_api_sad_path(mock_requests_get: Mock):
    default_author = "Pepe"
    api_url = "http://www.test.invalid"
    api_reader = ApiReader(default_author, api_url)

    status_code = 400
    mock_response = Mock()
    mock_response.status_code = status_code

    mock_requests_get.return_value = mock_response

    res = api_reader.readQuotesFromAPI()
    
    assert res is None
    assert mock_requests_get.call_count == api_reader.max_num_requests
    assert api_reader.status_code == status_code


@patch("requests.get", side_effect=RequestException)
def test_read_quotes_from_api_raise_request_exception(mock_requests_get: Mock):
    default_author = "Pepe"
    api_url = "http://www.test.invalid"
    api_reader = ApiReader(default_author, api_url)

    res = api_reader.readQuotesFromAPI()

    assert res is None
    assert mock_requests_get.call_count == api_reader.max_num_requests
    assert api_reader.status_code == -1


@patch("requests.get")
def test_get_one_quote_happy_path(mock_requests_get: Mock):
    default_author = "Pepe"
    api_url = "http://www.test.invalid"
    api_reader = ApiReader(default_author, api_url)

    status_code = 200
    expected_text = "Some text"
    expected_author = "Some author"
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = [
        {
            "text": expected_text,
            "author": expected_author
        }
    ]

    mock_requests_get.return_value = mock_response
    q_text, q_author = api_reader.getOneQuote()

    assert expected_text == q_text
    assert expected_author == q_author


@patch("requests.get")
def test_get_one_quote_cannot_generate_proper_quote(mock_requests_get: Mock):
    default_author = "Pepe"
    api_url = "http://www.test.invalid"
    api_reader = ApiReader(default_author, api_url)

    status_code = 200
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = [
        {
            "text": None,
            "author": "Some author"
        }
    ]

    mock_requests_get.return_value = mock_response
    q_text, q_author = api_reader.getOneQuote()

    assert "" == q_text
    assert "" == q_author


@patch("requests.get")
def test_get_one_quote_too_large(mock_requests_get: Mock):
    default_author = "Pepe"
    api_url = "http://www.test.invalid"
    api_reader = ApiReader(default_author, api_url)

    status_code = 200
    too_large_quote_text = "a" * (api_reader.max_size_quote + 1)
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.json.return_value = [
        {
            "text": too_large_quote_text,
            "author": "Some author"
        }
    ]

    mock_requests_get.return_value = mock_response
    q_text, q_author = api_reader.getOneQuote()

    assert ApiReader.DEFAULT_QUOTE_TEXT == q_text
    assert ApiReader.DEFAULT_QUOTE_AUTHOR == q_author


@patch("requests.get", side_effect=RequestException)
def test_get_one_quote_no_internet_connection(mock_requests_get: Mock):
    default_author = "Pepe"
    api_url = "http://www.test.invalid"
    api_reader = ApiReader(default_author, api_url)

    q_text, q_author = api_reader.getOneQuote()

    assert ApiReader.DEFAULT_QUOTE_TEXT == q_text
    assert ApiReader.DEFAULT_QUOTE_AUTHOR == q_author
