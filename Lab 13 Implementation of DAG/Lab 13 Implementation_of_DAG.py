class DAGNode:
    def __init__(self, id, value, left=None, right=None):
        self.id = id
        self.value = value
        self.left = left
        self.right = right
        self.labels = [] # Variables assigned to this node's value

class DAG:
    def __init__(self):
        self.nodes = []
        self.node_counter = 1
        
    def find_node_by_value(self, value):
        # Mostly for leaf nodes
        for node in self.nodes:
            if node.value == value and node.left is None and node.right is None:
                return node
            # Also check if it's a label for an existing internal node
            if value in node.labels:
                return node
        return None

    def find_internal_node(self, op, left_node, right_node):
        for node in self.nodes:
            if node.value == op and node.left == left_node and node.right == right_node:
                return node
        return None

    def add_node(self, res, arg1, op=None, arg2=None):
        # Handle Arg1
        left_node = self.find_node_by_value(arg1)
        if not left_node:
            left_node = DAGNode(self.node_counter, arg1)
            self.node_counter += 1
            self.nodes.append(left_node)
            
        if not op and not arg2: # Simple assignment (e.g., x = y)
            left_node.labels.append(res)
            return

        # Handle Arg2
        right_node = self.find_node_by_value(arg2)
        if not right_node:
            right_node = DAGNode(self.node_counter, arg2)
            self.node_counter += 1
            self.nodes.append(right_node)

        # Check for Common Subexpression
        internal_node = self.find_internal_node(op, left_node, right_node)
        if internal_node:
             # Eliminate redundancy by attaching the label to existing node
            if res not in internal_node.labels:
                internal_node.labels.append(res)
        else:
            # Create new internal node
            internal_node = DAGNode(self.node_counter, op, left_node, right_node)
            internal_node.labels.append(res)
            self.node_counter += 1
            self.nodes.append(internal_node)

    def display(self):
        print(f"{'Node ID':<10} | {'Value':<8} | {'Left Child':<12} | {'Right Child':<12} | {'Labels (Vars)'}")
        print("-" * 75)
        for node in self.nodes:
            left_id = node.left.id if node.left else "-"
            right_id = node.right.id if node.right else "-"
            labels = ", ".join(node.labels) if node.labels else "-"
            print(f"{node.id:<10} | {node.value:<8} | {left_id:<12} | {right_id:<12} | {labels}")

# Driver Code
if __name__ == '__main__':
    # Example to show Common Subexpression Elimination
    # Original math: a + a * (b - c) + (b - c) * d
    tac_input = [
        "t1 = b - c",
        "t2 = a * t1",
        "t3 = a + t2",
        "t4 = b - c",   # Common Subexpression!
        "t5 = t4 * d",
        "t6 = t3 + t5"
    ]
    
    print("Input 3AC Block:")
    for code in tac_input:
        print(code)
    print("\nConstructing DAG...\n")
    
    dag = DAG()
    for tac in tac_input:
        # Parsing "res = arg1 op arg2"
        left, right = tac.split('=')
        res = left.strip()
        expr = right.strip().split()
        
        if len(expr) == 3:
            arg1, op, arg2 = expr
            dag.add_node(res, arg1, op, arg2)
        elif len(expr) == 1:
            dag.add_node(res, expr[0])
            
    dag.display()