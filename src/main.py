import os

import apiReader
from pync import Notifier

default_author = "Someone"
ar = apiReader.ApiReader(default_author)

quote_text, quote_author = ar.get_one_quote(True)

# Create macOS notification with the selected quote
Notifier.notify(
    quote_text, title=quote_author + " once said:", group=os.getpid(), sound="Submarine"
)
