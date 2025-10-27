# factorial_finder.py
# Program to find factorial of a number

def factorial(n):
    return 1 if n == 0 else n * factorial(n - 1)

def main():
    num = int(input("Enter a number: "))
    print(f"Factorial of {num} is {factorial(num)}")

if __name__ == "__main__":
    main()
