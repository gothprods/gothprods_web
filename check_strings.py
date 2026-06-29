import sys

def check(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    in_string = False
    string_char = ''
    string_line = 0
    escape = False
    
    line_num = 1
    for char in content:
        if char == '\n':
            line_num += 1
            if in_string and string_char != '`' and not escape:
                print(f"Unclosed string {string_char} opened at line {string_line} ended at newline at line {line_num-1}")
                in_string = False
        
        if not in_string:
            if char in "'\"`":
                in_string = True
                string_char = char
                string_line = line_num
                escape = False
        else:
            if escape:
                escape = False
            elif char == '\\':
                escape = True
            elif char == string_char:
                in_string = False
                
    if in_string:
        print(f"File ended with unclosed string {string_char} opened at line {string_line}")
    else:
        print("All strings are closed!")

check('script_check.js')
