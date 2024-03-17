from unittest.mock import Mock
from unittest.mock import patch

from inspi_quote_notifier.main import main
from inspi_quote_notifier.main import notify_quote
from inspi_quote_notifier.quotes.domain.quote import Quote


@patch("inspi_quote_notifier.main.QuoteGetter")
@patch("inspi_quote_notifier.main.create_validator_chain")
@patch("inspi_quote_notifier.main.create_notifier")
@patch("inspi_quote_notifier.main.Scheduler")
def test_main(
    mock_scheduler: Mock,
    mock_create_notifier: Mock,
    mock_create_validator_chain: Mock,
    mock_quote_getter: Mock,
):
    main()

    mock_create_notifier.assert_called_once()
    mock_create_validator_chain.assert_called_once()

    mock_notifier_instance = mock_create_notifier.return_value
    mock_quote_getter_instance = mock_quote_getter.return_value

    mock_scheduler_instance = mock_scheduler.return_value
    mock_scheduler_instance.schedule_every_minute.assert_called_once_with(
        notify_quote, mock_quote_getter_instance, mock_notifier_instance
    )
    mock_scheduler_instance.start.assert_called_once()


def test_notify_quote():
    quote = Quote("Some author", "Some message")

    mock_quote_getter = Mock()
    mock_quote_getter.get_quote.return_value = quote

    mock_notifier = Mock()

    notify_quote(mock_quote_getter, mock_notifier)

    mock_quote_getter.get_quote.assert_called_once_with()
    mock_notifier.notify.assert_called_once_with(quote)
