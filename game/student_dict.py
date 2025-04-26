import statistics # Using the statistics module for average is an alternative, but we'll calculate manually as requested
from typing import Dict, List, Set, Any, Tuple

# 1. Create a dictionary to store information about students
# The structure is { student_name: { 'age': int, 'subjects': List[str], 'grades': Set[float] } }
students: Dict[str, Dict[str, Any]] = {
    "Alice": {"age": 16, "subjects": ["Math", "Physics", "Chemistry"], "grades": {85.5, 90, 88.0}},
    "Bob": {"age": 17, "subjects": ["History", "Geography"], "grades": {75, 88, 92.5}},
    "Charlie": {"age": 16, "subjects": ["Computer Science", "Math", "Physics"], "grades": {95, 89.5, 91, 95}}, # Note: Set handles duplicate grades like 95
}

print("Initial students dictionary:")
print(students)
print("-" * 30)

# 2. Perform the following operations:

# 2.1. Add a new student
print("Adding a new student: 'David'")
students["David"] = {"age": 15, "subjects": ["Biology", "Chemistry", "Math"], "grades": {79, 85.0, 81.5}}
print("Students dictionary after adding David:")
print(students)
print("-" * 30)

# 2.2. Update the grades of an existing student
student_to_update_grades = "Alice"
new_grades_for_alice = {91.5, 93} # Using a set for new grades to easily update the existing set

print(f"Updating grades for {student_to_update_grades}")
if student_to_update_grades in students:
    # Add new grades to the existing set using the update method
    students[student_to_update_grades]['grades'].update(new_grades_for_alice)
    print(f"Students dictionary after updating {student_to_update_grades}'s grades:")
    print(students)
else:
    print(f"Student '{student_to_update_grades}' not found.")
print("-" * 30)

# 2.3. Remove a subject from a student's list of subjects
student_to_update_subjects = "Bob"
subject_to_remove = "Geography"

print(f"Removing '{subject_to_remove}' from {student_to_update_subjects}'s subjects")
if student_to_update_subjects in students:
    if subject_to_remove in students[student_to_update_subjects]['subjects']:
        students[student_to_update_subjects]['subjects'].remove(subject_to_remove)
        print(f"Students dictionary after removing '{subject_to_remove}' for {student_to_update_subjects}:")
        print(students)
    else:
        print(f"Subject '{subject_to_remove}' not found for {student_to_update_subjects}.")
else:
    print(f"Student '{student_to_update_subjects}' not found.")
print("-" * 30)

# 2.4. Find the average grade of a specific student
def calculate_average_grade(student_grades_set: Set[float]) -> float:
    """Calculates the average of grades from a set by converting to a list."""
    grades_list = list(student_grades_set) # Convert set to list as requested
    if not grades_list: # Check if list is empty to avoid division by zero
        return 0.0
    return sum(grades_list) / len(grades_list)

student_to_average = "Alice"
if student_to_average in students:
    alice_grades_set = students[student_to_average]['grades']
    alice_average = calculate_average_grade(alice_grades_set)
    print(f"Grades for {student_to_average}: {alice_grades_set}")
    print(f"Average grade for {student_to_average}: {alice_average:.2f}")
else:
    print(f"Student '{student_to_average}' not found.")
print("-" * 30)


# 2.5. Find the student with the highest average grade
highest_average_grade = -1.0 # Initialize with a low value
student_with_highest_average = None

print("Calculating average grades for all students...")
for student_name, student_data in students.items():
    current_average = calculate_average_grade(student_data['grades'])
    print(f"{student_name}'s average grade: {current_average:.2f}")
    if current_average > highest_average_grade:
        highest_average_grade = current_average
        student_with_highest_average = student_name

print("-" * 30)
if student_with_highest_average:
    best_student_info = students[student_with_highest_average]
    print(f"Student with the highest average grade:")
    print(f"Name: {student_with_highest_average}")
    print(f"Age: {best_student_info['age']}")
    print(f"Subjects: {', '.join(best_student_info['subjects'])}")
    print(f"Average Grade: {highest_average_grade:.2f}")
else:
    print("No students available to find the highest average grade.")
print("-" * 30)


# 3. Create a tuple for each student and print sorted by number of subjects
student_summary_tuples: List[Tuple[str, int, int]] = []

for student_name, student_data in students.items():
    num_subjects = len(student_data['subjects'])
    student_tuple = (student_name, student_data['age'], num_subjects)
    student_summary_tuples.append(student_tuple)

# Sort the list of tuples based on the number of subjects (the third element, index 2)
# We use a lambda function as the key for the sorted function
sorted_students_by_subjects = sorted(student_summary_tuples, key=lambda item: item[2])

print("Student summaries (Name, Age, Number of Subjects) sorted by number of subjects:")
for student_tuple in sorted_students_by_subjects:
    print(student_tuple)
print("-" * 30)

    
# This code defines a dictionary to store student information and provides functions to add, update, remove students, and calculate the average grade.      