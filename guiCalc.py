"""
Dev: Prajwal Nautiyal
Date: 18 April 2023
Description: GUI Calculator using Tkinter module
"""

import time
import tkinter as tk


class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")

        # Initialize variables
        self.total = 0
        self.current = ""
        self.input_value = True
        self.check_sum = False
        self.op = ""
        self.result = False

        # Create display screen
        self.display = tk.Entry(self.master)
        self.display.grid(row=0, columnspan=6, sticky=tk.W+tk.E)

        # Create buttons
        self.create_buttons()

    def create_buttons(self):
        # Create buttons
        self.button_list = [
            "7", "8", "9", "+",
            "4", "5", "6", "-",
            "1", "2", "3", "*",
            "C", "0", "=", "/",
        ]

        # Initialize row and column
        row = 1
        column = 0

        for button in self.button_list:
            # Define command
            action = lambda x=button: self.click_event(x)

            # Create button
            tk.Button(self.master, text=button, command=action, width=10).grid(row=row, column=column, sticky=tk.W+tk.E)

            # Increment column
            column += 1

            # Check if column == 4
            if column > 3:
                column = 0
                row += 1

    def click_event(self, key):
        if self.check_sum:
            self.result = False
            self.display.delete(0, tk.END)
            self.total = 0
            self.input_value = True
            self.current = 0
            self.check_sum = False
        match key:
            case "C":
                self.display.delete(0, tk.END)
                self.input_value = True
                self.check_sum = True
            case "=":
                self.calc_sum()
                self.check_sum = True
            case "+":
                self.calc_sum()
                self.op = "+"
                self.input_value = True
            case "-":
                self.calc_sum()
                self.op = "-"
                self.input_value = True
            case "*":
                self.calc_sum()
                self.op = "*"
                self.input_value = True
            case "/":
                self.calc_sum()
                self.op = "/"
                self.input_value = True
            case _:
                if self.input_value:
                    self.current = key
                    self.input_value = False
                else:
                    if key == ".":
                        if key in self.current:
                            return
                    self.current += key
                self.display.delete(0, tk.END)
                self.display.insert(0, self.current)

    def calc_sum(self):
        self.result = True
        self.current = float(self.current)
        self.check_sum = False
        self.input_value = True
        match self.op:
            case "+":
                self.total += self.current
            case "-":
                self.total -= self.current
            case "*":
                self.total *= self.current
            case "/":
                try:
                    self.total /= self.current
                except ZeroDivisionError:
                    self.display.delete(0, tk.END)
                    self.display.insert(0, "Error")
                    self.check_sum = True
            case _:
                self.total = self.current
        self.current = 0
        self.display.delete(0, tk.END)
        self.display.insert(0, str(self.total))


root = tk.Tk()
my_gui = Calculator(root)
root.mainloop()