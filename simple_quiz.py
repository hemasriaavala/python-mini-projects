# simple_quiz.py
# A basic quiz game

def main():
    print("🎯 Simple Quiz")
    score = 0

    q1 = input("1. What is the capital of India? ").lower()
    if q1 == "delhi":
        score += 1

    q2 = input("2. What is 5 + 3? ")
    if q2 == "8":
        score += 1

    q3 = input("3. Who developed Python? ").lower()
    if "guido" in q3:
        score += 1

    print(f"\n✅ Your Score: {score}/3")

if __name__ == "__main__":
    main()
