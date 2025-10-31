import tkinter as tk
from tkinter import font as tkfont
import math


class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)

        # Configure modern color scheme
        self.bg_color = "#1e1e2e"
        self.display_bg = "#2d2d44"
        self.button_bg = "#3d3d5c"
        self.button_hover = "#4d4d6c"
        self.operator_bg = "#5865f2"
        self.operator_hover = "#6875ff"
        self.equals_bg = "#43b581"
        self.equals_hover = "#53c591"
        self.special_bg = "#f04747"
        self.text_color = "#ffffff"
        self.secondary_text = "#b9bbbe"

        self.root.configure(bg=self.bg_color)

        # Calculator state
        self.current = ""
        self.previous = ""
        self.operation = ""
        self.result_displayed = False
        self.memory = 0

        self.create_ui()

    def create_ui(self):
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Display frame
        display_frame = tk.Frame(main_frame, bg=self.display_bg, height=150)
        display_frame.pack(fill="x", pady=(0, 20))
        display_frame.pack_propagate(False)

        # Secondary display (shows operation)
        self.secondary_display = tk.Label(
            display_frame,
            text="",
            bg=self.display_bg,
            fg=self.secondary_text,
            font=("Segoe UI", 14),
            anchor="e",
            padx=20,
            pady=10
        )
        self.secondary_display.pack(fill="x")

        # Main display
        self.display = tk.Label(
            display_frame,
            text="0",
            bg=self.display_bg,
            fg=self.text_color,
            font=("Segoe UI", 36, "bold"),
            anchor="e",
            padx=20,
            pady=10
        )
        self.display.pack(fill="both", expand=True)

        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill="both", expand=True)

        # Button layout
        buttons = [
            ["MC", "MR", "M+", "M-"],
            ["C", "⌫", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["±", "0", ".", "="]
        ]

        for i, row in enumerate(buttons):
            row_frame = tk.Frame(button_frame, bg=self.bg_color)
            row_frame.pack(fill="both", expand=True, pady=2)

            for j, btn_text in enumerate(row):
                btn = self.create_button(row_frame, btn_text, i, j)
                btn.pack(side="left", fill="both", expand=True, padx=2)

    def create_button(self, parent, text, row, col):
        # Determine button color
        if text in ["C", "⌫"]:
            bg_color = self.special_bg
            hover_color = "#f15757"
        elif text in ["÷", "×", "-", "+"]:
            bg_color = self.operator_bg
            hover_color = self.operator_hover
        elif text == "=":
            bg_color = self.equals_bg
            hover_color = self.equals_hover
        elif text in ["MC", "MR", "M+", "M-"]:
            bg_color = "#4a4a6a"
            hover_color = "#5a5a7a"
        else:
            bg_color = self.button_bg
            hover_color = self.button_hover

        btn = tk.Label(
            parent,
            text=text,
            bg=bg_color,
            fg=self.text_color,
            font=("Segoe UI", 18, "bold"),
            cursor="hand2",
            relief="flat"
        )

        # Bind events
        btn.bind("<Button-1>", lambda e: self.on_button_click(text))
        btn.bind("<Enter>", lambda e: btn.configure(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg_color))

        return btn

    def on_button_click(self, value):
        if value.isdigit() or value == ".":
            self.handle_digit(value)
        elif value in ["÷", "×", "-", "+"]:
            self.handle_operator(value)
        elif value == "=":
            self.calculate()
        elif value == "C":
            self.clear()
        elif value == "⌫":
            self.backspace()
        elif value == "±":
            self.toggle_sign()
        elif value == "%":
            self.percentage()
        elif value == "MC":
            self.memory_clear()
        elif value == "MR":
            self.memory_recall()
        elif value == "M+":
            self.memory_add()
        elif value == "M-":
            self.memory_subtract()

    def handle_digit(self, digit):
        if self.result_displayed:
            self.current = ""
            self.result_displayed = False

        if digit == "." and "." in self.current:
            return

        if self.current == "0" and digit != ".":
            self.current = digit
        else:
            self.current += digit

        self.update_display()

    def handle_operator(self, op):
        if self.current:
            if self.previous and self.operation:
                self.calculate()
            self.previous = self.current
            self.current = ""

        self.operation = op
        self.result_displayed = False
        self.update_secondary_display()

    def calculate(self):
        if not self.previous or not self.current:
            return

        try:
            num1 = float(self.previous)
            num2 = float(self.current)

            if self.operation == "+":
                result = num1 + num2
            elif self.operation == "-":
                result = num1 - num2
            elif self.operation == "×":
                result = num1 * num2
            elif self.operation == "÷":
                if num2 == 0:
                    self.display.config(text="Error: Div by 0")
                    self.current = ""
                    self.previous = ""
                    self.operation = ""
                    return
                result = num1 / num2

            # Format result
            if result == int(result):
                result = int(result)
            else:
                result = round(result, 8)

            self.current = str(result)
            self.previous = ""
            self.operation = ""
            self.result_displayed = True
            self.update_display()
            self.secondary_display.config(text="")

        except Exception as e:
            self.display.config(text="Error")
            self.current = ""
            self.previous = ""
            self.operation = ""

    def clear(self):
        self.current = ""
        self.previous = ""
        self.operation = ""
        self.result_displayed = False
        self.display.config(text="0")
        self.secondary_display.config(text="")

    def backspace(self):
        if self.current:
            self.current = self.current[:-1]
            self.update_display()

    def toggle_sign(self):
        if self.current and self.current != "0":
            if self.current.startswith("-"):
                self.current = self.current[1:]
            else:
                self.current = "-" + self.current
            self.update_display()

    def percentage(self):
        if self.current:
            try:
                num = float(self.current)
                self.current = str(num / 100)
                self.update_display()
            except:
                pass

    def memory_clear(self):
        self.memory = 0

    def memory_recall(self):
        self.current = str(self.memory)
        self.result_displayed = False
        self.update_display()

    def memory_add(self):
        if self.current:
            try:
                self.memory += float(self.current)
            except:
                pass

    def memory_subtract(self):
        if self.current:
            try:
                self.memory -= float(self.current)
            except:
                pass

    def update_display(self):
        display_text = self.current if self.current else "0"

        # Limit display length
        if len(display_text) > 15:
            try:
                num = float(display_text)
                display_text = f"{num:.6e}"
            except:
                display_text = display_text[:15]

        self.display.config(text=display_text)

    def update_secondary_display(self):
        if self.previous and self.operation:
            text = f"{self.previous} {self.operation}"
            self.secondary_display.config(text=text)
        else:
            self.secondary_display.config(text="")


def main():
    root = tk.Tk()
    app = ModernCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
