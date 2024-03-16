import logging

from inspi_quote_notifier.quotes.domain.quote import Quote
from inspi_quote_notifier.quotes.domain.validator import Validator


class ChainValidator(Validator):
    def __init__(self, validators: list[Validator]):
        self.validators = validators
        self.logger = logging.getLogger(ChainValidator.__name__)

    def validate(self, quote: Quote) -> bool:
        for validator in self.validators:
            if not validator.validate(quote):
                self.logger.info("Validator %s failed with quote %s", validator, quote)
                return False

        return True
