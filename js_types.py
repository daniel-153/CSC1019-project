class Primitive: # base for all other types, used to centralize some features
    def __init__(self, input_obj):
        self.value = input_obj
    
    def __str__(self):
        return str(self.value)
    
    class ConstructorError(Exception):
        def __init__(self, attempted_type, input_obj, failure):
            type_name = attempted_type.__class__.__name__

            if failure == "invalid_literal":
                error_msg = f"<{input_obj}> is not a valid JS {type_name} literal"
            elif failure == "invalid_type":
                error_msg = f"Cannot directly construct JS {type_name} from '{input_obj}' typeof '{type(input_obj)}'"
            else:
                error_msg = "Unknown construtor error"
            
            super().__init__(error_msg)

class String(Primitive):
    def __init__(self, input_obj): # Direct construction 
        if isinstance(input_obj, str):
            if (
                input_obj[0] in ["'", '"'] and
                len(input_obj) >= 2 and
                input_obj[0] == input_obj[-1] and
                input_obj.count(input_obj[0]) == 2
            ):
                self.value = input_obj[1:-1]
            else:
                raise self.ConstructorError(self, input_obj, "invalid_literal")
        elif isinstance(input_obj, Primitive):
            self.value = str(input_obj) 
        else:
            raise self.ConstructorError(self, input_obj, "invalid_type")

class Number(Primitive):
    def __init__(self, input_obj):
        if isinstance(input_obj, str): # construction by literal 
            if input_obj == "NaN":
                self.value = "NaN"
            else:
                attempted_build = Number(String(f"'{input_obj}'"))
                
                if attempted_build.value == "NaN":
                    raise self.ConstructorError(self, input_obj, "invalid_literal")
                else:
                    self.value = attempted_build.value
        elif isinstance(input_obj, Primitive): # conversion from another JS type    
            if isinstance(input_obj, String): 
                str_value = input_obj.value

                if ( # positive or negative int
                    str_value.isdigit() or 
                    str_value[0] == '-' and str_value[1:].isdigit()
                ):
                    self.value = int(str_value)
                elif ( # positive or negative decimal
                    str_value.count(".") == 1 and
                    (
                        str_value.replace(".", "").isdigit() or 
                        str_value[0] == '-' and str_value[1:].replace(".", "").isdigit()
                    ) and
                    str_value[0] != "." and
                    str_value[-1] != "."
                ):
                    self.value = float(str_value)
                else:
                    self.value = "NaN"
            elif isinstance(input_obj, Boolean): 
                if input_obj.value:
                    self.value = 1
                else:
                    self.value = 0
            elif isinstance(input_obj, Number):
                self.value = input_obj.value
            else: # can't convert anything else to a number
                self.value = "NaN"
        else:
            raise self.ConstructorError(self, input_obj, "invalid_type")

class Boolean(Primitive):
    def __init__(self, input_obj):
        if isinstance(input_obj, str): # direct construction
            if input_obj == "true":
                self.value = True
            elif input_obj == "false":
                self.value = False
            else:
                raise self.ConstructorError(self, input_obj, "invalid_literal")
        elif isinstance(input_obj, Primitive): # conversion from another JS type
            if isinstance(input_obj, Number):
                if (
                    input_obj.value == 0 or
                    input_obj.value == "NaN"
                ):
                    self.value = False
                else:
                    self.value = True
            elif isinstance(input_obj, String):
                if len(input_obj.value) == 0:
                    self.value = False
                else:
                    self.value = True
            elif isinstance(input_obj, Boolean): # no change
                self.value = input_obj.value
            else:
                self.value = False
        else:
            raise self.ConstructorError(self, input_obj, "invalid_type")

    def __str__(self):
        return str(self.value).lower()

class Undefined(Primitive):
    def __init__(self, input_obj):
        if isinstance(input_obj, str):
            if input_obj == "undefined":
                self.value = input_obj
            else:
                raise self.ConstructorError(self, input_obj, "invalid_literal")
        else:
            raise self.ConstructorError(self, input_obj, "invalid_type")

class Null(Primitive):
    def __init__(self, input_obj):
        if isinstance(input_obj, str):
            if input_obj == "null":
                self.value = input_obj
            else:
                raise self.ConstructorError(self, input_obj, "invalid_literal")
        else:
            raise self.ConstructorError(self, input_obj, "invalid_type")