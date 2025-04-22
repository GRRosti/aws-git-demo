
age = input("What is your age?")
if int(age) < 0:
    print("Invalid age")
elif int(age) < 18:
        print("You cannot enter the castle.")  
        exit()
is_blacklisted = input("Are you blacklisted? (True/False)")
if is_blacklisted == "True":
    print("You cannot enter the castle.")
    exit()
elif is_blacklisted == "False" and int(age) >= 18:       
        print("Please answer the following questions to check if you can enter the castle.")
has_goldpass = input("Do you have a gold pass? (True/False)")
if has_goldpass == "True":
    print("You can enter the castle.")
    exit()
elif has_goldpass == "False":
    is_royal = input("Are you part of royal family? (True/False)")
    if is_royal == "True":
        print("You can enter the castle.")
        exit()
    else:
        print("You cannot enter the castle.")
        exit()