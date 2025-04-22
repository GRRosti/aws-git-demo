salary = float(input("what is your salary"))
salary_net = salary * 0.88
rent = 3000
savings = 1000

if salary_net >= rent + savings:
    print("You can afford the rent and save money")
elif salary_net >= rent and salary_net - rent < savings:
    print("You can afford the rent but you will not save money")
else:
    print("You cannot afford the rent or save money")