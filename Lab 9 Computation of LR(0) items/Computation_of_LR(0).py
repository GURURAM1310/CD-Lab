def closure(items, grammar):
    closure_set = set(items)
    changed = True
    
    while changed:
        changed = False
        new_items = set()
        
        for lhs, rhs, dot_pos in closure_set:
            # If dot is not at the end of the RHS
            if dot_pos < len(rhs):
                next_symbol = rhs[dot_pos]
                # If the symbol right of the dot is a non-terminal
                if next_symbol in grammar:
                    for prod in grammar[next_symbol]:
                        new_item = (next_symbol, tuple(prod), 0)
                        if new_item not in closure_set and new_item not in new_items:
                            new_items.add(new_item)
                            
        if new_items:
            closure_set.update(new_items)
            changed = True
            
    return closure_set

def goto(items, symbol, grammar):
    goto_set = set()
    for lhs, rhs, dot_pos in items:
        if dot_pos < len(rhs) and rhs[dot_pos] == symbol:
            # Move the dot one position to the right
            goto_set.add((lhs, rhs, dot_pos + 1))
    return closure(goto_set, grammar)

def format_item(item):
    lhs, rhs, dot_pos = item
    rhs_list = list(rhs)
    rhs_list.insert(dot_pos, '.')
    return f"{lhs} -> {''.join(rhs_list)}"

def compute_lr0(grammar, start_symbol):
    # 1. Augment grammar
    aug_start = start_symbol + "'"
    grammar[aug_start] = [[start_symbol]]
    
    # Extract all symbols (terminals and non-terminals)
    symbols = set(grammar.keys())
    for rules in grammar.values():
        for rule in rules:
            symbols.update(rule)
            
    # 2. Initialize with closure of augmented start production
    initial_item = (aug_start, tuple([start_symbol]), 0)
    initial_state = frozenset(closure({initial_item}, grammar))
    
    states = [initial_state]
    
    # 3. Compute all states using goto
    added = True
    while added:
        added = False
        for state in states:
            for symbol in symbols:
                next_state = frozenset(goto(state, symbol, grammar))
                if next_state and next_state not in states:
                    states.append(next_state)
                    added = True
                    
    return states

# Driver Code
if __name__ == '__main__':
    # Grammar: E -> E+T | T, T -> id
    # Represented as lists of characters/symbols
    grammar = {
        'E': [['E', '+', 'T'], ['T']],
        'T': [['i', 'd']]
    }
    
    start_symbol = 'E'
    print("Given Grammar:")
    for nt, rules in grammar.items():
        print(f"{nt} -> {' | '.join([''.join(r) for r in rules])}")
    print("-" * 30)
    
    states = compute_lr0(grammar, start_symbol)
    
    print("LR(0) Item Sets (Canonical Collection):\n")
    for i, state in enumerate(states):
        print(f"State I{i}:")
        for item in sorted(state):
            print(f"  {format_item(item)}")
        print()