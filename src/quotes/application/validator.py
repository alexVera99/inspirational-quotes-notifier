class DataValidator:
    def __init__(self, default_author='Unknown'):
        self.default_author = default_author

    def validate(self, quote, author):
        success = True
        if quote == None:
            success = False
            quote = ''
            author = ''

        elif author == None:
            author = self.default_author
        
        return success, quote, author
        