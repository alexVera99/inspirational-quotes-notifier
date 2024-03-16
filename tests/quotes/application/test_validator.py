import pytest
from inspi_quote_notifier.quotes.application.validator import DataValidator
from inspi_quote_notifier.quotes.domain.quote import Quote

validator = DataValidator()


def test_validate():
    quote = Quote("Some author", "Some text")

    result = validator.validate(quote)

    assert result


@pytest.mark.parametrize(
    "quote",
    [
        (Quote("Some author", None)),
        (Quote(None, "Some text")),
        (Quote(None, None)),
    ],
)
def test_validate_quote_empty(quote):
    result = validator.validate(quote)

    assert not result


def test_validate_quote_text_larger_than_max_chars():
    text = "a" * (validator.max_size_quote + 1)

    quote = Quote("Some author", text)

    result = validator.validate(quote)

    assert not result
