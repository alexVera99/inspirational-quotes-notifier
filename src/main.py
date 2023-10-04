from api_reader import ApiReader
from notifications.macos.notifier_osx import NotifierOSX
from notifications.notifier import Notifier

notifier: Notifier = NotifierOSX()

default_author = "Someone"
ar = ApiReader(default_author)

quote = ar.get_one_quote(True)

notifier.notify(quote)
