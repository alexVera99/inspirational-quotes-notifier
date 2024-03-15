from unittest.mock import Mock
from unittest.mock import patch

from inspi_quote_notifier.main import main
from inspi_quote_notifier.quotes.domain.quote import Quote


@patch("inspi_quote_notifier.main.ApiReader")
@patch("inspi_quote_notifier.main.create_notifier")
def test_main(mock_create_notifier: Mock, mock_api_reader: Mock):
    quote = Quote("Some author", "Some message")
    mock_api_reader_instance = mock_api_reader.return_value
    mock_api_reader_instance.get_one_quote.return_value = quote

    main()

    mock_api_reader_instance.get_one_quote.assert_called_once_with(True)
    mock_create_notifier.return_value.notify.assert_called_once_with(quote)
