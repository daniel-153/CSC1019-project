class Arithmetic:
    symbols = ["+", "-", "*", "/", "%", "**"]
    
    def __init__(self, operand1, operand2, operator):
        pass

class Assignment:
    # symbols need to include the special assigments like += "plus equals"
    symbols = ["="].append([(operator + "=") for operator in Arithmetic.symbols])

    def __init__(self, operand1, operand2):
        pass

class Comparison:
    symbols = ["==", "!=", "===", "!==", ">", "<", ">=", "<="]

    def __init__(self, operand1, operand2):
        pass

class Logic:
    symbols = ["&&", "||"]

    def __init__(self, operand1, operand2):
        pass

class Mutation:
    symbols = ["!", "++", "--", "+", "-"]

    def __init__(self, operand):
        pass