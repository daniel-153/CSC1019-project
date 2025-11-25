

def getExprSignature(js_str):
    js_str = js_str.lstrip() # strip leading whitespace

    # expression is a declaration if it starts with one of these keywords
    if js_str.startswith(("let ", "var ", "const ")):
        return JSDeclaration(js_str)
    
    js_str = "".join(js_str.split()) # strip all whitespace

    # expression is an assignment if it has a single equals sign
    eq_index = js_str.find("=") 
    if eq_index != -1 and js_str[eq_index + 1] != "=":
        return JSAssignment(js_str)
        
    # expression is a "simple" expression otherwise
    return JSExpression(js_str)

def performJSAssignment(assignment, window):
    var_name = assignment.var_name
    new_value = assignment.var_value
    
    # check if variable has been declared
    if not var_name in window:
        raise JSError(f"ReferenceError: {var_name} is not defined.")
     
    dec_type = window[var_name][0] # the type of declaration (let, var, or const)

    # if dec_type is const, error, can't assign to a constant variable
    if dec_type == "const":
        raise JSError("TypeError: Assignment to constant variable.")
    
    window[var_name][1] = new_value

def performJSDeclaration(declaration, window):
    var_name = declaration.assignment.var_name
    var_value = declaration.assignment.var_value
    
    # check if variable has already been declared
    if var_name in window:
        raise JSError(f"SyntaxError: Identifier '{var_name}' has already been declared.")
    
    if ( # let and var declarations treated the same
        declaration.keyword == "let" 
        or declaration.keyword == "var"
    ): 
        if var_value is None: # initialize to undefined
            window[var_name] = [declaration.keyword, "undefined"]
        else: # initialize to provided value
            window[var_name] = [declaration.keyword, var_value]
    elif declaration.keyword == "const": # const requires a value
        if var_value is None: # error, const initialization must have a value
            raise JSError("SyntaxError: Missing initializer in const declaration.")
        else: # initialize to provided value
            window[var_name] = [declaration.keyword, var_value]

def eval_js(js_line, window):
    eval_result = {}
    
    try:
        signature = getExprSignature(js_line)

        if isinstance(signature, JSExpression):
            eval_result["value"] = signature.value
        elif isinstance(signature, JSAssignment):
            performJSAssignment(signature, window)
            eval_result["value"] = signature.var_value
        elif isinstance(signature, JSDeclaration):
            performJSDeclaration(signature, window)
            eval_result["value"] = "undefined"
    except Exception as e:
        eval_result["is_error"] = True
        
        if isinstance(e, JSError):
            eval_result["error_msg"] = str(e)
        else:
            eval_result["error_msg"] = "ParsingError: " + str(e)
    finally:
        if eval_result.get("is_error"):
            return "\u29BB " + str(eval_result.get("error_msg"))
        else:
            return eval_result.get("value")