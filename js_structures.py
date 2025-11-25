class Error(Exception):
    pass

class Expression:
    def __init__(self, expr_str):
        self.value = expr_str

class Assignment:
    def __init__(self, var_name, expr_str):
        self.var_name = var_name
        self.var_value = Expression(expr_str)

class Declaration:
    def __init__(self, keyword, var_name, expr_str):
        self.keyword = keyword
        self.assignment = Assignment(var_name, expr_str)