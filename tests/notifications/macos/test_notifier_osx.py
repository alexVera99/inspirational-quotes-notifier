import sys
from unittest.mock import ANY
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from inspi_quote_notifier.quotes.domain.quote import Quote


sys.modules["pync"] = MagicMock()


@pytest.fixture
def mock_pync_notify():
    with patch("pync.notify") as mock_notify:
        yield mock_notify


@pytest.fixture
def notifier_osx(mock_pync_notify):
    from inspi_quote_notifier.notifications.macos.notifier_osx import NotifierOSX

    yield NotifierOSX()


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
