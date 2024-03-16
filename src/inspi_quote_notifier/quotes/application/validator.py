from inspi_quote_notifier.quotes.domain.quote import Quote


class DataValidator:
    def __init__(self, max_size_quote: int = 84):
        # Max size of the quote to be displayed correctly in the notifications
        self.max_size_quote = max_size_quote

    def validate(self, quote: Quote) -> bool:
        text: str = quote.text
        author: str = quote.author

        if text is None:
            return False

        if author is None:
            return False

        if len(text) >= self.max_size_quote:
            return False

        return True
