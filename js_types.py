class Primitive: # base for all other types
    def __init__(self, input_str):
        self.value = input_str

    def __repr__(self):
        return self.value

class String(Primitive):
    def __repr__(self):
        return f"'{self.value}'"

class Number(Primitive):
    pass

class Boolean(Primitive):
    def __init__(self, input_str):
        pass

class Undefined(Primitive):
    def __init__(self, input_str):
        pass

class Null(Primitive):
    def __init__(self, input_str):
        pass