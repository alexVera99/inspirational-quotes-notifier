from inspi_quote_notifier.quotes.application.validators.osx_validator import (
    OSXValidator,
)
from inspi_quote_notifier.quotes.domain.quote import Quote

validator = OSXValidator()


def test_validate_quote_text_larger_than_max_chars():
    text = "a" * (validator.max_size_quote + 1)

    quote = Quote("Some author", text)

    result = validator.validate(quote)

    assert not result
