import js_types

"""
File purpose: defines some classes that
are used for parsing. Error and Variable
are used for making those structures in JS.
The Token classes are used for taking a raw
string like "x * 3 + 2" and sorting its pieces
into categories [x, *, 3, +, 2].
"""

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
    binding_powers = { # for operator precedence
        1: {"symbols": ["||"], "direction": 1},
        2: {"symbols": ["&&"], "direction": 1},
        3: {"symbols": ["==", "!=", "===", "!=="], "direction": 1},
        4: {"symbols": [">", "<", ">=", "<="], "direction": 1},
        5: {"symbols": ["+", "-"], "direction": 1},
        6: {"symbols": ["*", "/", "%"], "direction": 1},
        7: {"symbols": ["**"], "direction": -1}
    }

    def __init__(self, tkn_str):
        super().__init__(tkn_str)
        match_found = False
        match_power = None
        for power, entry in self.binding_powers.items():
            if tkn_str in entry["symbols"]:
                match_found = True
                match_power = power
                break

        if not match_found:
            raise self.TokenError(self, tkn_str)
        
        self.power = match_power
        self.direction = self.binding_powers[match_power]["direction"]
        
class Parenthesis(Token): 
    def __init__(self, tkn_str):
        super().__init__(tkn_str)

        if not tkn_str in ["(", ")"]:
            raise self.TokenError(self, tkn_str)