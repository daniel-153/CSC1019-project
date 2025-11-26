class Error(Exception):
    def __init__(self, error_type, description):
        self.error_type = error_type
        self.description = description
        self.is_js_error = True

        super().__init__(f"{error_type}Error: {description}")

class Variable:
    def __init__(self, init_type, name, value):
        # dont allow reserved keywords
        if name in ['quit', 'NaN', 'true', 'false', 'let', 'var', 'const']:
            raise Error("Syntax", f"'{name}' is a reserved keyword")

        self.init_type = init_type
        self.name = name
        self.value = value