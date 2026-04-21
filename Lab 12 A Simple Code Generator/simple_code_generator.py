def generate_assembly(tac_list):
    op_map = {
        '+': 'ADD',
        '-': 'SUB',
        '*': 'MUL',
        '/': 'DIV'
    }
    
    assembly_code = []
    reg_index = 0 # To simulate utilizing different registers if needed
    
    for tac in tac_list:
        # Splitting the assignment part and expression part
        if '=' not in tac:
            continue
            
        left, right = tac.split('=')
        res = left.strip()
        expr = right.strip().split()
        
        reg = f"R{reg_index}"
        
        if len(expr) == 3: # Format: arg1 op arg2
            arg1, op, arg2 = expr
            assembly_code.append(f"MOV {arg1}, {reg}")
            assembly_code.append(f"{op_map[op]} {arg2}, {reg}")
            assembly_code.append(f"MOV {reg}, {res}")
            
        elif len(expr) == 1: # Format: arg1 (Simple assignment)
            arg1 = expr[0]
            assembly_code.append(f"MOV {arg1}, {reg}")
            assembly_code.append(f"MOV {reg}, {res}")
            
        # Toggle register for variation (Optional basic register allocation)
        reg_index = (reg_index + 1) % 2 
        
    return assembly_code

# Driver Code
if __name__ == '__main__':
    # 3-Address Code: w = a - b, x = a - c, y = x + w
    tac_input = [
        "t1 = a - b",
        "t2 = c * d",
        "t3 = t1 + t2"
    ]
    
    print("Intermediate Code (3AC):")
    for code in tac_input:
        print(code)
        
    print("\nGenerated Target Assembly Code:")
    print("-" * 30)
    
    assembly_instructions = generate_assembly(tac_input)
    for instruction in assembly_instructions:
        print(instruction)