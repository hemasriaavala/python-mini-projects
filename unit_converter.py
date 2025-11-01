def convert_temperature(value, unit_from, unit_to):
    if unit_from == "C" and unit_to == "F":
        return (value * 9/5) + 32
    elif unit_from == "F" and unit_to == "C":
        return (value - 32) * 5/9
    else:
        return value

def convert_length(value, unit_from, unit_to):
    conversions = {"m": 1, "cm": 100, "km": 0.001}
    return value * conversions[unit_to] / conversions[unit_from]

def convert_weight(value, unit_from, unit_to):
    conversions = {"kg": 1, "g": 1000, "lb": 2.20462}
    return value * conversions[unit_to] / conversions[unit_from]

def main():
    print("=== Universal Unit Converter ===")
    choice = input("Convert (temperature/length/weight): ").lower()

    if choice == "temperature":
        val = float(input("Value: "))
        from_u = input("From (C/F): ").upper()
        to_u = input("To (C/F): ").upper()
        print(f"Result: {convert_temperature(val, from_u, to_u):.2f}°{to_u}")

    elif choice == "length":
        val = float(input("Value: "))
        from_u = input("From (m/cm/km): ")
        to_u = input("To (m/cm/km): ")
        print(f"Result: {convert_length(val, from_u, to_u):.4f} {to_u}")

    elif choice == "weight":
        val = float(input("Value: "))
        from_u = input("From (kg/g/lb): ")
        to_u = input("To (kg/g/lb): ")
        print(f"Result: {convert_weight(val, from_u, to_u):.4f} {to_u}")

    else:
        print("Invalid category.")

if __name__ == "__main__":
    main()

