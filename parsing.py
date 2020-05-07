
# Authored by Saauren Mankad


from math import pow

operators = ["+", "-", "*", "/", "^"]
brackets = ["(", ")"]


def tokenization(expr):

    operators_and_brackets = operators + brackets
    # if the character is an operator add space before and after it so it can easily be split
    for character in expr:
        if character in operators_and_brackets:
            expr = expr.replace(character, " " + character + " ")

    # split into list of tokens
    tokens = expr.split()

    # try to cast each token to a float, if unsuccessful try the next value in list
    for i in range(len(tokens)):
        try:
            tokens[i] = float(tokens[i])
        except(ValueError, TypeError):
            continue

    return tokens


def has_precedence(op1, op2):

    val1 = 0
    val2 = 0

    # highest precedence operator has the lowest number
    if op1 == "^":
        val1 = 1
    elif op1 == "*" or op1 == "/":
        val1 = 2
    elif op1 == "+" or op1 == "-":
        val1 = 3

    # put brackets at lowest precedence so that in complex_evaluation, calculation is skipped, rather than
    # trying to operate using a bracket operator
    elif op1 == "(" or op1 == ")":
        val1 = 4

    if op2 == "^":
        val2 = 1
    elif op2 == "*" or op2 == "/":
        val2 = 2
    elif op2 == "+" or op2 == "-":
        val2 = 3
    elif op2 == "(" or op2 == ")":
        val2 = 4

    # if the first val is lower than or equal val2, that means op1 has precedence
    op1_has_precedence = val1 < val2

    return op1_has_precedence


def do_operation(n1, operator, n2):

    # basic function that takes two numbers and an operator and returns
    # the result of the operation

    if operator == "^":
        return float(pow(n1, n2))

    elif operator == "*":
        return float(n1 * n2)

    elif operator == "/":
        return float(n1 / n2)

    elif operator == "+":
        return float(n1 + n2)

    elif operator == "-":
        return float(n1 - n2)


def simple_evaluation(tokens):
    plus_minus = ["+","-"]
    times_divide = ["*","/"]

    output = []    # will contain numbers and result
    op_stack = []  # will contain operators

    # save processing time if the math expr is just a basic one like 2*3
    if len(tokens) == 3:
        return do_operation(tokens[0], tokens[1], tokens[2])

    for token in tokens:

        if token in operators:
            
            # while the top item of the stack has a greater than (or equal to)
            # precedence and the stack is not empty
            while op_stack and (has_precedence(op_stack[-1], token) or (op_stack[-1] == token) or (op_stack[-1] in plus_minus
                           and token in plus_minus) or (op_stack[-1] in times_divide and token in times_divide)):
                cur_op = op_stack.pop()
                num2 = output.pop()
                num1 = output.pop()
                temp_res = do_operation(num1, cur_op, num2)
                output.append(temp_res)

            op_stack.append(token)

        else:
            output.append(token)

    # do final evaluation with remaining values
    while op_stack:
        cur_op = op_stack.pop()
        num2 = output.pop()
        num1 = output.pop()
        temp_res = do_operation(num1, cur_op, num2)
        output.append(temp_res)

    if len(output) > 0:
        result = output[0]
    else:
        result = None

    return result


def complex_evaluation(tokens):
    plus_minus = ["+", "-"]
    times_divide = ["*", "/"]

    op_stack = []  # will contain operators and brackets
    output = []    # will contain numbers and results of operating

    for token in tokens:


        if token in operators:

            # while the top item of the stack has a greater than (or equal to)
            # precedence and the stack is not empty
            while op_stack and (has_precedence(op_stack[-1], token) or (op_stack[-1] == token) or (op_stack[-1] in plus_minus
                           and token in plus_minus) or (op_stack[-1] in times_divide and token in times_divide)):

                # pop op_stack to grab the operator from top of stack and store to variable
                # pop output and store to num2, pop
                cur_op = op_stack.pop()
                num2 = output.pop()
                num1 = output.pop()
                temp_res = do_operation(num1, cur_op, num2)
                output.append(temp_res)

            # append operator token
            op_stack.append(token)

        # always append opening brackets
        elif token == "(":
            op_stack.append("(")

        # when closing bracket encountered, do calculations for everything inside
        # until an opening bracket is encountered, indicating end of expression
        # do not append this closing bracket (no reason to as we only want to check)
        elif token == ")":
            while op_stack and op_stack[-1] != "(":
                cur_op = op_stack.pop()
                num2 = output.pop()
                num1 = output.pop()
                temp_res = do_operation(num1, cur_op, num2)
                output.append(temp_res)

            # get rid of opening bracket, which will be at the top of the stack
            # once evaluation inside the brackets is done
            op_stack.pop()

        else:
            output.append(token)

    # final evaluation
    while op_stack and len(output) != 1:

        cur_op = op_stack.pop()
        num2 = output.pop()
        num1 = output.pop()
        temp_res = do_operation(num1, cur_op, num2)
        output.append(temp_res)

    if len(output) > 0:
        result = output[0]
    else:
        result = None

    return result


def evaluation(string):
    return complex_evaluation(tokenization(string))

print(evaluation("((4+2)*3 - (1 /3))"))
