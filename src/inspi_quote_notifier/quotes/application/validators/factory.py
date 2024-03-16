import platform

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
from inspi_quote_notifier.quotes.application.validators.osx_validator import (
    OSXValidator,
)
from inspi_quote_notifier.quotes.domain.validator import Validator


def create_validator_chain() -> Validator:
    current_platform = platform.system()
    if current_platform == Platforms.MACOS.value:
        validators = [BaseValidator(), OSXValidator()]

        return ChainValidator(validators)

    elif current_platform == Platforms.WINDOWS.value:
        raise NotSupportedPlatformException(current_platform)

    elif current_platform == Platforms.LINUX.value:
        raise NotSupportedPlatformException(current_platform)

    else:
        raise NotSupportedPlatformException(current_platform)
