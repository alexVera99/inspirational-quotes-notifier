from unittest.mock import Mock
from unittest.mock import patch

from inspi_quote_notifier.main import main
from inspi_quote_notifier.main import notify_quote
from inspi_quote_notifier.quotes.domain.quote import Quote


@patch("inspi_quote_notifier.main.Scheduler")
def test_main(
    mock_scheduler: Mock,
):
    main()

    mock_scheduler_instance = mock_scheduler.return_value
    mock_scheduler_instance.schedule_every_minute.assert_called_once_with(notify_quote)
    mock_scheduler_instance.start.assert_called_once()


@patch("inspi_quote_notifier.main.quote_getter")
@patch("inspi_quote_notifier.main.notifier")
def test_notify_quote(
    mock_notifier: Mock,
    mock_quote_getter: Mock,
):
    quote = Quote("Some author", "Some message")
    mock_quote_getter.get_quote.return_value = quote

    notify_quote()

    mock_quote_getter.get_quote.assert_called_once_with()
    mock_notifier.notify.assert_called_once_with(quote)
