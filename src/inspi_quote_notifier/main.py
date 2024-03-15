from inspi_quote_notifier.api_reader import ApiReader
from inspi_quote_notifier.notifications.factory import create_notifier


def main() -> None:
    notifier = create_notifier()

    default_author = "Someone"
    ar = ApiReader(default_author)

    quote = ar.get_one_quote(True)

    notifier.notify(quote)
