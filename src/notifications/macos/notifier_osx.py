import os

from notifications.notifier import Notifier
from pync import Notifier as pync_notifier
from quotes.domain.quote import Quote


class NotifierOSX(Notifier):
    sound: str = "Submarine"

    def notify(self, quote: Quote):
        title = quote.author + " once said:"

        pync_notifier.notify(
            quote.text, title=title, group=os.getpid(), sound=self.sound
        )
