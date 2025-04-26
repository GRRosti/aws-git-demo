# 1. Create a dictionary to store information about students
students = {
    "Alice": {"grade": 85, "age": 16},
    "Bob": {"grade": 92, "age": 17},
    "Charlie": {"grade": 78, "age": 16}
}

print("Initial students dictionary:")
print(students)
print("-" * 20)

# 2. Perform operations on the dictionary

# 2.1. Add a new student
print("Adding a new student: 'David' with grade 95 and age 15")
students["David"] = {"grade": 95, "age": 15}
print("Dictionary after adding David:")
print(students)
print("-" * 20)

# 2.2. Update the grade of an existing student
print("Updating Alice's grade to 88")
if "Alice" in students: # Check if student exists before updating
    students["Alice"]["grade"] = 88
    print("Dictionary after updating Alice's grade:")
    print(students)
else:
    print("Alice not found in the dictionary.")
print("-" * 20)

# 2.3. Remove a student from the dictionary
print("Removing student 'Charlie'")
if "Charlie" in students: # Check if student exists before removing
    del students["Charlie"]
    # Alternative using pop: students.pop("Charlie", None) # Use pop with a default to avoid error if key not found
    print("Dictionary after removing Charlie:")
    print(students)
else:
     print("Charlie not found in the dictionary.")
print("-" * 20)


# 2.4. Calculate and print the average grade of all students
total_grades = 0
student_count = 0

for student_name, student_data in students.items():
    total_grades += student_data['grade']
    student_count += 1

if student_count > 0:
    average_grade = total_grades / student_count
    print(f"Total students: {student_count}")
    print(f"Total grades sum: {total_grades}")
    print(f"Average grade of all students: {average_grade:.2f}") # Format to 2 decimal places
else:
    print("No students in the dictionary to calculate the average grade.")
print("-" * 20)


# 2.5. Find and print the name of the student with the highest grade
highest_grade = -1 # Initialize with a value lower than any possible grade (0-100)
student_with_highest_grade = None

if students: # Proceed only if the dictionary is not empty
    # Initialize with the first student's data to handle edge cases easily
    first_student_name = list(students.keys())[0]
    highest_grade = students[first_student_name]['grade']
    student_with_highest_grade = first_student_name

    # Iterate through the rest of the students
    for student_name, student_data in students.items():
        current_grade = student_data['grade']
        if current_grade > highest_grade:
            highest_grade = current_grade
            student_with_highest_grade = student_name

    print(f"The student with the highest grade is: {student_with_highest_grade} (Grade: {highest_grade})")
else:
    print("No students in the dictionary to find the highest grade.")

print("-" * 20)