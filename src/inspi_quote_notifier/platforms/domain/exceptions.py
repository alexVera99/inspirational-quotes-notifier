class NotSupportedPlatformException(Exception):
    def __init__(self, current_platform: str):
        super().__init__(f'The platform "{current_platform}" is not supported.')
