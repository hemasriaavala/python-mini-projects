# Dice Roller Simulator
import random

def roll_dice():
    return random.randint(1, 6)

if __name__ == "__main__":
    while True:
        input("Press Enter to roll the dice 🎲 (or type 'exit' to quit): ")
        print("You rolled:", roll_dice())
        choice = input("Roll again? (y/n): ")
        if choice.lower() != 'y':
            print("Goodbye! 👋")
            break
