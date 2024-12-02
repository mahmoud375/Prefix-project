import tkinter as tk
from tkinter import messagebox, simpledialog
from pythonds.basic.stack import Stack

def infix2postfix(infixInput):
    priority = {"^": 4, "*": 3, "/": 3, "-": 2, "+": 2, "(": 1}
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

def revExp(exp):
    exp = exp.split()[::-1]
    for i in range(len(exp)):
        if exp[i] == "(":
            exp[i] = ")"
        elif exp[i] == ")":
            exp[i] = "("
    return exp  

def doMath(operator, operand1, operand2):
    try:
        operand1 = float(operand1)
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
    elif operator == "%" and operand2 != 0:
        return operand1 % operand2
    elif operator == "^":
        return operand1 ** operand2
    else:
        return "math error"

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
            if opStack.size() < 2:
                return "Can't evaluate, too few operands"
            operand1 = opStack.pop()
            operand2 = opStack.pop()
            result = doMath(token, operand1, operand2)
            if result == "math error":
                return "Error during calculation"
            opStack.push(result)
    
    if opStack.size() == 1:
        return opStack.pop()
    else:
        return "Can't evaluate, invalid expression"

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

# واجهة المستخدم
def evaluate_expression():
    infix = entry.get()
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
    
    # جمع القيم للمتغيرات
    variables = set(filter(str.isalpha, infix))
    var_values = {}
    
    for var in variables:
        value = tk.simpledialog.askstring("Variable Value", f"Enter value for {var}:")
        if value is None:
            return
        try:
            var_values[var] = float(value)
        except ValueError:
            messagebox.showerror("Error", f"Invalid value for {var}. Please enter a number.")
            return
    
    result = mathEvaluation(prefix, var_values)
    result_label.config(text=f"Result: {result}")

# إنشاء نافذة
root = tk.Tk()
root.title("Infix to Prefix Converter and Evaluator")

# عناصر الواجهة
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="Enter Infix Expression:").grid(row=0, column=0, pady=5)
entry = tk.Entry(frame, width=30)
entry.grid(row=0, column=1, pady=5)

evaluate_btn = tk.Button(frame, text="Evaluate", command=evaluate_expression)
evaluate_btn.grid(row=1, column=0, columnspan=2, pady=10)

prefix_label = tk.Label(frame, text="Prefix: ", fg="blue")
prefix_label.grid(row=2, column=0, columnspan=2)

result_label = tk.Label(frame, text="Result: ", fg="green")
result_label.grid(row=3, column=0, columnspan=2)

# بدء التشغيل
root.mainloop()
