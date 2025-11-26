import parsing

def main():    
    window = {} # Represents the window object (in browser JS)
    
    while True:
        inputted_js = input('Enter a line of JavaScript code:')

        if inputted_js == 'quit':
            break
        else:
            eval_value = parsing.parse(inputted_js, window)
            print(eval_value)

if __name__ == '__main__':
    main()