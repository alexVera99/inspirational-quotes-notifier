import apiReader
from pync import Notifier
import os

ar = apiReader.apiReader()

quote_text, quote_author = ar.getOneQuote(True)

# Create MacOS notification with the selected quote
Notifier.notify(quote_text, title=quote_author + " once said:", group=os.getpid(), sound="Submarine")#, ignoreDnD=False)
