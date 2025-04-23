print("Interactive Two-Number Calculator")
print("Enter numbers and operators one by one.")
print("Supported operators: +, -, *, /, %, **, //")
print("You can use 'ans' as a number to refer to the previous result.")
# 2. Create a function that takes two numbers and an operator as input
number1 = float(input("Enter first number: "))
number2 = float(input("Enter second number: "))
operator = input("Enter operation (+, -, *, /, %, **, //): ")
result = None
def calculator(num1, num2, op):
    if op == '+':
        return num1 + num2
    elif op == '-':
        return num1 - num2
    elif op == '*':
        return num1 * num2
    elif op == '/':
        if num2 != 0:
            return num1 / num2
        else:
            print("Error: Division by zero is not allowed.")
    elif op == '%':
        # Handle modulo by zero
        if num2 == 0:
            print("Error: Modulo by zero is not allowed.")
            return None  # Skip processing and return None
        return num1 % num2
    elif op == '**':
        return num1 ** num2
    elif op == '//':
        # Handle integer division by zero
        if num2 == 0:
            print("Error: Integer division by zero is not allowed.")
            return None  # Skip processing and return None
        return num1 // num2
    else:
        print("Error: Invalid operation. Please enter one of +, -, *, /, %, **, //.")
        return None
# 1. Create a simple calculator that takes two numbers and an operation as input
# 2. Perform the operation and print the result
result = calculator(number1, number2, operator) 
if result is not None:
    print(f"The result of {number1} {operator} {number2} is: {result}")
# 3. Handle division by zero and invalid operations gracefully 
while True:
    try:
        number1 = float(input("Enter first number: "))
        number2 = float(input("Enter second number: "))
        operator = input("Enter operation +, -, *, /, %, **, //.")
        result = calculator(number1, number2, operator)
        if result is not None:
            print(f"The result of {number1} {operator} {number2} is: {result}")
    except ValueError:
        print("Invalid input. Please enter numeric values.")
# 4. Allow the user to use the result of the previous operation in the next calculation
    # 5. Add support for additional operations like exponentiation and integer division
    # 6. Allow the user to exit the program gracefully
    if operator.lower() or number1.lower() or number2.lower() == 'exit':
        print("Exiting the calculator. Goodbye!")
        break
    else:
        print("Invalid operation. Please enter a valid operator.")
# 7. Add support for using the result of the previous operation in the next calculation                                                                  
