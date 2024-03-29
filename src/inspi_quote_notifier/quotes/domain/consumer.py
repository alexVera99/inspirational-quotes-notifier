from abc import ABC
from abc import abstractmethod

from inspi_quote_notifier.quotes.domain.quote import Quote


class QuoteConsumer(ABC):
    @abstractmethod
    def get_quotes(self) -> list[Quote]:
        pass
