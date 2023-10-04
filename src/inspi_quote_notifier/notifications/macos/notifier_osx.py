import os

from inspi_quote_notifier.notifications.notifier import Notifier
from inspi_quote_notifier.quotes.domain.quote import Quote
from pync import Notifier as pync_notifier


class NotifierOSX(Notifier):
    sound: str = "Submarine"

    def notify(self, quote: Quote):
        title = quote.author + " once said:"

        pync_notifier.notify(
            quote.text, title=title, group=os.getpid(), sound=self.sound
        )
