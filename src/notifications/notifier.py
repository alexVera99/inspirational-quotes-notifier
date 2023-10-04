from abc import ABC
from abc import abstractmethod

from quotes.domain.quote import Quote


class Notifier(ABC):
    @abstractmethod
    def notify(self, quote: Quote):
        pass
