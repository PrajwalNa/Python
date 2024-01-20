"""
Dev: Prajwal Nautiyal
Last Update: 13 January 2023
This is a simple calculator program using OOPs.
"""

import argparse
import sys
import timeit as ti

class cal:
    def __init__(self):
        self.__num1 = 0.00
        self.__num2 = 0.00
        self.__op = ""

    @staticmethod
    def __calculate(op: str, num1: float, num2: float) -> float:
        match op:
            case '+':
                val = num1 + num2
            case '-':
                val = num1 - num2
            case '*':
                val = num1 * num2
            case '/':
                val = num1 / num2
            case '**':
                val = num1 ** num2
            case '%':
                val = num1 % num2
            case _:
                val = 0.00
        return val
    
    def __call__(self, num1: float, num2: float, op: str):
        self.__num1 = num1
        self.__num2 = num2
        self.__op = op
        return cal.__calculate(self.__op, self.__num1, self.__num2)
    
    def __str__(self) -> str:
        return f"Number 1: {self.__num1} | Number 2: {self.__num2} | Operator: {self.__op}"
    
    def __repr__(self) -> str:
        return f"Calculator Object of expression: {self.__num1} {self.__op} {self.__num2}"

def inp()-> tuple[float, float, str]:
        parser = argparse.ArgumentParser(description="A basic calculator program. The available operators are '+', '-', '*', '/', '**', '%")
        parser.add_argument("-n", "--num", type = float, dest = "number", nargs = 2, help = "Argument to store enter two numbers", required = True)
        parser.add_argument("-o", "--operator", type = str, dest = "operator", help = "Argument to store the operator", required = True)
        try:
            args = parser.parse_args()
            return args.number[0], args.number[1], args.operator
        except Exception as e:
            print(f"Error: {e}")
            print("\nRunning without arguments.")
            n1 = float(input("Enter the first number: "))
            n2 = float(input("Enter the second number: "))
            op = input("Enter the operator: ")
            return n1, n2, op
     
# Main Function of the program
def main():
    start = ti.default_timer()
    try:
        a, b, ops = inp()
    except KeyboardInterrupt:
        print("Exit")
        sys.exit()
    obj = cal()
    try:
        calT_start = ti.default_timer()
        result = obj(a, b, ops)
        print(f"Result: {result}")
        calT_stop = ti.default_timer()
        print(f"Calculation Time: {(calT_stop - calT_start):.4f} seconds")
    except Exception as e:
        print(f"Error: {e}")
    stop = ti.default_timer()
    print(f"Total Runtime: {(stop - start):.4f} seconds")
    
if __name__ == "__main__":
    main()