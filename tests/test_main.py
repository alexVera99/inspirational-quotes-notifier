from unittest.mock import Mock
from unittest.mock import patch

from inspi_quote_notifier.main import main
from inspi_quote_notifier.quotes.domain.quote import Quote


@patch("inspi_quote_notifier.main.QuoteGetter")
@patch("inspi_quote_notifier.main.create_validator_chain")
@patch("inspi_quote_notifier.main.create_notifier")
def test_main(
    mock_create_notifier: Mock, mock_create_validator: Mock, mock_quote_getter: Mock
):
    quote = Quote("Some author", "Some message")
    mock_quote_getter_instance = mock_quote_getter.return_value
    mock_quote_getter_instance.get_quote.return_value = quote

    main()

    mock_quote_getter_instance.get_quote.assert_called_once_with()
    mock_create_notifier.return_value.notify.assert_called_once_with(quote)
    mock_create_validator.assert_called_once()
