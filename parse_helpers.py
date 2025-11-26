import js_structures

def isDeclaration(js_str):
    js_str = js_str.lstrip()
    
    # expression is a declaration if it starts with one of these keywords
    return js_str.startswith(("let ", "var ", "const "))

def parseExpression(js_str, window):
    # remove semicolon if present
    pass

def performDeclaration(js_str, window):
    # preprocessing - extract keyword, name, and expression 
    if js_str.startswith(("let ", "var ")):
        init_keyword = js_str[0:3]
    elif js_str.startswith("const "):
        init_keyword = "const"
    else:
        raise Exception("Invalid JS declaration: initializer not recognized")
    
    js_str = js_str.replace(init_keyword + " ", "", 1).lstrip()

    # extract variable name and check if it follows variable name rules

    if js_str[0] != "=":
        raise Exception("Invalid JS declaration: missing equals sign")
    
    js_str = js_str[1:].rstrip()

    if js_str[-1] == ";":
        js_str = js_str[:-1]

    
    

    

    


    

    

    

# JSError(f"SyntaxError: Identifier '{var_name}' has already been declared.")
# JSError("SyntaxError: Missing initializer in const declaration.")