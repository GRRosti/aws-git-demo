age = int(input("Enter your age: "))
if age < 0:
    print("Invalid age")
    exit()
day = input("Weekday/Weekend: ").strip().lower()   
if day not in ["weekday", "weekend"]:
    print("Invalid day")
    exit()
membership = input("Are you a member? (yes/no): ").strip().lower()
#pricing
base_price = 20
def calculate_price(age, day, membership):
    if age < 13:
        price = base_price * 0.5
    elif age >= 60:
        price = base_price * 0.7
    else:
        price = base_price

    if day == "weekend":
        price += 5

    if membership == "yes":
        price -= 2

    return price
# Calculate the price
price = calculate_price(age, day, membership)
# Display the price
print(f"The ticket price is: ${price:.2f}")
# The ticket price is: $20.00