from pythonds.basic.stack import Stack

def infix2postfix(infixInput):
    priority = {"^": 4, "*": 3, "/": 3, "-": 2, "+": 2, "(": 1}
    operation = Stack()
    postfix = []
    tokenlist = infixInput
    
    for token in tokenlist:
        if token.isalpha() or token.isdigit():  # حرف أو رقم
            postfix.append(token)
        elif token == "(":
            operation.push(token)
        elif token == ")":
            while not operation.isEmpty() and operation.peek() != "(":
                postfix.append(operation.pop())
            if not operation.isEmpty():
                operation.pop()  # إزالة "("
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
    if isinstance(exp, str):
        exp = exp.split()
    exp = exp[::-1]
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

def mathEvaluation(expr):
    opStack = Stack()
    tokenlist = expr.split()
    
    for token in reversed(tokenlist):
        if token.replace('.', '', 1).isdigit():  # دعم الأرقام العشرية
            opStack.push(float(token))
        elif token.isalpha():
            value = input(f"Enter value for {token}: ")
            try:
                opStack.push(float(value))
            except ValueError:
                return f"Invalid value for variable {token}. Please enter a number."
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

if __name__ == '__main__':
    print("Welcome to the infix-to-prefix converter and evaluator!")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("\nEnter infix expression: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        if not validate_expression(user_input):
            print("Error: Unbalanced parentheses")
            continue
        
        rev_input = revExp(user_input)
        postfix = infix2postfix(rev_input)
        
        if "Error" in postfix:
            print(postfix)
            continue
        
        prefix = "".join(reversed(postfix))
        print(f'Prefix:-->  {prefix}')
        
        result = mathEvaluation(prefix)
        print(f'Result:-->  {result}')
