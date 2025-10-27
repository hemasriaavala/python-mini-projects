# safe_calculator.py
# Simple calculator with a safe expression evaluator using ast

import ast
import operator as op

# allowed operators mapping
ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: lambda x: +x,
    ast.USub: lambda x: -x,
}

def safe_eval(expr: str):
    """
    Evaluate a math expression safely using ast.
    Supports +, -, *, /, //, %, ** and parentheses.
    Raises ValueError for invalid expressions.
    """
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Num):  # Python <3.8
            return node.n
        if hasattr(ast, "Constant") and isinstance(node, ast.Constant):  # Python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Unsupported constant type")
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in ALLOWED_OPERATORS:
                return ALLOWED_OPERATORS[op_type](left, right)
            raise ValueError(f"Unsupported binary operator: {op_type}")
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in ALLOWED_OPERATORS:
                return ALLOWED_OPERATORS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type}")
        raise ValueError(f"Unsupported expression: {type(node)}")

    parsed = ast.parse(expr, mode='eval')
    return _eval(parsed)

def menu():
    print("Simple Python Calculator (type 'quit' to exit)")
    print("You can enter expressions like: 2+3*4, (5-2)**3, 10//3, 10%3")
    while True:
        expr = input("Enter expression: ").strip()
        if expr.lower() in ('quit', 'exit'):
            print("Goodbye!")
            break
        if not expr:
            continue
        try:
            result = safe_eval(expr)
            print("= ", result)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    menu()
