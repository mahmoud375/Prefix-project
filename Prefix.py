from pythonds.basic.stack import Stack

def infix2postfix(infixInput):
    
    priority = {} # creating a dictionary
    
    priority["^"] = 4
    priority["*"] = 3
    priority["/"] = 3
    priority["-"] = 2
    priority["+"] = 2
    priority["("] = 1
    
    operation=Stack() # operation {*,/,+,-} will be kept in a stack
    postfix=[] # the postfix expression in a list 
    
    tokenlist=infixInput # do not need .split() function here because already been used in revexp()
    
    for token in tokenlist:        
        if token.isalpha() or token.isdigit(): # normal toke or a number either a one digit or more
            postfix.append(token)
            
        elif token == "(": 
            operation.push(token)    
            
        elif token == ")":
            topToken = operation.pop()
            while topToken != "(": 
                postfix.append(topToken)    # pop all operators until reaching "("
                topToken = operation.pop()  # reassigning the top token value
        
        else:
            while not operation.isEmpty() and\
                priority[operation.peek()]> priority[token]: # the deference here will be that > values will be the only one to pop out
                    postfix.append(operation.pop())
                    # if the stack is not empty and the peek value is > the new token it will pop it
            operation.push(token)
            
    while not operation.isEmpty():
        postfix.append(operation.pop()) # popping the remaining operators until the stack is empty 
            
    return" ".join(postfix) # rejoining the list

def revExp(exp):
    #convert exp to list if it string (exp.split() >>> error if exp is list)
    if isinstance(exp,str):
        exp = exp.split()
    #reverse exp 
    exp = exp[::-1]
    #replace ')' to '(' and '(' to ')'
    for i in range(len(exp)):
        if exp[i] == "(":
            exp[i] = ")"
        elif exp[i] == ")":
            exp[i] = "("
        
    return exp  

def doMath(operator, operand1, operand2):
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
        return "maths error"

def mathEvaluation(expr):
    opStack = Stack()
    tokenlist = expr.split()

    for token in reversed(tokenlist):  
        if token.isnumeric():  # If the token is a number
            opStack.push(int(token))
        elif token.isalpha():  # If the token is a variable
            value = input(f"Enter value for {token}: ")
            try:
                opStack.push(int(value))  
            except ValueError:
                return f"Invalid value for variable {token}. Please enter a number."
        else:  
            if opStack.size() < 2:  
                return "Can't evaluate, too few operands"
            operand1 = opStack.pop()
            operand2 = opStack.pop()
            result = doMath(token, operand1, operand2)
            opStack.push(result)

    if opStack.size() == 1:
        return opStack.pop()
    else:
        return "Can't evaluate, invalid expression"




if __name__ == '__main__' :
    while True:
        prefix = "".join(reversed(infix2postfix(revExp(input('\nEnter infix expression: ')))))
        print(f'Prefix:-->  {prefix}')
        print(f'output:-->  {mathEvaluation(prefix)}')
