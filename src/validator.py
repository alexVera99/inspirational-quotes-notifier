class DataValidator:
    def __init__(self, default_author='Unknown'):
        self.default_author = default_author

    def validateData(self, quote, author):
        if quote == None:
            success = False
            quote = ''
            author = ''
            return success, quote, author
        elif author == None:
            success = True
            return success, quote, self.default_author
        
        return True, quote, author
        