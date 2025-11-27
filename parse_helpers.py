import js_structures
import js_types
import js_operators

def isDeclaration(js_str):
    js_str = js_str.lstrip()
    
    # expression is a declaration if it starts with one of these keywords
    return js_str.startswith(("let ", "var ", "const "))

def isAssignment(js_str):
    for symbol in ["===", "!==", "==", "!=", ">=", ">="]:
        js_str.replace(symbol, "")

    js_str = js_str.split("'")[0].split('"')[0]

    return "=" in js_str

def checkVariableName(name_str, window): # raises if name isn't valid
    # checks basic rules
    for idx, char in enumerate(name_str):
        if idx == 0 and not (
            char.isalpha() or
            char == "_"
        ): 
            raise js_structures.Error("Syntax", "invalid first character in variable name")
        elif not (
            char.isalpha() or
            char.isdigit() or
            char == "_"
        ): 
            return js_structures.Error("Syntax", f"invalid character in variable name at index {idx}")
    
    # checks reserved keywords and if var already has been declared
    if name_str in ['quit', 'NaN', 'true', 'false', 'let', 'var', 'const', 'undefined', 'null']:
        raise js_structures.Error("Syntax", f"'{name_str}' is a reserved keyword")
    
    if name_str in window:
        raise js_structures.Error("Syntax", f"Identifier '{name_str}' has already been declared")

def extractDecKeyword(dec_str):
    dec_str = dec_str.lstrip()
    if dec_str.startswith(("let ", "var ")):
        dec_keyword = dec_str[0:3]
    elif dec_str.startswith("const "):
        dec_keyword = "const"
    else:
        raise Exception("Invalid JS declaration: initializer not recognized")
    
    js_str = js_str.replace(dec_keyword, "", 1)

    return dec_keyword, dec_str

def extractVarName(dec_str):
    dec_str = dec_str.lstrip()
    var_name = dec_str.split('=')[0].rstrip()
    dec_str = dec_str.replace(var_name, "", 1).lstrip()

    if dec_str[0] != "=":
        raise Exception("Invalid JS declaration: missing equals sign")
    
    dec_str = dec_str[1:]

    return var_name, dec_str

def preProcessInitExpr(dec_keyword, expr_str):
    if len(expr_str) == 0 and dec_keyword == "const":
        js_structures.Error("Syntax", "Missing initializer in const declaration")
    elif len(expr_str) == 0:
        return "undefined"
    else:
        return expr_str
    
def createVariable(dec_keyword, name, value, window):
    window[name] = js_structures.Variable(dec_keyword, name, value)

def checkVariableExists(var_name, window):
    if not var_name in window:
        raise js_structures.Error("Reference", f"'{var_name}' is not defined")

def updateVariableValue(var_name, new_value, window):
    if window[var_name].dec_keyword == "const":
        raise js_structures.Error("Type", "Assignment to constant variable") 
    
    window[var_name].value = new_value

def preProcessExpr(expr_str):
    expr_str = expr_str.strip()

    if expr_str[-1] == ";":
        expr_str = expr_str[:-1]

    # remove whitespace except between quotes
    quote_flag = {"is_inside": False, "type": None}
    processed_expr = ""

    for char in expr_str:
        if char == " " and not quote_flag["is_inside"]:
            continue
        
        if char == "'" or char == "\"":
            if not quote_flag["is_inside"]: # opening quote
                quote_flag["is_inside"] = True
                quote_flag["type"] = char
            elif quote_flag["is_inside"] and char == quote_flag["type"]: # closing quote
                quote_flag["is_inside"] = False
                quote_flag["type"] = None
            
        processed_expr += char
            
    return processed_expr

def matchFixedTokens(tkn_str, include = ["literal", "arithmetic", "comparison", "parenthesis"]):
    forms = {
        "literal": ["NaN", "null", "true", "false", "undefined"],
        "arithmetic": ["+", "-", "*", "/", "%", "**"],
        "comparison": ["==", "!=", "===", "!==", ">", "<", ">=", "<=", "&&", "||"],
        "parenthesis": ["(", ")"]
    }

    included_forms = [form[1] for form in forms.items() if form[0] in include]
    match_strings = [item for sublist in included_forms for item in sublist] # flattens the 2d array

    matches = 0
    for form in match_strings:
        if len(tkn_str) > len(form):
            continue
        elif tkn_str == form[0:len(tkn_str)]:
            matches += 1

    return matches

def matchNumericalToken(tkn_str):
    if ( # note string construction (type conversions like false -> 0 won't happen)
        tkn_str[0] != "-" and (
            js_types.Number(js_types.String(tkn_str)).value != "NaN" or 
            tkn_str == "."
        ) 
    ):
        return 1
    else:
        return 0
    
def matchStringToken(tkn_str):
    if tkn_str[0] == "'" or tkn_str[0] == '"':
        open_quote = tkn_str[0]
        quote_count = tkn_str[1:].count(open_quote)

        if (
            quote_count == 0 or
            (quote_count == 1 and tkn_str[-1] == open_quote)
        ):
            return 1
        else:
            return 0
    else:
        return 0
    
def matchVariableToken(tkn_str):
    for idx, char in enumerate(tkn_str):
        if idx == 0 and not (
            char.isalpha() or
            char == "_"
        ):
            return 0
        elif not (
            char.isalpha() or
            char.isdigit() or
            char == "_"
        ):
            return 0

    return 1

def numTokenMatches(tkn_str):
    return (
        matchFixedTokens(tkn_str) +
        matchNumericalToken(tkn_str) +
        matchStringToken(tkn_str) +
        matchVariableToken(tkn_str)
    )

def tokenize(expr_str):
    # assumes whitespace is already normalized
    tokens = []
    while len(expr_str) > 0:
        tkn_buffer = ""
        last_matches = 0
        
        for idx, char in enumerate(expr_str):
            tkn_buffer += char
            num_matches = numTokenMatches(tkn_buffer)

            if num_matches == 0 and last_matches >= 1:
                tokens.append(tkn_buffer[:-1])
                expr_str = expr_str[len(tkn_buffer) - 1:]
                tkn_buffer = ""
                break
            elif num_matches == 1 and idx == len(expr_str) - 1:
                tokens.append(tkn_buffer)
                tkn_buffer = expr_str = ""
            
            last_matches = num_matches

        if len(tkn_buffer) > 0:
            raise Exception(f"Unable to JS tokenize '{tkn_buffer}'")
        
    if len(tokens) > 0 and (
        len(tokens[-1]) >= 2 and
        tokens[-1][0] in ["'", '"'] and
        tokens[-1][0] != tokens[-1][-1]
    ):
        raise Exception(f"Unterminated JS string")
    
    return tokens

def isAtomic(tkn):
    return bool(
        matchFixedTokens(tkn, ["literal", "parenthesis"]) +
        matchNumericalToken(tkn) +
        matchStringToken(tkn) +
        matchVariableToken(tkn)
    )

def isOperator(tkn):
    return bool(
        matchFixedTokens(tkn, ["arithmetic", "comparison"])
    )

def resolveUnaryMinus(token_list):
    modified_tokens = []
    for idx, curr_tkn in enumerate(token_list):
        prev_tkn = None if (idx - 1) < 0 else token_list[idx - 1]
        next_tkn = None if (idx + 1) > len(token_list) - 1 else token_list[idx + 1]

        if (
            curr_tkn == "-" and
            next_tkn is not None and
            isAtomic(next_tkn) and (
                prev_tkn is None or 
                prev_tkn == "(" or
                isOperator(prev_tkn)
            )
        ):
            modified_tokens.append("-1")
            modified_tokens.append("*")
        else:
            modified_tokens.append(curr_tkn)

    return modified_tokens
    
print(resolveUnaryMinus(tokenize(preProcessExpr( # tester
    "3+-4"
))))