from unittest.mock import Mock
from unittest.mock import patch

import pytest
from inspi_quote_notifier.notifications.factory import create_notifier
from inspi_quote_notifier.notifications.factory import NotSupportedPlatformException
from inspi_quote_notifier.notifications.factory import Platforms
from inspi_quote_notifier.notifications.macos.notifier_osx import NotifierOSX


@patch("platform.system")
def test_create_notifier_macos(mock_platform_system: Mock, mock_pync_notify):
    platform = Platforms.MACOS.value
    mock_platform_system.return_value = platform

    notifier = create_notifier()

    assert isinstance(notifier, NotifierOSX)
    mock_platform_system.assert_called_once()


@patch("platform.system")
def test_create_notifier_windows(mock_platform_system: Mock):
    platform = Platforms.WINDOWS.value
    mock_platform_system.return_value = platform

    with pytest.raises(NotSupportedPlatformException):
        _ = create_notifier()
        mock_platform_system.assert_called_once()


@patch("platform.system")
def test_create_notifier_linux(mock_platform_system: Mock):
    platform = Platforms.LINUX.value
    mock_platform_system.return_value = platform

    with pytest.raises(NotSupportedPlatformException):
        _ = create_notifier()
        mock_platform_system.assert_called_once()
