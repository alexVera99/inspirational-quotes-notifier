import pytest
from inspi_quote_notifier.quotes.application.validators.base_validator import (
    BaseValidator,
)
from inspi_quote_notifier.quotes.domain.quote import Quote

validator = BaseValidator()


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
