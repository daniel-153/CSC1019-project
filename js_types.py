class Primitive: # base for all other types, used to centralize str()
    def __init__(self, input_obj):
        self.value = input_obj
    
    def __str__(self):
        return str(self.value)

class String(Primitive):
    def __init__(self, input_obj): # Direct construction (no restrictions)
        self.value = str(input_obj)

    def __repr__(self):
        return f"'{self.value}'"

class Number(Primitive):
    def __init__(self, input_obj):
        if isinstance(input_obj, str): # direct construction 
            # this block cannot be passed unless the string can be made into a JS number
            try:
                float(input_obj)
            except:
                raise Exception(f"Cannot directly construct JS Number from '{input_obj}'")
                
            input_obj = String(input_obj) # if valid, the handling is the same as a JS String    
                
        # conversion from another JS type
        if isinstance(input_obj, String): # number from String
            str_value = str(input_obj)

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
            else: # NaN otherwise
                self.value = "NaN"
        elif isinstance(input_obj, Boolean): # number from Boolean
            if input_obj.value:
                self.value = 1
            else:
                self.value = 0
        elif isinstance(input_obj, Number): # no change
            self.value = input_obj.value
        else: # can't convert anything else to a number
            self.value = "NaN"

class Boolean(Primitive):
    def __init__(self, input_obj):
        if isinstance(input_obj, str): # direct construction
            if input_obj == "true":
                self.value = True
            elif input_obj == "false":
                self.value = False
            else:
                raise Exception(f"Cannot directly construct JS Boolean from '{input_obj}'")
        else: # conversion from another JS type
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

class Undefined(Primitive):
    def __init__(self, input_obj):
        if ( # only direct construction allowed (can't convert anything else to undefined)
            isinstance(input_obj, str) and 
            input_obj == 'undefined'
        ):
            self.value = input_obj
        else:
            raise Exception(f"Cannot directly construct JS Undefined from '{input_obj}'")

class Null(Primitive):
    def __init__(self, input_obj):
        if ( # only direct construction allowed (can't convert anything else to null)
            isinstance(input_obj, str) and 
            input_obj == 'null'
        ):
            self.value = input_obj
        else:
            raise Exception(f"Cannot directly construct JS Null from '{input_obj}'")