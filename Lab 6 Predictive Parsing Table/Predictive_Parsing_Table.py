def construct_parsing_table(grammar, first, follow, terminals, non_terminals):
    # Initialize empty parsing table
    # table[Non-Terminal][Terminal]
    table = {nt: {t: "" for t in terminals + ['$']} for nt in non_terminals}
    
    for nt in non_terminals:
        for rule in grammar[nt]:
            
            # Find FIRST(RHS)
            first_of_rhs = set()
            if rule == 'ε':
                first_of_rhs.add('ε')
            else:
                first_symbol = rule[0]
                if not first_symbol.isupper() and first_symbol != 'ε': 
                    # If it's a terminal
                    first_of_rhs.add(first_symbol)
                else:
                    # If it's a non-terminal, add its FIRST set
                    first_of_rhs.update(first[first_symbol])
            
            # Apply Rule 1: Add to Table[A][a] for all 'a' in FIRST(RHS)
            for terminal in first_of_rhs:
                if terminal != 'ε':
                    # Check for LL(1) conflict
                    if table[nt][terminal] != "":
                        print(f"Grammar is not LL(1). Conflict at Table[{nt}][{terminal}]")
                    table[nt][terminal] = f"{nt} -> {rule}"
            
            # Apply Rule 2 & 3: If 'ε' in FIRST(RHS), add to Table[A][b] for all 'b' in FOLLOW(A)
            if 'ε' in first_of_rhs:
                for terminal in follow[nt]:
                    table[nt][terminal] = f"{nt} -> {rule}"
                    
    return table

def print_table(table, terminals, non_terminals):
    headers = terminals + ['$']
    
    # Print Header row
    print(f"{'NT':<5} | " + " | ".join([f"{h:<10}" for h in headers]))
    print("-" * 75)
    
    # Print Table content
    for nt in non_terminals:
        row = f"{nt:<5} | "
        for t in headers:
            row += f"{table[nt][t]:<10} | "
        print(row)

# Driver Code
if __name__ == '__main__':
    # Standard expression grammar without Left Recursion
    # E  -> TE'
    # E' -> +TE' | ε
    # T  -> FT'
    # T' -> *FT' | ε
    # F  -> (E) | i
    
    grammar = {
        'E':  ['TE\''],
        'E\'': ['+TE\'', 'ε'],
        'T':  ['FT\''],
        'T\'': ['*FT\'', 'ε'],
        'F':  ['(E)', 'i']
    }
    
    non_terminals = ['E', 'E\'', 'T', 'T\'', 'F']
    terminals = ['+', '*', '(', ')', 'i']
    
    # Pre-computed FIRST sets
    first = {
        'E':  {'(', 'i'},
        'E\'': {'+', 'ε'},
        'T':  {'(', 'i'},
        'T\'': {'*', 'ε'},
        'F':  {'(', 'i'}
    }
    
    # Pre-computed FOLLOW sets
    follow = {
        'E':  {')', '$'},
        'E\'': {')', '$'},
        'T':  {'+', ')', '$'},
        'T\'': {'+', ')', '$'},
        'F':  {'*', '+', ')', '$'}
    }
    
    print("Constructing LL(1) Parsing Table...\n")
    parsing_table = construct_parsing_table(grammar, first, follow, terminals, non_terminals)
    
    print_table(parsing_table, terminals, non_terminals)