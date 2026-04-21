def get_precedence(op):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    return precedence.get(op, 0)

def infix_to_postfix(expression):
    stack = []
    output = []
    
    for char in expression:
        if char.isalnum(): # Operand
            output.append(char)
        elif char == '(': # Left Parenthesis
            stack.append(char)
        elif char == ')': # Right Parenthesis
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop() # Remove '('
        else: # Operator
            while stack and get_precedence(char) <= get_precedence(stack[-1]):
                output.append(stack.pop())
            stack.append(char)
            
    while stack:
        output.append(stack.pop())
        
    return "".join(output)

def infix_to_prefix(expression):
    # Step 1 & 2: Reverse and swap parentheses
    reversed_expr = ""
    for char in expression[::-1]:
        if char == '(':
            reversed_expr += ')'
        elif char == ')':
            reversed_expr += '('
        else:
            reversed_expr += char
            
    # Step 3: Apply modified postfix algorithm
    stack = []
    output = []
    
    for char in reversed_expr:
        if char.isalnum():
            output.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            # Note the strictly less than `<` here instead of `<=` for prefix rules
            while stack and get_precedence(char) < get_precedence(stack[-1]):
                output.append(stack.pop())
            stack.append(char)
            
    while stack:
        output.append(stack.pop())
        
    # Step 4: Reverse the output to get prefix
    return "".join(output[::-1])

# Driver Code
if __name__ == '__main__':
    infix_expr = "A+B*C-D/E"
    
    print(f"{'Input Infix Expression':<25}: {infix_expr}")
    print("-" * 45)
    
    postfix_expr = infix_to_postfix(infix_expr)
    print(f"{'Postfix Notation':<25}: {postfix_expr}")
    
    prefix_expr = infix_to_prefix(infix_expr)
    print(f"{'Prefix Notation':<25}: {prefix_expr}")