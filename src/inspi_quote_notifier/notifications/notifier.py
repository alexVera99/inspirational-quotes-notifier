from abc import ABC
from abc import abstractmethod

from inspi_quote_notifier.quotes.domain.quote import Quote


class Notifier(ABC):
    @abstractmethod
    def notify(self, quote: Quote):
        pass
