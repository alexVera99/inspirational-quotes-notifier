from quotes.domain.quote import Quote


class DataValidator:
    def __init__(self, default_author="Unknown"):
        self.default_author = default_author

    def validate(self, quote: Quote) -> Quote:
        text: str = quote.text
        author: str = quote.author

        if text is None:
            text = ""
            author = ""

        if author is None:
            author = self.default_author

        return Quote(author, text)
