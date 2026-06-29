import sys

def check(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    stack = []
    line_num = 1
    for i, char in enumerate(content):
        if char == '\n':
            line_num += 1
        elif char in '{[(': 
            stack.append((char, line_num))
        elif char in '}])':
            if not stack:
                print(f"Extra closing {char} at line {line_num}")
                return
            top, top_line = stack.pop()
            if (top == '{' and char != '}') or \
               (top == '[' and char != ']') or \
               (top == '(' and char != ')'):
                print(f"Mismatch: opened {top} at line {top_line}, tried to close with {char} at line {line_num}")
                return
    
    if stack:
        for char, line in stack:
            print(f"Unclosed {char} opened at line {line}")
    else:
        print("All braces match perfectly!")

check('script_check.js')
