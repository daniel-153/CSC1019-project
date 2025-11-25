class JSError(Exception):
    pass

def getExprSignature(expr):
    pass

def parseJsExpr(expr):
    pass

def performJsAssignment(expr):
    pass

def getLineValue(expr):
    pass

def eval_js(js_line, window):
    eval_result = {}
    
    try:
        signature = getExprSignature(js_line)

        expr_value = parseJsExpr(signature["expression"])

        if signature["is_assigment"]:
            performJsAssignment(signature, expr_value, window)
        
        eval_result["value"] = getLineValue(signature, expr_value)
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
            return str(eval_result.get("value"))