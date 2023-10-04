import os
from unittest.mock import Mock
from unittest.mock import patch

from inspi_quote_notifier.notifications.macos.notifier_osx import NotifierOSX
from inspi_quote_notifier.quotes.domain.quote import Quote


@patch("pync.Notifier.notify")
def test_notify(mock_pync_notifier: Mock):
    author = "author"
    text = "text"
    quote = Quote(author, text)

    expected_notification_title = quote.author + " once said:"

    notifier = NotifierOSX()

    notifier.notify(quote)

    mock_pync_notifier.assert_called_once_with(
        quote.text,
        title=expected_notification_title,
        group=os.getpid(),
        sound=NotifierOSX.sound,
    )
