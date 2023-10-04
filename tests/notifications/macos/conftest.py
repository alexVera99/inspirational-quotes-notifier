from unittest.mock import patch

import pytest


@pytest.fixture()
def mock_pync_notifier():
    with patch("pync.Notifier.notify") as mock_notifier:
        yield mock_notifier


@pytest.fixture()
def notifier_osx(mock_pync_notifier):
    # Dirty, but works: The reason for this is that executing in
    # the CI, we use Ubuntu. So, the macOS library for notifications
    # raises an exception since we are not in macOS
    from inspi_quote_notifier.notifications.macos.notifier_osx import NotifierOSX

    yield NotifierOSX()
