print ("please enter two different numbers greater than 0")
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))
test_range = range(a, b)
dividers = int(input("Enter a number to check if it divides the range: "))
list1 = []
list2 = []
def test_division():
    for i in test_range:
        if i % dividers == 0:
            while True:
                list1.append(i)
                break
        else:
            list2.append(i)
test_division()
print("The numbers that are divisible by", dividers, "are:","\n", list1, end="\n\n")
print("There are", len(list1), "numbers that are divisible by", dividers, end="\n\n")
print("The numbers that are not divisible by", dividers, "are:","\n", list2, end="\n\n")
print("There are", len(list2), "numbers that are not divisible by", dividers, end="\n\n")
print("Thanks for playing!")
