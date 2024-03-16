from unittest.mock import Mock

from inspi_quote_notifier.quotes.application.validators.chain_validator import (
    ChainValidator,
)
from inspi_quote_notifier.quotes.domain.quote import Quote
from inspi_quote_notifier.quotes.domain.validator import Validator


def test_validate():
    mock_validator_1 = Mock(spec=Validator)
    mock_validator_2 = Mock(spec=Validator)

    mock_validator_1.validate.return_value = True
    mock_validator_2.validate.return_value = True

    validators = [mock_validator_1, mock_validator_2]

    validator_chain = ChainValidator(validators)

    assert validator_chain.validate(Mock(spec=Quote))


def test_validate_with_one_validator_fail():
    mock_validator_1 = Mock(spec=Validator)
    mock_validator_2 = Mock(spec=Validator)

    mock_validator_1.validate.return_value = False
    mock_validator_2.validate.return_value = True

    validators = [mock_validator_1, mock_validator_2]

    validator_chain = ChainValidator(validators)

    assert not validator_chain.validate(Mock(spec=Quote))
