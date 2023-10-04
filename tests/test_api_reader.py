
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
