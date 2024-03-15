import platform
from enum import Enum

from inspi_quote_notifier.notifications.macos.notifier_osx import NotifierOSX
from inspi_quote_notifier.notifications.notifier import Notifier


class Platforms(Enum):
    MACOS = "Darwin"
    WINDOWS = "Windows"
    LINUX = "Linux"


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


class NotSupportedPlatformException(Exception):
    def __init__(self, current_platform: str):
        super().__init__(f'The platform "{current_platform}" is not supported.')
