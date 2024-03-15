import sys
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

sys.modules["pync"] = MagicMock()


@pytest.fixture
def mock_pync_notify():
    with patch(
        "inspi_quote_notifier.notifications.macos.notifier_osx.notify"
    ) as mock_notify:
        yield mock_notify


@pytest.fixture
def notifier_osx(mock_pync_notify):
    from inspi_quote_notifier.notifications.macos.notifier_osx import NotifierOSX

    yield NotifierOSX()
