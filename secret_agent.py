# Secret Agent Code Generator

# 1. Inputs (use input() in this exact order)
code1_input = input()
code2_input = input()
code3_input = input()
numA_input_str = input()
numB_input_str = input()

# Convert inputs to lowercase for consistency and store in final variables
code1 = code1_input.lower()
code2 = code2_input.lower()
code3 = code3_input.lower()

# Assume integer conversion will not raise ValueError based on constraints,
# but will validate the *value* later.
numA = int(numA_input_str)
numB = int(numB_input_str)

# 2. Validation

# Check for non-alphabetic characters in codes
if not code1.isalpha() or not code2.isalpha() or not code3.isalpha():
    print("Invalid codeword")
    exit() # Exit the script

# Check if numA or numB are less than 1
if numA < 1 or numB < 1:
    print("Invalid numbers")
    exit() # Exit the script

# Store original numA and numB for average calculation before potential swapping logic below
# (although swapping is assigned to new variables, explicitly using originals is clear)
original_numA = numA
original_numB = numB


# 3. Variable Operations (create these variables)

# 1. combined: join the three codes with hyphens
combined = f"{code1}-{code2}-{code3}"

# 2. secret_number: compute (numA * numB) + numA - numB
secret_number = (original_numA * original_numB) + original_numA - original_numB

# 3. swapped_A, swapped_B: swap the values of numA and numB without using a third variable
swapped_A, swapped_B = original_numB, original_numA

# 4. avg_value: average of the original numA and numB
# Use float division to ensure the average is a float
avg_value = (original_numA + original_numB) / 2.0

# 5. message_length: length of combined (number of characters)
message_length = len(combined)

# 6. is_palindrome: Boolean indicating whether combined (with hyphens removed)
# reads the same forward and backward
combined_no_hyphens = combined.replace('-', '')
is_palindrome = combined_no_hyphens == combined_no_hyphens[::-1]


# 4. Output
print("Secret Code: " + combined)
print("Secret Number: " + str(secret_number))
print(f"Swapped Values: A={swapped_A}, B={swapped_B}")
print("Average of Originals: " + str(avg_value))
print("Combined Length: " + str(message_length))
print("Palindrome: " + str(is_palindrome))