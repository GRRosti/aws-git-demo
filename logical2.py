
def validate_form():
    """Reads username, password, and email and validates them based on specific criteria."""
    username = input("Enter username: ")
    password = input("Enter password: ")
    email = input("Enter email: ")

    # Check if username is non-empty
    is_username_valid = bool(username) # An empty string evaluates to False

    # Check if password length >= 8 AND contains at least one digit
    is_password_long_enough = len(password) >= 8
    has_digit = any(char.isdigit() for char in password)
    is_password_valid = is_password_long_enough and has_digit

    # Check if email contains exactly one "@" AND ends with ".com"
    has_one_at_sign = email.count('@') == 1
    ends_with_dot_com = email.endswith(".com")
    is_email_valid = has_one_at_sign and ends_with_dot_com

    # Combine all conditions in a single if statement
    if is_username_valid and is_password_valid and is_email_valid:
        print("Form valid")
    else:
        print("Form invalid")

# Run the validator
validate_form()