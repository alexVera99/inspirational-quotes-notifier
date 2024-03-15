from unittest.mock import ANY
from unittest.mock import Mock

from inspi_quote_notifier.quotes.domain.quote import Quote


def test_notify(notifier_osx: Mock, mock_pync_notify):
    author = "author"
    text = "text"
    quote = Quote(author, text)

    expected_notification_title = quote.author + " once said:"

    notifier_osx.notify(quote)

    mock_pync_notify.assert_called_once_with(
        quote.text,
        title=expected_notification_title,
        group=ANY,
        sound=notifier_osx.sound,
    )
