import parsing
import user_interface

"""
File purpose: main file that brings all
the other modules together. It handles
the main loop for user input and output.
"""

def main():    
    user_interface.displayInfoMessage()
    window = {} # mimics the window object (in browser JS)
    
    while True:
        inputted_js = input("[Input JS] >> ")

        if inputted_js == "quit":
            break
        else:
            eval_value = parsing.parse(inputted_js, window)
            print("[ Output ] <<", eval_value)

if __name__ == "__main__":
    main()