from inspi_quote_notifier.quotes.domain.quote import Quote
from inspi_quote_notifier.quotes.domain.validator import Validator


class BaseValidator(Validator):
    def validate(self, quote: Quote) -> bool:
        return quote.text is not None and quote.author is not None
