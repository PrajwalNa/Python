"""
Dev: Prajwal Nautiiyal
Last Update: 20 September 2022
"""

import time

def inp():#function for taking input
    print("Enter your name:", end='')
    nam = input()
    print("Enter your age:", end='')
    ag = int(input())
    return nam, ag

def out(nm,age):#function to process output and the list gimmick
    print(f"{nm}\taged {age}")
    print('*'*20,("Enjoy the list"),'*'*20)
    i=64#comment this block if trying modifications with the print statement above 
    try:
        while(i<122):
            i=i+1
            n = [91,92,93,94,95,96]
            if i not in n:
                print("\rChar="+chr(i),end="\t")
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n",'#'*20,"Program Closed",'#'*20)

# nm,a=inp()#calling the input function
# out(nm,a)#calling the output function

def num2words(num):
    num = int(num)
    if num == 0:
        return "zero"
    if num < 0:
        return "minus " + num2words(-num)
    words = []
    if (num // 1000000000) > 0:
        words.append(num2words(num // 1000000000) + " billion")
        num %= 1000000000
    if (num // 1000000) > 0:
        words.append(num2words(num // 1000000) + " million")
        num %= 1000000
    if (num // 1000) > 0:
        words.append(num2words(num // 1000) + " thousand")
        num %= 1000
    if (num // 100) > 0:
        words.append(num2words(num // 100) + " hundred")
        num %= 100
    if num > 0:
        if num < 20:
            words.append(["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"][num - 1])
        else:
            words.append(["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"][num // 10 - 2])
            if (num % 10) > 0:
                words.append(num2words(num % 10))
    return " ".join(words)

# !!!WAR CRIME BELOW!!! 
# *DO NOT TRY THIS AT HOME*
print(f"""You are {num2words(input(f"Hi, {input('Enter your name: ')}! How old are you? "))} years old.""")

isEven = lambda x: x >> 1 << 1 == x
# print(isEven(22))
# print(isEven(25))

# maxnum = lambda x,y: x if x>y else y
# print(maxnum(22,25))

# print(f"The larger number is: {(lambda x,y: x if x>y else y)(input('Enter a number:'), input('Enter another number:'))}")

# Number to words function