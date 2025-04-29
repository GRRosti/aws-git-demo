number = int(input("Enter your number "))
if number<= 1:
    print("Not prime")
else:
    for i in range(2, number):
        if number % i == 0:
            print("Not prime")
            break
    else:
        print("Prime")
# This code checks if a number is prime or not.

