"""
File purpose: organize code that helps
the user with input/output (unrelated
to the technical parsing functions).
File was made to keep main.py clean and 
since the welcome function doesn't belong
anywhere else.
"""

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
On each line marked with '[Input JS] >>', you 
can enter a single line of JavaScript code,
and the output will be displayed on the next line.

If an entered line is invalid or unsupported,
an error message will be displayed. You can
enter 'quit' to end the program. Here is a demo video:
https://drive.google.com/file/d/1ilbcIOeH3gbWDcmLmxzCOoGT57QFZIlD/view?usp=sharing
            
These are some examples:
[Input JS] >> let x = 5;
[ Output ] << 5
[Input JS] >> 2 * (x + 1)
[ Output ] << 12
[Input JS] >> const y = x - 1;
[ Output ] << 4
[Input JS] >> x === y
[ Output ] << false
[Input JS] >> quit

^ Read Me ^
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾"""
    )