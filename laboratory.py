def check_lab_safety(temperature, pressure, voltage):
  """Checks if lab conditions are safe based on temperature, pressure, and voltage."""

  print(f"Checking conditions: Temperature={temperature}°C, Pressure={pressure} kPa, Voltage={voltage} V")

  # 2. Conditions:
  # ○ Temperature must be between 20 and 80
  # ○ Pressure under 50
  # ○ Voltage between 200–250
  is_temperature_safe = 20 <= temperature <= 80
  is_pressure_safe = pressure < 50
  is_voltage_safe = 200 <= voltage <= 250

  # 3. If all are true: print “Safe to proceed”. Otherwise: print “Unsafe conditions”.
  if is_temperature_safe and is_pressure_safe and is_voltage_safe:
    print("Safe to proceed")
  else:
    print("Unsafe conditions")

  print("-" * 20) # Separator for multiple calls
try: 
    temperature = float(input("Enter temperature in °C: "))
    pressure = float(input("Enter pressure in kPa: "))
    voltage = float(input("Enter voltage in V: "))
    check_lab_safety(temperature, pressure, voltage)
except ValueError:
    print("Invalid input. Please enter numeric values for temperature, pressure, and voltage.") 

# Example usage:
#check_lab_safety(temperature=25, pressure=40, voltage=220) # All safe
#check_lab_safety(temperature=15, pressure=40, voltage=220) # Temperature unsafe
#check_lab_safety(temperature=25, pressure=60, voltage=220) # Pressure unsafe
#check_lab_safety(temperature=25, pressure=40, voltage=190) # Voltage unsafe
#check_lab_safety(temperature=90, pressure=60, voltage=260) # All unsafe