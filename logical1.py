#part 1
# 1.1 true 
# true or false = true
# 1.2 false 
# 1.3 true
# 1.4 false or true = true

# part 2
# 10 <= x <= 20 (or x >= 10 and x <= 20)
# len(s) > 0 and 'py' in s (or s and 'py' in s)
# n < 0 or abs(n) > 100
# (user_role == 'admin' and active) or superuser
# not (temperature < 0 or temperature > 35) (or 0 <= temperature <= 35)

# Part 3: Access Eligibility Checker
print("Welcome to the Access Eligibility Checker!")
age = int(input("Please enter your age: "))
if age <= 0:
    print("Invalid age. Please enter a positive number.")
    exit()
else:
    pass
has_ticket = input("Do you have a ticket? (yes/no ): ").strip().lower()
is_ticket = has_ticket == 'yes' or has_ticket == 'y'
vip_code = input("What is your vip code? if not vip leave empty ").strip().upper()
is_vip_code = vip_code == "GOLDPASS"
eligible = False
if age >= 18 and (is_ticket) or is_vip_code:
    eligible = True
if eligible:
    print("You are eligible to enter the event.")
else:
    print("You are not eligible to enter the event.")
# Part 4: Logical Operators

