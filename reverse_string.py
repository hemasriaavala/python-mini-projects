# reverse_string.py
# Reverse a string entered by the user

def main():
    text = input("Enter a string: ")
    reversed_text = text[::-1]
    print("Reversed string:", reversed_text)

if __name__ == "__main__":
    main()
