from inspi_quote_notifier.quotes.domain.quote import Quote
from inspi_quote_notifier.quotes.domain.validator import Validator


class OSXValidator(Validator):
    def __init__(self, max_size_quote: int = 84):
        # Max size of the quote to be displayed correctly in macOS notifications
        self.max_size_quote = max_size_quote

    def validate(self, quote: Quote) -> bool:
        return len(quote.text) <= self.max_size_quote
