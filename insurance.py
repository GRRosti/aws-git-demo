# insurance.py

def calculate_insurance_quote(age, accident_count):
  """Calculates a base insurance quote based on age and accident count."""
  # 2. If age < 25 → base premium is 3000; else 2000.
  if age < 25:
    base_premium = 3000
  else:
    base_premium = 2000

  # 3. Add 500 for each accident.
  accident_cost = accident_count * 500
  total_premium = base_premium + accident_cost

  # 4. If premium exceeds 5000, print “High Risk”; else “Standard”.
  if total_premium > 5000:
    risk_level = "High Risk"
  else:
    risk_level = "Standard"

  print(f"Driver Age: {age}")
  print(f"Accident Count: {accident_count}")
  print(f"Base Premium: {base_premium}")
  print(f"Accident Cost: {accident_cost}")
  print(f"Total Premium: {total_premium}")
  print(f"Risk Level: {risk_level}")
  print("-" * 20) # Separator for multiple calls

try:
            while True:
                    age = int(input("Enter driver age: "))
                    accident_count = int(input("Enter number of accidents: "))
                    calculate_insurance_quote(age, accident_count)
                    continue_prompt = input("Do you want to calculate another quote? (yes/no): ").strip().lower()
                    if continue_prompt != 'yes':
                            break
except ValueError:
            print("Invalid input. Please enter numeric values.")
except KeyboardInterrupt:
            print("\nExiting the program.")

finally:
      print("Thank you for using the insurance calculator.")
## calculate_insurance_quote(40, 0) # Age >= 25, 0 accidents