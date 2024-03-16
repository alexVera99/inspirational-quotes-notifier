from unittest.mock import Mock
from unittest.mock import patch

import pytest
from inspi_quote_notifier.platforms.domain.exceptions import (
    NotSupportedPlatformException,
)
from inspi_quote_notifier.platforms.domain.platforms import Platforms
from inspi_quote_notifier.quotes.application.validators.base_validator import (
    BaseValidator,
)
from inspi_quote_notifier.quotes.application.validators.chain_validator import (
    ChainValidator,
)
from inspi_quote_notifier.quotes.application.validators.factory import (
    create_validator_chain,
)
from inspi_quote_notifier.quotes.application.validators.osx_validator import (
    OSXValidator,
)


@patch("platform.system")
def test_create_notifier_macos(mock_platform_system: Mock):
    platform = Platforms.MACOS.value
    mock_platform_system.return_value = platform

    validator = create_validator_chain()

    assert isinstance(validator, ChainValidator)
    validators = getattr(validator, "validators")

    assert isinstance(validators[0], BaseValidator)
    assert isinstance(validators[1], OSXValidator)
    mock_platform_system.assert_called_once()


@patch("platform.system")
def test_create_notifier_windows(mock_platform_system: Mock):
    platform = Platforms.WINDOWS.value
    mock_platform_system.return_value = platform

    with pytest.raises(NotSupportedPlatformException):
        _ = create_validator_chain()
        mock_platform_system.assert_called_once()


@patch("platform.system")
def test_create_notifier_linux(mock_platform_system: Mock):
    platform = Platforms.LINUX.value
    mock_platform_system.return_value = platform

    with pytest.raises(NotSupportedPlatformException):
        _ = create_validator_chain()
        mock_platform_system.assert_called_once()
