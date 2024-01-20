"""
Dev: Prajwal Nautiyal
Last Update: 11 April 2023
A simple program to convert a date from dd/mm/yyyy format to dd monthname yyyy format.
"""

import time

class DateConvert:
    """
    Description
    ------------
    This class is used to convert a date from dd/mm/yyyy format to dd monthname, yyyy format.
    
    Attributes
    ------------
    date: list[str]
        The date in the format of 'dd/mm/yyyy' as a list of strings.

    day: str
        The day in the format of 'dd' as a string.

    month: str
        The month in the format of 'mm' as a string, or the month name as a string.

    year: str
        The year in the format of 'yyyy' as a string.

    Methods
    ------------
    __init__(self, date = "0/00/0000")

    getVar(self, __name: str) -> str|list[str]

    setVar(self, __name: str, __value)

    __postinit(self)

    datein(self)

    __name(self)

    __validate(self) -> bool

    assignDate(self)
    """
    def __init__(self, date = '0/00/0000'):     # Initialising the class
        self.__date = date.split("/")           # Splitting the date into a list
        self.__day = self.__date[0]             # Setting the day as the first element of the list
        self.__month = self.__date[1]           # Setting the month as the second element of the list
        self.__year = self.__date[2]            # Setting the year as the third element of the list

    def getVar(self, __name: str) -> str|list[str]:
        """
        Description
        ------------
        This method returns the value of the class variable as a string or a list of strings.
        \nIt runs the name of the class variable through a match statement to get the appropriate value.

        Parameters
        ------------
        __name: str
            The name of the class variable.

        Returns
        ------------
        date: list[str]
            The date in the format of 'dd/mm/yyyy' as a string or a list of strings.

        day: str
            The day in the format of 'dd' as a string.

        month: str
            The month in the format of 'mm' as a string.

        year: str
            The year in the format of 'yyyy' as a string.
        """
        match __name:
            case "date":
                return self.__date
            case "day":
                return self.__day
            case "month":
                return self.__month
            case "year":
                return self.__year
            case _:
                return "Unknown Attribute"
            
    def setVar(self, __name: str, __value):
        """
        Description
        ------------
        This method sets the value of the class variable as a string or a list of strings.
        \nIt runs the name of the class variable through a match statement to set the appropriate value.

        Parameters
        ------------
        __name: str
            The name of the class variable.

        __value
            The value to be set to the class variable.
        """
        match __name:
            case "date":
                self.__date = __value
            case "day":
                self.__day = __value
            case "month":
                self.__month = __value
            case "year":
                self.__year = __value
            case _:
                print("Unknown Attribute")

    def __postinit(self):
        """
        Description
        ------------
        This method is called after the user input is taken and the date is split into a list.
        \nIt sets the class variables as the respective elements of the list.
        """
        self.setVar("day", self.getVar("date")[0])
        self.setVar("month", self.getVar("date")[1])
        self.setVar("year", self.getVar("date")[2])
        
    def datein(self):                           # User Input function to given instructions to the user on the format of input
        """
        Description
        ------------
        This method takes the input from the user and sets the class variable as a split list of the input.
        \nThe input is taken in the format of dd/mm/yyyy and is split into a list.
        \nThe function also handles the exception if the user enters a wrong format.
        """
        try:
            date = str(input("Enter a date[dd/mm/yyyy]: ")).split("/")
            self.setVar("date", date)
            self.__postinit()
        except IndexError:                      # If the user enters a date in a wrong format
            print("\033[91m!!Invalid Entry!!\033[00m\n")

    def __name(self):                       # Function to convert the month number into month name
        """
        Description
        ------------
        This runs the month number through a match statement to get the appropriate month name.
        \nAnd if the month number is invalid, it returns an error message.
        """
        match self.getVar('month'):
            case "01": self.setVar("month", "January")
            case "02": self.setVar("month", "February")
            case "03": self.setVar("month", "March")
            case "04": self.setVar("month", "April")
            case "05": self.setVar("month", "May")
            case "06": self.setVar("month", "June")
            case "07": self.setVar("month", "July")
            case "08": self.setVar("month", "August")
            case "09": self.setVar("month", "September")
            case "10": self.setVar("month", "October")
            case "11": self.setVar("month", "November")
            case "12": self.setVar("month", "December")
            case _: self.setVar("month", "Invalid Month")

    def __validate(self) -> bool:               # Validating the Input, took the list as argument
        """
        Description
        ------------
        This method returns a boolean value.
        \nThe function checks if the date is valid or not by checking the month and the date. The function also checks if the year is a leap year or not.
        \nThe function calls the name function to convert the month number into month name. Then it checks if the month is in the list of months with 31 days, 30 days for the respective months or 28/29 days for February.
        It takes no arguments.

        Returns
        ------------
        True: bool
            If the date is valid.
        False: bool
            If the date is invalid.
        """
        self.__name()                           # Assigning the month name to a variable
        # Checking if the month is in the list of months with 31 days
        if self.getVar('month') in  ['January', 'March', 'May', 'July', 'August', 'October', 'December']:
            if int(str(self.getVar('day'))) in range(1,32):      # Checking if the date is valid or not for the respective months
                return True
        # Checking if the month is February
        elif self.getVar('month') == 'February':
            if int(str(self.getVar('year')))%4 == 0:              # Checking if the year is a leap year
                if int(str(self.getVar('day'))) in range(1,30):  # Checking if the date is valid or not for a leap year february
                    return True
            elif int(str(self.getVar('day'))) in range(1,29):    # Checking if the date is valid or not for a non-leap year february
                return True
        # Checking if the month is in the list of months with 30 days
        elif self.getVar('month') in ['April', 'June', 'September', 'November']:
            if int(str(self.getVar('day'))) in range(1,31):      # Checking if the date is valid or not for the respective months
                return True
        return False
                    
    def assignDate(self):                # Converting the date into a different format
        """
        Description
        ------------
        This method returns a string of the date in the format of dd monthname, yyyy. It takes no arguments.

        Returns
        ------------
        date: str
            The date in the format of 'dd' as a string.
        month: str
            The month name in the format of 'monthname' as a string.
        year: str
            The year in the format of 'yyyy' as a string.
        The function returns the date, month and year in the format of dd monthname, yyyy. 
        If the date is invalid, it returns an error message.
        """
        if self.__validate():
            # Assigning values of date month and year into respectuve variables
            day = self.getVar('day')
            monthName = self.getVar('month')
            year = self.getVar('year')
            return  f'{day} {monthName}, {year}'
        else:
            return "Invalid Date!!"

loading = lambda i: print(f"\r|\033[48;5;51;38;5;0m{'>' * (i * 25 // 100)}\033[0m{' ' * (25 - (i * 25 // 100))}|", end="") or time.sleep(0.01)

def main():
    """
    Description
    ------------
    This is the main function of the program.
    \nIt creates an object of the Date class and calls the datein function to take the input from the user.
    \nIt then calls the assign function to convert the date into a different format and prints the result.
    """
    dateObj = DateConvert()
    dateObj.datein()
    list(map(loading, range(101)))
    print()
    print(dateObj.assignDate())

if __name__ == "__main__":
    main()