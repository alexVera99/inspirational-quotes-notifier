import requests
import random
from logger import Logger

class apiReader:

    def __init__(self):
        # Max size of the quote to be displayed correctly in the notifications
        self.max_size_quote = 84 # By prueba and error, I've found that 84 is the max number of characters to be displayed correctly in the notifications

        # Setting the max number of requests
        self.max_num_requests = 10
        self.num_requests = 0

        # Initializing the status code
        self.status_code = 0

        # Default Inspiration Quote
        self.quote_text = "Play wisely the cards life gave you."
        self.quote_author = "Yourself"

        # Initializing the logger
        self.logger = Logger()

    def readQuotesFromAPI(self, debug = False):
        # Read quotes from API
        try:
            # Retrying the request until a 200 status code is obtained or max number of requests is achieved
            while(self.status_code!=200 or self.num_requests == self.max_num_requests):
                # Read quotes from API
                r = requests.get("https://type.fit/api/quotes")
                self.status_code = r.status_code
                self.num_requests += 1
                if debug:
                    # Debug variables. Estaría guay q esto se printará en un log file
                    message_log = "Number of requests: " + str(self.num_requests) + "\n"
                    message_log += "Status code: " + str(self.status_code)
                    self.logger.writeToLogFile(message_log)
                
        except:
            self.status_code = -1 # -1 means no internet conection or some error ocurr 
            return None
        
        return r

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
                self.quote_text = quote["text"]
                self.quote_author = quote["author"]
                if (len(self.quote_text) <= self.max_size_quote):
                    break
        return self.quote_text, self.quote_author
