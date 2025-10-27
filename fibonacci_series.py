# fibonacci_series.py
# Print Fibonacci series up to n terms

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        print(a, end=" ")
        a, b = b, a + b

def main():
    n = int(input("Enter number of terms: "))
    print("Fibonacci Series:")
    fibonacci(n)

if __name__ == "__main__":
    main()
