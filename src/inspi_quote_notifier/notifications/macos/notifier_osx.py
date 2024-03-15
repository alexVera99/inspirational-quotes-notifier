import os

from inspi_quote_notifier.notifications.notifier import Notifier
from inspi_quote_notifier.quotes.domain.quote import Quote
from pync import notify


class NotifierOSX(Notifier):
    def __init__(self) -> None:
        self.sound = "Submarine"

    def notify(self, quote: Quote) -> None:
        title = quote.author + " once said:"

        notify(quote.text, title=title, group=os.getpid(), sound=self.sound)
