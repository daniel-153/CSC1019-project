class Error(Exception):
    def __init__(self, error_type, description):
        self.error_type = error_type
        self.description = description
        self.is_js_error = True

        super().__init__(f"{error_type}Error: {description}")

class Variable:
    def __init__(self, dec_keyword, name, value):
        self.dec_keyword = dec_keyword
        self.name = name
        self.value = value