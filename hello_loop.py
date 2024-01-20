from time import sleep


temp = ""
for c in "Hello World":         # Printing a new line to pass control to the next row
    temp += c                   # Adding the character to the temporary string
    print(f"\r\033[1;3m{temp}", end="")                 # Printing the temporary strings
    sleep(0.08)
    
print("\033[22;23m")                # Resetting the terminal color
# temp = "abcd"
# temp.upper()
# print(temp)