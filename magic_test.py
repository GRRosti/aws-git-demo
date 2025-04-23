# Scenario: A wizard student is being evaluated.
# 1. Input three stats: spell power, accuracy, and control.
print ("Assign spell power, accuracy, and control (0–100 each)")
spell_power = float(input("Spell Power is? 0 -100 ")) 	    
accuracy = float(input("Accuracy score is? 0 -100 ")) 
control = float(input("Control Rate is? 0 -100 "))    
average_score = (spell_power + accuracy + control) / 3
grade = "" 
#2. Check failures:
if spell_power < 40 or accuracy < 40 or control < 40:
    print ("Fail")
    exit(0)
else:
    # 2. Compute an average score.
    average_score = (spell_power + accuracy + control) / 3
    grade = ""
    # 3. Grade based on average if no automatic fail
    if average_score >= 90:
        grade = "Archmage"
    elif average_score >= 75:
        grade = "Mage"
    elif average_score >= 60:
        grade = "Apprentice"
    else:
        grade = "Fail"

# Print the results
print(f"Spell Power: {spell_power}")
print(f"Accuracy: {accuracy}")
print(f"Control: {control}")
print(f"Average Score: {average_score:.2f}") # Format average to two decimal places
print(f"Grade: {grade}")