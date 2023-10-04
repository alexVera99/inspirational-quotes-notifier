from inspi_quote_notifier.api_reader import ApiReader
from inspi_quote_notifier.notifications.macos.notifier_osx import NotifierOSX
from inspi_quote_notifier.notifications.notifier import Notifier

notifier: Notifier = NotifierOSX()

default_author = "Someone"
ar = ApiReader(default_author)

quote = ar.get_one_quote(True)

notifier.notify(quote)
