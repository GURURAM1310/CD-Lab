import re

def parse_3ac(code_list):
    parsed = []
    # Regex to match patterns like "t1 = a + b" or "t1 = - c" or "t1 = a"
    pattern = re.compile(r'([a-zA-Z0-9_]+)\s*=\s*([a-zA-Z0-9_]+)?\s*([+\-*/])?\s*([a-zA-Z0-9_]+)?')
    
    for line in code_list:
        match = pattern.match(line.strip())
        if match:
            res = match.group(1)
            arg1 = match.group(2) if match.group(2) else ""
            op = match.group(3) if match.group(3) else ""
            arg2 = match.group(4) if match.group(4) else ""
            parsed.append({'res': res, 'arg1': arg1, 'op': op, 'arg2': arg2})
    return parsed

def generate_quadruples(parsed_code):
    print("\nQUADRUPLES:")
    print(f"{'Index':<6} | {'Operator':<8} | {'Arg1':<6} | {'Arg2':<6} | {'Result'}")
    print("-" * 45)
    for i, line in enumerate(parsed_code):
        print(f"{i:<6} | {line['op']:<8} | {line['arg1']:<6} | {line['arg2']:<6} | {line['res']}")

def generate_triples(parsed_code):
    print("\nTRIPLES:")
    print(f"{'Index':<6} | {'Operator':<8} | {'Arg1':<6} | {'Arg2'}")
    print("-" * 35)
    
    # Dictionary to keep track of which temporary variable maps to which index
    temp_map = {}
    triples = []
    
    for i, line in enumerate(parsed_code):
        arg1 = f"({temp_map[line['arg1']]})" if line['arg1'] in temp_map else line['arg1']
        arg2 = f"({temp_map[line['arg2']]})" if line['arg2'] in temp_map else line['arg2']
        
        triples.append((line['op'], arg1, arg2))
        temp_map[line['res']] = i
        
        print(f"{i:<6} | {line['op']:<8} | {arg1:<6} | {arg2}")
        
    return triples

def generate_indirect_triples(triples, start_address=100):
    print("\nINDIRECT TRIPLES:")
    print(f"{'Statement':<10} | {'Pointer (Triple Index)'}")
    print("-" * 35)
    for i in range(len(triples)):
        print(f"{start_address + i:<10} | ({i})")

# Driver Code
if __name__ == '__main__':
    # Sequence of 3-address codes for the expression: a + b * c - d
    three_address_code = [
        "t1 = b * c",
        "t2 = a + t1",
        "t3 = t2 - d"
    ]
    
    print("Input Three-Address Code:")
    for code in three_address_code:
        print(code)
        
    parsed = parse_3ac(three_address_code)
    
    generate_quadruples(parsed)
    triples = generate_triples(parsed)
    generate_indirect_triples(triples)