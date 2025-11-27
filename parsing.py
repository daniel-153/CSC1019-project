import parse_helpers

def parseExpression(js_str, window):
    js_str = parse_helpers.preProcessExpr(js_str)


def performDeclaration(js_str, window):
    dec_keyword, js_str = parse_helpers.extractDecKeyword(js_str)
    var_name, js_str = parse_helpers.extractVarName(js_str)
    
    parse_helpers.checkVariableName(var_name, window)

    expr = parse_helpers.preProcessExpr(js_str)
    expr = parse_helpers.preProcessInitExpr(dec_keyword, expr)

    value = parseExpression(expr, window)
    parse_helpers.createVariable(dec_keyword, var_name, value, window)

def performAssignment(js_str, window):
    var_name, expr = parse_helpers.extractVarName(js_str)

    parse_helpers.checkVariableExists(var_name, window)
    new_value = parseExpression(expr, window)
    parse_helpers.updateVariableValue(var_name, new_value, window)

    return new_value

def parse(js_line, window):
    try:
        eval_result = {}

        if parse_helpers.isDeclaration(js_line):
            performDeclaration(js_line, window)
            eval_result["value"] = ""
        elif parse_helpers.isAssignment(js_line):
            eval_result["value"] = performAssignment(js_line, window)
        else:
            eval_result["value"] = parseExpression(js_line, window)
    except Exception as e:
        eval_result["is_error"] = True
        
        if getattr(e, "is_js_error"):
            eval_result["error_msg"] = str(e)
        else:
            eval_result["error_msg"] = "ParsingError: unrecognized or unsupported JavaScript syntax"
    finally:
        if eval_result.get("is_error"):
            return "\u29BB " + str(eval_result.get("error_msg"))
        else:
            return eval_result.get("value")