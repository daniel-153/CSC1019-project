import js_structures
import js_types
import js_operators

"""
File purpose: contain all the small helper
functions for parsing. Most are responsible
for string matching and tokenizing (making sense
of the JS code). The last two functions do
the evaluation (with recursion).
"""

def isDeclaration(js_str):
    js_str = js_str.lstrip()
    
    # expression is a declaration if it starts with one of these keywords
    return js_str.startswith(("let ", "var ", "const "))

def isAssignment(js_str):
    for symbol in ["===", "!==", "==", "!=", ">=", "<="]:
        js_str = js_str.replace(symbol, "")

    js_str = js_str.split("'")[0].split('"')[0]

    return "=" in js_str

def checkVariableName(name_str, window): # raises if name isn't valid
    js_structures.Variable('let', name_str, None) # validates name characters
    
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
    
    dec_str = dec_str.replace(dec_keyword, "", 1)

    return dec_keyword, dec_str

def extractDecVarName(dec_str):
    copy_dec_str = dec_str
    if isAssignment(dec_str):
        copy_dec_str = dec_str.split("=")[0]

    var_name = copy_dec_str.split(";")[0].strip()
    dec_str = dec_str.replace(var_name, "", 1).strip()

    if len(dec_str) > 0 and dec_str[0] == "=":
        dec_str = dec_str[1:]

    return var_name, dec_str

def extractVarName(assign_str):
    assign_str = assign_str.lstrip()
    var_name = assign_str.split('=')[0].rstrip()
    assign_str = assign_str.replace(var_name, "", 1).lstrip()

    if assign_str[0] != "=":
        raise Exception("Invalid JS assignment: missing equals sign")
    
    assign_str = assign_str[1:]

    return var_name, assign_str

def preProcessInitExpr(dec_keyword, expr_str):
    if len(expr_str) == 0 and dec_keyword == "const":
        raise js_structures.Error("Syntax", "Missing initializer in const declaration")
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

    if len(expr_str) > 0 and expr_str[-1] == ";":
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
    if tkn_str == ".":
        return 1
    elif tkn_str[0] == "-" or tkn_str == "NaN":
        return 0
    
    try:
        js_types.Number(tkn_str)
        return 1
    except js_types.Primitive.ConstructorError:
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
    try:
        js_structures.Variable('let', tkn_str, None)
        return 1
    except js_structures.Error:
        return 0

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
            elif num_matches >= 1 and idx == len(expr_str) - 1:
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
        matchFixedTokens(tkn, ["literal"]) +
        matchNumericalToken(tkn) +
        matchStringToken(tkn) +
        matchVariableToken(tkn) +
        int(tkn == "(")
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

def detectToken(tkn_str):
    match_found = False
    for TokenType in [
        js_structures.Identifier,
        js_structures.Literal, 
        js_structures.Operator, 
        js_structures.Parenthesis
    ]:
        try:
            matched_tkn = TokenType(tkn_str)
            match_found = True
            break
        except js_structures.Token.TokenError:
            pass

    if not match_found:
        raise js_structures.Error("Syntax", f"invalid token '{tkn_str}'")

    return matched_tkn

def typeTokenList(token_list): # turns literal tokens into JS types
    typed_list = []
    for tkn_str in token_list:
        tkn_type = detectToken(tkn_str)

        if isinstance(tkn_type, js_structures.Literal):
            typed_list.append(js_types.Auto(tkn_str))
        else:
            typed_list.append(tkn_type) 

    return typed_list

def resolveVariableRefs(typed_tokens, window):
    resolved_tokens = []
    for token in typed_tokens:
        if isinstance(token, js_structures.Identifier):
            if token.tkn_str in window:
                resolved_tokens.append(window[token.tkn_str].value)
            else:
                raise js_structures.Error("Reference", f"'{token.tkn_str}' is not defined")
        else:
            resolved_tokens.append(token)

    return resolved_tokens

def findClosingParen(typed_tokens, index):
    if not (
        isinstance(typed_tokens[index], js_structures.Parenthesis) and
        typed_tokens[index].tkn_str == "("
    ):
        raise Exception("Provided index is not an opening paren")

    depth = 1
    sub_index = index + 1
    while sub_index < len(typed_tokens):
        if isinstance(typed_tokens[sub_index], js_structures.Parenthesis):
            tkn = typed_tokens[sub_index].tkn_str
            if tkn == "(":
                depth += 1
            elif tkn == ")":
                depth -= 1
                if depth == 0:
                    return sub_index

        sub_index += 1

    return -1

def checkParenClosing(typed_tokens):
    depth = 0
    for token in typed_tokens:
        if isinstance(token, js_structures.Parenthesis):
            if token.tkn_str == "(":
                depth += 1
            elif token.tkn_str == ")":
                depth -= 1
        
        if depth < 0:
            raise js_structures.Error("Syntax", "Unexpected token ')'")
    
    if depth != 0:
        raise js_structures.Error("Syntax", "Unexpected end of input")
    
def detectOperatorType(typed_tkn):
    if isinstance(typed_tkn, js_structures.Operator):
        if matchFixedTokens(typed_tkn.tkn_str, ["arithmetic"]):
            return "arithmetic"
        elif matchFixedTokens(typed_tkn.tkn_str, ["comparison"]):
            return "comparison"

    raise Exception(f"Provided token '{typed_tkn.tkn_str}' is not an operator")

def getOrderedOperators(flat_expr): # assumes expr is properly ordered (val op val op val...)
    operators = [item for index, item in enumerate(flat_expr) if index % 2 == 1]
    sorted_ops = []

    while len(operators) > 0:
        highest_prec = max(operators, key = lambda operator: operator.power).power
        direction = js_structures.Operator.binding_powers[highest_prec]["direction"]

        updated_ops = []
        iter_ops = operators if direction > 0 else list(reversed(operators))

        for op in iter_ops:
            if op.power == highest_prec:
                sorted_ops.append(op)
            else:
                updated_ops.append(op)

        operators = updated_ops if direction > 0 else list(reversed(updated_ops))

    return sorted_ops

def evalFlatExpr(flat_expr): # list of only primitives and operators (correct order already checked)
    for operator in getOrderedOperators(flat_expr):
        found_idx = flat_expr.index(operator)
        operand1, operator, operand2 = flat_expr[found_idx - 1:found_idx + 2]
        operator_type = detectOperatorType(operator)

        value = getattr(js_operators, operator_type)(operand1, operand2, operator.tkn_str)

        flat_expr = flat_expr[:found_idx - 1] + [value] + flat_expr[found_idx + 2:]

    return flat_expr[0]

def evalExprList(expr_list): # list of primitives, operator tokens, and paren tokens (paren closing already checked before this runs)
    if len(expr_list) == 0:
        raise Exception("Cannot evaluate empty expression")
    
    # recursively eval parens until the expression is just atoms and operators
    flat_expr = []
    while len(expr_list) > 0:
        curr_entry = expr_list[0]

        if (
            isinstance(curr_entry, js_types.Primitive) or
            isinstance(curr_entry, js_structures.Operator)
        ):
            flat_expr.append(expr_list.pop(0))
        elif isinstance(curr_entry, js_structures.Parenthesis):
            closing_idx = findClosingParen(expr_list, 0)
            flat_expr.append(evalExprList(expr_list[1:closing_idx]))
            expr_list = expr_list[closing_idx + 1:]
        else:
            raise Exception(f"Unexpected expression item '{curr_entry}' type of '{type(curr_entry)}'")
        
    # check if expr is atoms and operators (in correct order)
    correct_order = True
    for idx, item in enumerate(flat_expr):
        if idx % 2 == 0:
            if not isinstance(item, js_types.Primitive):
                correct_order = False
                break
        else:
            if not isinstance(item, js_structures.Operator): 
                correct_order = False
                break

    if not correct_order or len(flat_expr) % 2 != 1:
        raise js_structures.Error("Syntax", "Invalid expression")
    
    return evalFlatExpr(flat_expr)