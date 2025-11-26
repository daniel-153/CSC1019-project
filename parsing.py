import parse_helpers

def parse(js_line, window):
    try:
        eval_result = {}

        if parse_helpers.isDeclaration(js_line):
            parse_helpers.performDeclaration(js_line, window)
            eval_result["value"] = "\n"
        else:
            eval_result["value"] = parse_helpers.parseExpression(js_line, window)
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