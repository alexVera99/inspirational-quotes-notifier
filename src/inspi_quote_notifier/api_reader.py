import logging
import random
from typing import Optional

import requests
from inspi_quote_notifier.quotes.application.validator import DataValidator
from inspi_quote_notifier.quotes.domain.quote import Quote
from requests import RequestException


class ApiReader:
    DEFAULT_QUOTE_TEXT = "Play wisely the cards life gave you."
    DEFAULT_QUOTE_AUTHOR = "Yourself"

    DEFAULT_QUOTE = Quote(DEFAULT_QUOTE_AUTHOR, DEFAULT_QUOTE_TEXT)

    def __init__(
        self,
        default_author: str = "Unknown",
        api_url: str = "https://type.fit/api/quotes",
    ) -> None:
        # Max size of the quote to be displayed correctly in the notifications
        self.max_size_quote = 84

        # Setting the max number of requests
        self.max_num_requests = 10

        # Initializing the logger
        self.logger = logging.getLogger(ApiReader.__name__)

        # Data validator
        self.validator = DataValidator(default_author)

        self.max_num_quotes_retries = 10

        # API url
        self.api_url = api_url

    def get_one_quote(self) -> Quote:
        quotes = self.read_quotes_from_api()

        if quotes is None:
            return ApiReader.DEFAULT_QUOTE

        # reading the JSON information
        data_size = len(quotes)

        for _ in range(0, self.max_num_quotes_retries):
            # Generating a random number to choose a random quote
            seed = random.randint(0, data_size - 1)

            # Choose the quote
            quote = quotes[seed]
            validated_quote = self.validator.validate(quote)

            if len(validated_quote.text) <= self.max_size_quote:
                return validated_quote

        self.logger.debug(
            "Could not obtain a proper quote from the ones provided by the API"
        )

        return ApiReader.DEFAULT_QUOTE

    def read_quotes_from_api(self) -> Optional[list[Quote]]:
        for num_requests in range(1, self.max_num_requests + 1):
            try:
                quotes = self.get_quotes()
                if quotes is not None:
                    return quotes

                self.logger.debug(f"Number of requests: {num_requests}")

            except RequestException as e:
                self.logger.error(f"Could not retrieve quotes from API due to {e}")

        return None

    def get_quotes(self) -> Optional[list[Quote]]:
        r = requests.get(self.api_url)

        if r.status_code != 200:
            return None

        data = r.json()

        return list(map(ApiReader.convert_to_quote, data))

    @staticmethod
    def convert_to_quote(raw_quote: dict) -> Quote:
        return Quote(raw_quote["author"], raw_quote["text"])
