my_string =input("Enter a string: ")
def reverse_string(my_string):
    # Base case: if the string is empty or has one character, return it
    if len(my_string) <= 1:
        return my_string
    # Recursive case: reverse the substring and append the first character at the end
    else:
        return my_string[::-1] 
# Call the function and print the result
reversed_string = reverse_string(my_string)   
print(f"Reversed string:", reversed_string)
# This code defines a function to reverse a string using recursion.