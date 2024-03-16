import requests
from inspi_quote_notifier.quotes.domain.consumer import QuoteConsumer
from inspi_quote_notifier.quotes.domain.exceptions import QuoteNotFoundException
from inspi_quote_notifier.quotes.domain.quote import Quote
from requests import RequestException
from requests import Response
from retry import retry

MAX_NUMBER_RETRIES = 5


class TypeFitQuoteConsumer(QuoteConsumer):
    def __init__(self) -> None:
        self.api_base_url = "https://type.fit/api/quotes"

    @retry(exceptions=QuoteNotFoundException, tries=MAX_NUMBER_RETRIES)
    def get_quotes(self) -> list[Quote]:
        response = self.request_api()

        if response.status_code != 200:
            raise QuoteNotFoundException(
                f"Couldn't obtain quotes from api at {self.api_base_url}"
            )

        data = response.json()

        return self._parse_quotes(data)

    def request_api(self) -> Response:
        try:
            return requests.get(self.api_base_url)
        except RequestException as e:
            raise QuoteNotFoundException(f"Request error: {e}")

    def _parse_quotes(self, raw_quotes: list[dict]) -> list[Quote]:
        return list(map(self._parse_quote, raw_quotes))

    @staticmethod
    def _parse_quote(raw_quote: dict) -> Quote:
        return Quote(raw_quote["author"], raw_quote["text"])
