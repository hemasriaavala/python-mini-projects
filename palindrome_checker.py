# Palindrome Checker

def is_palindrome(string):
    # Remove spaces and make lowercase
    clean_string = string.replace(" ", "").lower()
    # Check if the string equals its reverse
    return clean_string == clean_string[::-1]

if __name__ == "__main__":
    text = input("Enter a word or phrase: ")
    if is_palindrome(text):
        print("✅ It's a palindrome!")
    else:
        print("❌ Not a palindrome.")
