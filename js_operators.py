import js_types

# arithmetic_symbols: ["+", "-", "*", "/", "%", "**"]
def arithmetic(operand1, operand2, operator):
    if ( # operation is "+" and at least one operand is a String
        operator == "+" and (
            isinstance(operand1, js_types.String) or
            isinstance(operand2, js_types.String)
        )
    ): # convert to Strings and concatenate
        operand1 = js_types.String(operand1)
        operand2 = js_types.String(operand2)

        return js_types.String(operand1.value + operand2.value)
    else: # both operands must be numbers
        operand1 = js_types.Number(operand1)
        operand2 = js_types.Number(operand2)

        if ( # propagate NaN
            operand1.value == "NaN" or
            operand2.value == "NaN"
        ):
            return js_types.Number("NaN")
        elif operator == "+":
            return js_types.Number(str(operand1.value + operand2.value))       
        elif operator == "-":
            return js_types.Number(str(operand1.value - operand2.value))
        elif operator == "*":
            return js_types.Number(str(operand1.value * operand2.value))    
        elif operator == "/":
            # division has the special case of a zero divisor
            if operand2.value == 0:
                return js_types.Number("NaN") # real JS returns Infinity, but NaN keeps arithmetic simple
            else:
                return js_types.Number(str(operand1.value / operand2.value))  
        elif operator == "%":
            # JS implements a % b as a - trunc(a / b) * b 
            div = arithmetic(operand1, operand2, "/")

            if isinstance(div.value, float):
                div.value = int(div.value)
            
            return arithmetic(operand1, arithmetic(div, operand2, "*"), "-")
        elif operator == "**":
            # exponentiation has the special case of complex numbers, which JS doesn't support
            exp = operand1.value ** operand2.value

            if isinstance(exp, complex):
                return js_types.Number("NaN")
            else:
                return js_types.Number(str(exp))
        else:
            raise Exception(f"Invalid arithmetic operator '{operator}'")

# comparison_symbols: ["==", "!=", "===", "!==", ">", "<", ">=", "<=", "&&", "||"]
def comparison(operand1, operand2, operator):
    if operator == "===": # strict equality
        if ( # per JS spec, comparisons with NaN are always false, even NaN === NaN
            (
                isinstance(operand1, js_types.Number) 
                and operand1.value == "NaN"
            ) or 
            (
                isinstance(operand2, js_types.Number) 
                and operand2.value == "NaN"
            )
        ):
            return js_types.Boolean('false')
        elif (
            type(operand1) is type(operand2) and
            operand1.value == operand2.value
        ):
            return js_types.Boolean('true')
        else:
            return js_types.Boolean('false')
    elif operator == "!==": # negation of strict equality
        result = comparison(operand1, operand2, "===")
        result.value = not result.value

        return result
    elif operator == "==": # loose equality
        # handle specific type conversions
        if (
            isinstance(operand1, js_types.Number) and
            (
                isinstance(operand2, js_types.String) or
                isinstance(operand2, js_types.Boolean)
            )
        ):
            operand2 = js_types.Number(operand2.value)
        elif (
            isinstance(operand2, js_types.Number) and
            (
                isinstance(operand1, js_types.String) or
                isinstance(operand1, js_types.Boolean)
            )
        ):
            operand1 = js_types.Number(operand1.value)
        elif (
            isinstance(operand1, js_types.Undefined) and
            isinstance(operand2, js_types.Null)
        ):
            operand2 = js_types.Undefined('undefined')
        elif (
            isinstance(operand1, js_types.Null) and
            isinstance(operand2, js_types.Undefined)
        ):
            operand2 = js_types.Null('null')

        return comparison(operand1, operand2, "===") # perform normal comparison
    elif operator == "!=": # negation of lose equality
        result = comparison(operand1, operand2, "==")
        result.value = not result.value

        return result
    elif operator in ["<", ">", "<=", ">="]: # numerical comparison (both operands must be numbers)
        operand1 = js_types.Number(operand1)
        operand2 = js_types.Number(operand2)

        result = js_types.Boolean('false')
        if (
            operand1.value == "NaN" or
            operand2.value == "NaN"
        ):
            result.value = False
        elif operator == ">":
            result.value = operand1.value > operand2.value
        elif operator == "<":
            result.value = operand1.value < operand2.value
        elif operator == ">=":
            result.value = operand1.value >= operand2.value
        elif operator == "<=":
            result.value = operand1.value <= operand2.value
        
        return result
    elif operator == "&&" or operator == "||": # logical comparison (both operands must be booleans)
        operand1 = js_types.Boolean(operand1)
        operand2 = js_types.Boolean(operand2)

        result = js_types.Boolean('false')
        if operator == "&&":
            result.value = (operand1.value and operand2.value)
        elif operator == "||":
            result.value = (operand1.value or operand2.value)

        return result
    else:
        raise Exception(f"Invalid comparison operator '{operator}'")

# mutation_symbols: ["!", "+", "-"]
def mutation(operand, operator):
    if operator == "!": # logical negation
        operand = js_types.Boolean(operand)
        operand.value = not operand.value
        return operand
    elif operator == "+": # convert to Number 
        operand = js_types.Number(operand)
        return operand
    elif operator == "-": # numerical negation
        operand = js_types.Number(operand)
        return arithmetic(js_types.Number("-1"), operand, "*")
    else:
        raise Exception(f"Invalid mutation operator '{operator}'")

# assignment_symbols: ["=", "+=", "-=", "*=", "/=", "%=", "**="] 
def assignment(variable, value, operator):
    if operator == "=":
        variable.value = value
        return value
    elif operator in ["+=", "-=", "*=", "/=", "%=", "**="]:
        result = arithmetic(variable.value, value, operator[:-1])
        variable.value = result 
        return result
    else:
        raise Exception(f"Invalid assignment operator '{operator}'")
  
# increment_symbols: ["++", "--"]
def increment(variable, operator, is_right = True):
    variable.value = js_types.Number(variable.value) # must convert to a number
    pre_value = variable.value

    if operator == "++":
        variable.value = arithmetic(variable.value, js_types.Number("1"), "+")
    elif operator == "--":
        variable.value = arithmetic(variable.value, js_types.Number("1"), "-")
    else:
        raise Exception(f"Invalid increment operator '{operator}'")
    
    if is_right: # x++
        return pre_value
    else: # ++x
        return variable.value