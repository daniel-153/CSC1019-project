import js_types

class Error(Exception):
    def __init__(self, error_type, description):
        self.error_type = error_type
        self.description = description
        self.is_js_error = True

        super().__init__(f"{error_type}Error: {description}")

class Variable:
    def __init__(self, dec_keyword, name, value):
        # check if the name is valid
        for idx, char in enumerate(name):
            if (
                (idx == 0 and not (char.isalpha() or char == "_")) or
                not (char.isalpha() or char.isdigit() or char == "_")
            ): 
                raise Error("Syntax", f"Invalid identifier '{name}'")
        
        if name in ['quit', 'NaN', 'true', 'false', 'let', 'var', 'const', 'undefined', 'null']:
            raise Error("Syntax", f"'{name}' is a reserved keyword")
        
        self.dec_keyword = dec_keyword
        self.name = name
        self.value = value

class Token:
    def __init__(self, tkn_str):
        self.tkn_str = tkn_str

    class TokenError(Error):
        def __init__(self, intended_type, tkn_str):
            super().__init__("Syntax", f"'{tkn_str}' is not a valid {intended_type.__class__.__name__} token")

class Literal(Token):
    def __init__(self, tkn_str):
        super().__init__(tkn_str)

        try:
            self.data_type = js_types.Auto(tkn_str)
        except js_types.Primitive.ConstructorError:
            raise self.TokenError(self, tkn_str)
        
class Identifier(Token): 
    def __init__(self, tkn_str):
        super().__init__(tkn_str)

        try:
            Variable('let', tkn_str, None)
        except Error:
            raise self.TokenError(self, tkn_str)

class Operator(Token):
    binding_powers = { # for pratt parsing
        1: {"symbols": ["||"], "bias": 0.1},
        2: {"symbols": ["&&"], "bias": 0.1},
        3: {"symbols": ["==", "!=", "===", "!=="], "bias": 0.1},
        4: {"symbols": [">", "<", ">=", "<="], "bias": 0.1},
        5: {"symbols": ["+", "-"], "bias": 0.1},
        6: {"symbols": ["*", "/", "%"]},
        7: {"symbols": ["**"], "bias": -0.1}
    }

    def __init__(self, tkn_str):
        super().__init__(tkn_str)
        match_found = False
        match_power = None
        for power, symbols in self.binding_powers.items():
            if tkn_str in symbols:
                match_found = True
                match_power = power
                break

        if not match_found:
            raise self.TokenError(self, tkn_str)
        
        self.binding_power = (match_power, match_power + self.binding_powers[match_power]["bias"])
        
class Parenthesis(Token): 
    def __init__(self, tkn_str):
        super().__init__(tkn_str)
        
        if not tkn_str in ["(", ")"]:
            raise self.TokenError(self, tkn_str)