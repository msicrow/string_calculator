import re
import functools

commands = {"/help": "Please enter a calculation. "
                     "Expressions can include the following operations:"
                     "+, -, *, / and brackets can be used.",
            "/exit": "Bye!"}
user_variables = {}


def compare(key_1, key_2):
    if len(key_1) > len(key_2):
        return 1
    elif len(key_2) > len(key_1):
        return -1
    else:
        return 0


def replace_user_variable(inp):
    key_list = [key for key in user_variables.keys()]
    key_list.sort(key=functools.cmp_to_key(compare), reverse=True)
    for key in key_list:
        if key in inp:
            inp = inp.replace(key, user_variables[key])
        else:
            pass
    return inp


def format_string(inp):
    inp = inp.replace(" ", "")
    while True:
        length = len(inp)
        inp = inp.replace("--", "+").replace("++", "+").replace("-+", "-").replace("+-", "-")
        if len(inp) == length:
            break
        else:
            continue
    inp = replace_user_variable(inp)
    return inp


def peek(stack):
    return stack[-1] if stack else None


def operation_precedence(op1, op2):
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}
    return precedence[op1] >= precedence[op2]


def calculation(nums, ops):
    operator = ops.pop()
    lhs = nums.pop()
    rhs = nums.pop()
    if operator == "+":
        nums.append(lhs + rhs)
    elif operator == "-":
        nums.append(rhs - lhs)
    elif operator == "*":
        nums.append(lhs * rhs)
    elif operator == "/":
        nums.append(rhs / lhs)


def store_var(inp):
    variable = inp.replace(" ", "").split("=")
    if re.search(r"\d", variable[0]):
        print("Invalid identifier")
    elif re.search(r"(?:\d+[a-zA-Z]+|[a-zA-Z]+\d+)", variable[1]) \
            or (variable[1].isalpha() and variable[1] not in user_variables.keys()):
        print("Invalid assignment")
    else:
        variable[1] = replace_user_variable(variable[1])
        operator = re.findall("[+/*()-]", variable[1])
        if operator:
            variable[1] = str(evaluate(variable[1]))
        user_variables[variable[0]] = variable[1]  # if no operator, key == LHS, value == RHS


def evaluate(inp):
    tokens = re.findall("[+/*()-]|\d+", inp)
    integers = []
    operators = []
    try:
        for token in tokens:
            if token.isnumeric():
                integers.append(int(token))
            elif token == "(":
                operators.append(token)
            elif token == ")":
                stack_top = peek(operators)
                while stack_top and stack_top != "(":
                    calculation(integers, operators)
                    stack_top = peek(operators)
                operators.pop()
            else:
                stack_top = peek(operators)
                while stack_top is not None and stack_top not in "()" and operation_precedence(stack_top, token):
                    calculation(integers, operators)
                    stack_top = peek(operators)
                operators.append(token)

        while peek(operators) is not None:
            calculation(integers, operators)
        return integers[0]
    except IndexError:
        print("Invalid expression")


def main():
    while True:
        inp = input()
        if inp in commands:
            if inp == "/help":
                print(commands["/help"])
            else:
                print(commands["/exit"])
                break
        elif not inp:
            pass
        elif inp[:1] == "/":
            print("Unknown command")
        elif "=" in inp:
            if inp.count("=") > 1:
                print("Invalid assignment")
            else:
                store_var(inp)
        elif inp.startswith("-") and not re.match("[+/*()-]", inp[1:]):
            print(inp)
        elif re.search(r"(?:\d+[a-zA-Z]+|[a-zA-Z]+\d+)", inp):
            print("Invalid identifier")
        elif inp.isalpha():
            if inp in user_variables.keys():
                print(user_variables[inp])
            else:
                print("Unknown variable")
        else:
            inp = format_string(inp)
            if evaluate(inp) is not None:
                print(evaluate(inp))
            else:
                pass


if __name__ == "__main__":

    main()
