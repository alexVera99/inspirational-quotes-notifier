class DataValidator:
    def __init__(self, default_author="Unknown"):
        self.default_author = default_author

    def validate(self, quote, author):
        success = True
        if quote is None:
            success = False
            quote = ""
            author = ""

        elif author is None:
            author = self.default_author

        return success, quote, author
