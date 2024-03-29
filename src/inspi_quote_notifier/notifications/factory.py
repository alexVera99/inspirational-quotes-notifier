import platform

from inspi_quote_notifier.notifications.macos.notifier_osx import NotifierOSX
from inspi_quote_notifier.notifications.notifier import Notifier
from inspi_quote_notifier.platforms.domain.exceptions import (
    NotSupportedPlatformException,
)
from inspi_quote_notifier.platforms.domain.platforms import Platforms


def create_notifier() -> Notifier:
    current_platform = platform.system()
    if current_platform == Platforms.MACOS.value:
        return NotifierOSX()
    elif current_platform == Platforms.WINDOWS.value:
        raise NotSupportedPlatformException(current_platform)
    elif current_platform == Platforms.LINUX.value:
        raise NotSupportedPlatformException(current_platform)
    else:
        raise NotSupportedPlatformException(current_platform)
