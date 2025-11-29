def displayInfoMessage():
    print(
"""
CSC1019 Project: JavaScript Simulator
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
This program evaluates basic JavaScript code.
Only the following structures are supported:
    (1) Declarations (let x;)
    (2) Assignments (z = 3;)
    (3) Expressions (b - 4 / c)
On each line marked with '>>', you can enter
a single line of JavaScript code, and the 
output will be displayed on the next line.

If an entered line is invalid or unsupported,
an error message will be displayed. You can
enter 'quit' to end the program.
            
These are some examples:
>> let x = 5;
<< 5
>> 2 * (x + 1)
<< 12
>> const y = x - 1;
<< 4
>> x === y
<< false
>> quit
_____________________________________________"""
    )