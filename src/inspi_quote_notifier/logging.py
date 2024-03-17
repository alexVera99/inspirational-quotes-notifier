import logging

LOG_FILENAME = "inspi_notifier.log"
LOG_FORMAT = (
    "%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d: %(message)s"
)
LOG_LEVEL = logging.DEBUG


def configure_logging() -> None:
    logging.basicConfig(filename=LOG_FILENAME, level=LOG_LEVEL, format=LOG_FORMAT)
