# temp_converter.py
choice = input("Convert from (C/F): ").upper()
temp = float(input("Enter temperature: "))

if choice == 'C':
    print("In Fahrenheit:", (temp * 9/5) + 32)
elif choice == 'F':
    print("In Celsius:", (temp - 32) * 5/9)
else:
    print("Invalid choice!")
