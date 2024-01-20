"""Dev: Prajwal Nautiyal
Last Update: 12 March 2023
"""


def Prime(n):
    if n == 1:
        return False
    elif n == 2:
        return True
    else:
        for x in range(2, n):
            if n % x == 0:
                return False
        return True
    
def main():
    try:
        while True:
            try:
                n = int(input("Enter a number: "))
                if Prime(n):
                    print("Prime")
                else:
                    print("Not Prime")
            except Exception as e:
                print("Invalid input: ", e)
    except KeyboardInterrupt:
        print("Program terminated")

if __name__ == "__main__":
    main()