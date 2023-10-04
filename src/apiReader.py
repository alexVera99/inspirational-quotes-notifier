import requests
import random

from requests import RequestException

from logger import Logger
from validator import DataValidator

class ApiReader:

    def __init__(self, default_author='Unknown', api_url = "https://type.fit/api/quotes"):
        # Max size of the quote to be displayed correctly in the notifications
        self.max_size_quote = 84 # By prueba and error, I've found that 84 is the max number of characters to be displayed correctly in the notifications

        # Setting the max number of requests
        self.max_num_requests = 10

        # Initializing the status code
        self.status_code = 0

        # Default Inspiration Quote when no Internet connection
        self.quote_text = "Play wisely the cards life gave you."
        self.quote_author = "Yourself"

        # Initializing the logger
        self.logger = Logger()

        # Data validator
        self.validator = DataValidator(default_author)

        # API url
        self.api_url = api_url

    def readQuotesFromAPI(self, debug: bool = False):
        for num_requests in range(1, self.max_num_requests + 1):
            try:
                r = requests.get(self.api_url)
                self.status_code = r.status_code
                if self.status_code == 200:
                    return r

                if debug:
                    message_log = "Number of requests: " + str(num_requests) + "\n"
                    message_log += "Status code: " + str(self.status_code)
                    self.logger.writeToLogFile(message_log)

            except RequestException:
                self.status_code = -1

        return None


    def getOneQuote(self, debug = False):
        r = self.readQuotesFromAPI(debug)
        if(self.status_code == 200):
            # reading the JSON information
            data = r.json()
            data_size = len(data)

            while(True):
                # Generating a random number to choose a random quote
                seed = random.randint(0, data_size-1)

                # Choose the quote
                quote = data[seed]
                success, self.quote_text, self.quote_author = self.validator.validateData(quote["text"], quote["author"])

                if (success & len(self.quote_text) <= self.max_size_quote):
                    break
        return self.quote_text, self.quote_author
