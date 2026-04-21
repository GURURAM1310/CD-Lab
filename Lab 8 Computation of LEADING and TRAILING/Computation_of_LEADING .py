def shift_reduce_parser(grammar, input_string):
    stack = ""
    input_buffer = input_string + "$"
    action = ""
    
    # Print header
    print(f"{'STACK':<15} | {'INPUT BUFFER':<15} | {'ACTION'}")
    print("-" * 50)
    
    while True:
        # Print current state
        print(f"{stack + '$':<15} | {input_buffer:<15} | {action}")
        
        # Check for Acceptance condition
        if stack == list(grammar.values())[0] and input_buffer == "$":
            print("-" * 50)
            print("Result: String Accepted!")
            break
            
        # Flag to check if reduction happened in this iteration
        reduced = False
        
        # Try to Reduce
        for rhs, lhs in grammar.items():
            if stack.endswith(rhs):
                stack = stack[:-len(rhs)] + lhs
                action = f"Reduce {lhs} -> {rhs}"
                reduced = True
                break
        
        # If no reduction happened, try to Shift
        if not reduced:
            if input_buffer != "$":
                stack += input_buffer[0]
                input_buffer = input_buffer[1:]
                action = f"Shift '{stack[-1]}'"
            else:
                print("-" * 50)
                print("Result: String Rejected! (Syntax Error)")
                break

# Driver Code
if __name__ == '__main__':
    # Define Grammar: E -> E+E | E*E | i
    # Stored as RHS: LHS for easy reduction lookup
    grammar_rules = {
        "i": "E",
        "E+E": "E",
        "E*E": "E"
    }
    
    test_string = "i+i*i"
    print(f"Grammar Rules: E -> E+E | E*E | i")
    print(f"Input String: {test_string}\n")
    
    shift_reduce_parser(grammar_rules, test_string)