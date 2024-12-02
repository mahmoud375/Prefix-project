import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from pythonds.basic.stack import Stack
import math

# Function to format the expression by adding spaces
def format_expression(expression):
    formatted = ""
    for char in expression:
        if char in "+-*/%^()":
            formatted += f" {char} "
        else:
            formatted += char
    return " ".join(formatted.split())  # Remove any extra spaces

# Function to convert infix to postfix
def infix2postfix(infixInput):
    priority = {"^": 4, "*": 3, "/": 3, "-": 2, "+": 2, "%": 2, "(": 1}
    operation = Stack()
    postfix = []
    tokenlist = infixInput.split()
    
    for token in tokenlist:
        if token.isalpha() or token.isdigit():
            postfix.append(token)
        elif token == "(":
            operation.push(token)
        elif token == ")":
            while not operation.isEmpty() and operation.peek() != "(":
                postfix.append(operation.pop())
            if not operation.isEmpty():
                operation.pop()
            else:
                return "Error: Unbalanced parentheses"
        else:
            while not operation.isEmpty() and priority.get(operation.peek(), 0) >= priority[token]:
                postfix.append(operation.pop())
            operation.push(token)
    
    while not operation.isEmpty():
        top = operation.pop()
        if top in "()":
            return "Error: Unbalanced parentheses"
        postfix.append(top)
    
    return " ".join(postfix)

# Reverse the expression for prefix conversion
def revExp(exp):
    exp = exp.split()[::-1]
    for i in range(len(exp)):
        if exp[i] == "(":
            exp[i] = ")"
        elif exp[i] == ")":
            exp[i] = "("
    return exp  

# Perform mathematical operations
def doMath(operator, operand1, operand2=None):
    try:
        operand1 = float(operand1)
        if operand2 is not None:
            operand2 = float(operand2)
    except ValueError:
        return "math error"
    
    if operator == "+":
        return operand1 + operand2
    elif operator == "-":
        return operand1 - operand2
    elif operator == "*":
        return operand1 * operand2
    elif operator == "/" and operand2 != 0:
        return operand1 / operand2
    elif operator == "%":
        return operand1 % operand2
    elif operator == "^":
        return operand1 ** operand2
    elif operator == "sin":
        return math.sin(math.radians(operand1))
    elif operator == "cos":
        return math.cos(math.radians(operand1))
    elif operator == "sqrt":
        return math.sqrt(operand1)
    else:
        return "math error"

# Evaluate prefix expression
def mathEvaluation(expr, var_values):
    opStack = Stack()
    tokenlist = expr.split()
    
    for token in reversed(tokenlist):
        if token.replace('.', '', 1).isdigit():
            opStack.push(float(token))
        elif token.isalpha():
            if token in var_values:
                opStack.push(float(var_values[token]))
            else:
                return f"Error: Variable {token} is not assigned a value."
        else:
            if token in ["sin", "cos", "sqrt"]:
                if opStack.size() < 1:
                    return "Error: Too few operands for operation"
                operand1 = opStack.pop()
                result = doMath(token, operand1)
            else:
                if opStack.size() < 2:
                    return "Error: Too few operands"
                operand1 = opStack.pop()
                operand2 = opStack.pop()
                result = doMath(token, operand1, operand2)
            
            if result == "math error":
                return "Error during calculation"
            opStack.push(result)
    
    if opStack.size() == 1:
        return opStack.pop()
    else:
        return "Error: Invalid expression"

# Validate parentheses in the expression
def validate_expression(expr):
    balance = 0
    for char in expr:
        if char == "(":
            balance += 1
        elif char == ")":
            balance -= 1
        if balance < 0:
            return False
    return balance == 0

# Evaluate expression button action
def evaluate_expression():
    infix = entry.get()
    infix = format_expression(infix)
    if not validate_expression(infix):
        messagebox.showerror("Error", "Unbalanced parentheses")
        return
    
    rev_input = revExp(infix)
    postfix = infix2postfix(" ".join(rev_input))
    
    if "Error" in postfix:
        messagebox.showerror("Error", postfix)
        return
    
    prefix = " ".join(revExp(postfix))
    prefix_label.config(text=f"Prefix: {prefix}")
    
    variables = set(filter(str.isalpha, infix))
    var_values = {}
    
    for var in variables:
        value = simpledialog.askstring("Variable Value", f"Enter value for {var}:")
        if value is None:
            return
        try:
            var_values[var] = float(value)
        except ValueError:
            messagebox.showerror("Error", f"Invalid value for {var}. Please enter a number.")
            return
    
    result = mathEvaluation(prefix, var_values)
    result_label.config(text=f"Result: {result}")

# Reset all fields
def reset_fields():
    """Reset all input and output fields."""
    entry.delete(0, tk.END)
    prefix_label.config(text="Prefix: ")
    result_label.config(text="Result: ")

# GUI Setup
root = tk.Tk()
root.title("Infix to Prefix Converter and Evaluator")
root.geometry("700x500")
root.configure(bg="#1c2833")

style = ttk.Style()
style.configure("TButton", font=("Arial", 14), padding=10, background="#3498db", foreground="white")
style.configure("TLabel", font=("Arial", 14), background="#1c2833", foreground="white")
style.configure("TEntry", font=("Arial", 16))

frame = ttk.Frame(root, padding=30, style="TFrame")
frame.pack(expand=True)

ttk.Label(frame, text="Enter Infix Expression:").grid(row=0, column=0, pady=10, sticky="w")
entry = ttk.Entry(frame, width=50)
entry.grid(row=0, column=1, pady=10, padx=10)

evaluate_btn = ttk.Button(frame, text="Evaluate", command=evaluate_expression)
evaluate_btn.grid(row=1, column=0, pady=20)

reset_btn = ttk.Button(frame, text="Reset", command=reset_fields)
reset_btn.grid(row=1, column=1, pady=20)

prefix_label = ttk.Label(frame, text="Prefix: ")
prefix_label.grid(row=2, column=0, columnspan=2, pady=10)

result_label = ttk.Label(frame, text="Result: ")
result_label.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
