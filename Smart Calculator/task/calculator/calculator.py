def help_command():
    print("Please enter either an operation using either addition or subtraction.")


def standard_calc(string_inp):
    if "-" in string_inp or "+" in string_inp:
        if string_inp.endswith("-") or string_inp.endswith("+"):
            print("Invalid expression")
        else:
            operation = string_inp.replace("-", "+-")
            operation = operation.replace(" ", "").split("+")
            print(sum([int(x) for x in operation if x != ""]))
    else:
        if string_inp.isdigit():
            print(string_inp)
        else:
            if "-" not in string_inp or "+" not in string_inp:
                print("Invalid expression")
            else:
                operation = string_inp.replace(" ", "")
                print(sum([int(x) for x in operation if x != ""]))


def double_minus(string_inp):
    if string_inp.endswith("--"):
        print("Invalid expression")
    else:
        operation = string_inp.replace("--", "+")
        standard_calc(operation)


while True:
    calc = input()
    if not calc:
        continue
    elif calc.startswith("/"):
        if calc == "/exit":
            print("Bye!")
            break
        elif calc == "/help":
            help_command()
        else:
            print("Unknown command")
    elif "--" in calc:
        double_minus(calc)
    else:
        try:
            standard_calc(calc)
        except ValueError:
            print("Invalid expression")
