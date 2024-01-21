'''
Assignment No.: 2
Course: PROG23199
Student Name: Prajwal Nautiyal
Submission date: 2 April 2023
Instructor's name: Syed Tanbeer
------------------------------------------------------------------------------------------------------------------------
This program will read from the transactions and items file to populate the mysql database. 
Then perform operations on the database.
------------------------------------------------------------------------------------------------------------------------
ANSI Codes for colors used in this program:
    Red Background: \033[48;5;196m
    Green Background: \033[48;5;82m
    Yellow Background: \033[48;5;226m
    Cyan: \033[38;5;51m
    Clear: \033[0m
    Aqua: \033[48;5;122m

Error Codes:
    0: No error
    1: Table doesn't exist, Dependencies not satisfied
    2: File doesn't exist or is not in the same folder as the application
    3: SQL connection error
------------------------------------------------------------------------------------------------------------------------
'''
import os
import re
import csv
import sys
import time
import random
import mysql.connector

# function to print a loading bar with a cyan background
loading = lambda i: print(f"\r|\033[48;5;51m{'>' * (i * 25 // 100)}\033[0m{' ' * (25 - (i * 25 // 100))}|", end="") or time.sleep(0.01)

# function to get the username and password from the user
def userCredentials():
    try:
        username = input("\033[0mEnter your username: \033[38;5;51m")
        password = input("\033[0mEnter your password: \033[38;5;51m")
        database = input("\033[0mEnter the database name: \033[38;5;51m")
    except KeyboardInterrupt:
        print("\033[0m")
        print("\033[48;5;122mExiting...\033[0m")
        list(map(loading, range(101)))
        print("\n")
        sys.exit(0)
    return username, password, database

# function to connect to the database
def connectDatabase(username, password, database):
    # making the variables global so that they can be used in other functions
    global mydb, mycursor
    print("\033[0mConnecting to database...")
    # try to connect to the database, if it fails, ask for the username and password again
    try:
        # loading bar, using a map function to call the loading function 20 times and a list so that it actually shows the loading bar
        list(map(loading, range(101)))
        print("\n")     # new line to separate the loading bar from the next print statement
        mydb = mysql.connector.connect(host="localhost", user=username, password=password, database=database)
        print("\033[48;5;82mConnected to database successfully.\033[0m\n")
        mycursor = mydb.cursor()
        print("\033[48;5;82mCursor Initialised\033[0m\n")
    except Exception as e:
        print(f"\033[48;5;196m{e}\n\n\033[48;5;226mPlease try again.\033[0m\n")
        username, password, database = userCredentials()
        connectDatabase(username, password, database)


# function to fill the database with the data from the items_{firstName}.csv file
class items_user:
    # Initialising the class with the firstName of the user, the table name and the file name
    def __init__(self, firstName):
        self.firstName = firstName
        self.tableName = f"items_{firstName}"
        self.fileName = f"Items_{firstName}.csv"
        # try to get the data from the table, if it fails, it means the table doesn't exist, send a message to the user
        try:
            mycursor.execute(f"SELECT * FROM {self.tableName};")
            self.myresult = mycursor.fetchall()
        except Exception as e:
            print(f"\033[48;5;196m{e}\033[0m\n")
            print(f"\033[48;5;226mPlease satisfy the dependencies before running the Program!\033[0m\n")
            sys.exit(1)
    
    # function to populate the table with the data from the csv file
    def __populate_table(self):
        # get the path of the file, os.path.dirname(os.path.abspath(__file__)) gets the path to the python file, then add the file name to it
        filePath = os.path.dirname(os.path.abspath(__file__)) + "\\" + self.fileName
        # try to open the file, if it fails, send a message to the user and exit the program
        try:
            reader = csv.DictReader(open(filePath))
        except FileNotFoundError:
            print(f"\033[48;5;196mFile {self.fileName} not found.\033[0m\n")
            print(f"\033[48;5;226mPlease make sure the file: '{self.fileName}', is in the same folder as the application before running the Program!\033[0m\n")
            sys.exit(2)
        for row in reader:
            row['iid'] = int(row['iid'])        # convert the iid to an integer
            row['price'] = float(row['price'])  # convert the price to a float
            # insert the data into the table
            mycursor.execute(f"INSERT INTO {self.tableName} (iid, name, category, price) \
                             VALUES ({row['iid']}, '{row['name']}', '{row['category']}', {row['price']});")
        mydb.commit()
        print(f"\033[48;5;82mTable '{self.tableName}' populated successfully.\033[0m\n")

    def __call__(self):
        # check if the table is empty, populate it or send the appropriate message
        if len(self.myresult) == 0:
            self.__populate_table()
        else:
            print(f"\033[48;5;226mTable {self.tableName} already exists and is populated.\033[0m\n")
            reset = input(f"\033[48;5;122mWould you like to repopulate the table? (y/n)\033[0m\n").lower()
            if reset == "y":
                mycursor.execute(f"TRUNCATE {self.tableName};")
                self.__populate_table()

    # function to return the total sales for a given category with a sql query
    # def category_sales(self, category):
    #     mycursor.execute(f"SELECT name, SUM(price * transactions.quantity) as sales \
    #                      FROM {self.tableName} JOIN transactions ON {self.tableName}.iid = transactions.iid\
    #                      WHERE {self.tableName}.category = '{category}' GROUP BY items_prajwal.iid;")
    #     myresult = mycursor.fetchall()
    #     print(f"\033[48;5;82mTotal sales for {category} is {myresult[0][0]}\033[0m")
    #     return myresult[0][0]
    
    # a function to return a dictionary of the items after fetching them from the database
    def dict_of_items(self):
        mycursor.execute(f"SELECT * FROM {self.tableName};")
        myresult = mycursor.fetchall()
        mydict = {}
        for row in myresult:
            # the key is the iid and the value is a tuple of the other attributes
            mydict[row[0]] = row[1:]
        return mydict

class transactions:
    # Initialising the class with the firstName of the user, the table name and the file name
    def __init__(self, firstName):
        self.firstName = firstName
        self.tableName = "Transactions"
        self.fileName = f"Transactions.txt"
        # try to get the data from the table, if it fails, it means the table doesn't exist, send a message to the user
        try:
            mycursor.execute(f"SELECT * FROM {self.tableName};")
            self.myresult = mycursor.fetchall()
        except Exception as e:
            print(f"\033[48;5;196m{e}\033[0m\n")
            print(f"\033[48;5;226mPlease satisfy the dependencies before running the Program!\033[0m\n")
            sys.exit(1)
    
    # function to populate the table with the data from the text file
    def __populate_table(self):
        # get the path of the file, os.path.dirname(os.path.abspath(__file__)) gets the path to the python file, then add the file name to it
        filePath = os.path.dirname(os.path.abspath(__file__)) + "\\" + self.fileName
        # try to open the file, if it fails, send a message to the user and exit the program
        try:
            transactionsFile = open(filePath, "r")
        except FileNotFoundError:
            print(f"\033[48;5;196mFile {self.fileName} not found.\033[0m\n")
            print(f"\033[48;5;226mPlease make sure the file: '{self.fileName}', is in the same folder as the application before running the Program!\033[0m\n")
            sys.exit(2)
        reader = transactionsFile.readlines()   # read all the lines in the file and store them in a list
        transactionsFile.close()                # close the file
        # remove the first two lines from the list
        reader.pop(0)
        reader.pop(0)
        for line in reader:
            line = line.strip()
            # if the line is empty, break the loop
            if len(line) == 0:
                break
            else:
                line = line.split(" ")          # split the line into a list of strings
                line = [int(i) for i in line]   # convert the strings to integers
                # insert the data into the table
                mycursor.execute(f"INSERT INTO {self.tableName} (transaction_id, iid, quantity) \
                                VALUES ({line[0]}, {line[1]}, {line[2]});")
        mydb.commit()
        print(f"\033[48;5;82mTable '{self.tableName}' populated successfully.\033[0m\n")

    # function to return the total sales for a given category with a sql query
    # def TotalSales(self):
    #     mycursor.execute(f"select sum(price*{self.tableName}.quantity) as TotalSales \
    #                      from items_{self.firstName} join transactions on items_{self.firstName}.iid = {self.tableName}.iid;")
    #     myresult = mycursor.fetchall()
    #     print(f"\033[48;5;122mTotal sales for {self.firstName}'s Store is {myresult[0][0]}\033[0m")

    def __call__(self):
        # check if the table is empty, populate it or send the appropriate message
        if len(self.myresult) == 0:
            self.__populate_table()
        else:
            print(f"\033[48;5;226mTable {self.tableName} already exists and is populated.\033[0m\n")
            reset = input(f"\033[48;5;122mWould you like to repopulate the table? (y/n)\033[0m\n").lower()
            if reset == "y":
                mycursor.execute(f"TRUNCATE {self.tableName};")
                self.__populate_table()

    # a function to return a dictionary of the transactions after fetching them from the database
    def dict_of_transactions(self):
        mycursor.execute(f"SELECT * FROM {self.tableName};")
        myresult = mycursor.fetchall()
        mydict = {}
        for row in myresult:
            mydict[row[0]] = (row[1:])
        return mydict

# function to create the tables for the total sales of an item by category
def CategoryTables():
    # a list of the categories
    categories = ["Fruit", "Vegetables", "Dairy", "Meat", "Snacks"]
    # check for the tables that exist
    mycursor.execute("Show Tables;")
    result = mycursor.fetchall()
    # searching for 'categorytotal_' prefix in the result to check if the tables exist
    if re.search( r"categorytotal_",str(result)):
        print("\033[48;5;226mCategory Totals Tables already exist.\033[0m\n")
        reset = input(f"\033[48;5;122mWould you like to reset the tables? (y/n)\033[0m\n").lower()
        if reset == "y":
            for i in categories: mycursor.execute(f"TRUNCATE categorytotal_{i};")
    else:
        # a query to create the tables, since all the tables have the same structure, we can use the same query for all the tables
        sql = """CREATE TABLE IF NOT EXISTS CategoryTotal_{}(
        ItemID int primary key,
        Item varchar(255) not null,
        Amount float not null
        );"""
        print("\033[48;5;122mCreating Category Totals Tables...\033[0m")
        list(map(loading, range(101)))
        print("\n")
        # execute the queries
        for name in categories:
            # use the format method to insert the name of the category in the query
            mycursor.execute(sql.format(name))
        mydb.commit()
        print("\033[48;5;82mCategory Totals Tables created successfully.\033[0m\n")

# function to combine the multiple entries with the same iid in the transactions dictionary
def checkDuplicate(sortedList):
    newList = []
    currentID = None
    currentQuant = 0
    # loop through the sorted list of tuples and combine the tuples with the same iid
    for tupl in sortedList:
        # unpack the tuple
        iid, quantity = tupl
        # check if the current tuple is the first one, if it is, assign the values to the currentID and currentQuant
        if currentID is None:
            currentID = iid
            currentQuant = quantity
        # check if the current tuple has the same iid as the previous one, if it does, add the quantity to the currentQuant
        elif iid == currentID:
            currentQuant += quantity
        # if the current tuple has a different iid, 
        # add the previous tuple to the new list and assign the values of the current tuple to the currentID and currentQuant
        else:
            newList.append((currentID, currentQuant))
            currentID = iid
            currentQuant = quantity
    # Add the last combined tuple
    newList.append((currentID, currentQuant))
    return newList


# function to fill the all the tables with the data
def fillTables():
    # create the global dictionaries to use them in the function
    global itemDict
    global transactDict
    # get the first name from the user to use it in the table names and get the data from the correct file
    firstName = input("\033[0mEnter your first name: \033[38;5;51m").capitalize()
    # check if the name is valid, else ask the user to enter the name again
    if not re.match(r"^[a-zA-Z]+$", firstName):
        print("\033[48;5;196mInvalid name. Please try again.\033[0m")
        fillTables()
    else:
        # create the table objects
        items_obj = items_user(firstName)
        transcations_obj = transactions(firstName)
        print(f"\n\033[48;5;122mFilling values in items_{firstName} table for {firstName}...\033[0m")
        list(map(loading, range(101)))
        print("\n")
        # call the objects to fill the table items_{firstName}
        items_obj()
        print(f"\033[48;5;122mFilling values in Transactions table...\033[0m")
        list(map(loading, range(101)))
        print("\n")
        # call the object to fill the table Transactions
        transcations_obj()
        print(f"\033[48;5;122mFilling values in CategoryTotal tables...\033[0m")
        list(map(loading, range(101)))
        print("\n")
        # get the dictionaries from the objects
        itemDict = items_obj.dict_of_items()
        transactDict = transcations_obj.dict_of_transactions()
        cat = ["Dairy", "Fruit", "Meat", "Snacks", "Vegetables"]
        # run a query to get the data from a random categorytotal table
        mycursor.execute(f"SELECT * FROM CategoryTotal_{random.choice(cat)};")
        res = mycursor.fetchall()
        # check if the table is empty, if it is, fill it with the data
        if not len(res) == 0:
            print("\033[48;5;226mCategoryTotal tables already filled.\033[0m\n")
        else:
            # sort the values from the transactions dictionary by the iid
            value = sorted(transactDict.values(), key=lambda x: x[0])
            # call the function to combine the tuples with the same iid
            sorted_list = checkDuplicate(value)
            # a query structure to fill the tables
            sql = "INSERT INTO CategoryTotal_{} (ItemID, Item, Amount) VALUES ({}, '{}', {});"
            for key, valu in sorted_list:
                # get the attributes of the item from the items dictionary
                val = itemDict[key]
                # check the category of the item and fill the table with the data using the format method
                match val[1]:
                    case "Dairy":
                        mycursor.execute(sql.format(val[1], key, val[0], val[2]*valu))
                    case "Fruit":
                        mycursor.execute(sql.format(val[1], key, val[0], val[2]*valu))
                    case "Meat":
                        mycursor.execute(sql.format(val[1], key, val[0], val[2]*valu))
                    case "Snacks":
                        mycursor.execute(sql.format(val[1], key, val[0], val[2]*valu))
                    case "Vegetables":
                        mycursor.execute(sql.format(val[1], key, val[0], val[2]*valu))
            print(f"\033[48;5;82mCategoryTotal tables filled successfully.\033[0m\n")
        mydb.commit()

# function to fetch the data from the of a certain category from its respective table
def getCat_Total():
    cat = ["Dairy", "Fruit", "Meat", "Snacks", "Vegetables"]
    category = input(f"\n\033[0mThe Categories are {cat}\nEnter the category: \033[38;5;51m").capitalize()
    if not category in cat:
        print("\033[48;5;196mInvalid category. Please try again.\033[0m\n")
        getCat_Total()
    else:
        print("\033[48;5;122mGetting Category Totals...\033[0m")
        list(map(loading, range(101)))
        print("\n")
        mycursor.execute(f"SELECT * FROM CategoryTotal_{category};")
        myresult = mycursor.fetchall()
        print(f"Category Totals for {category}")
        print(f"\033[48;5;122m{'ItemID':<10}|{'Item':<20}|{'Amount (CA$)':<15}|\033[0m")
        for row in myresult:
            print(f"{row[0]:<10}|{row[1]:<20}|{row[2]:<15}|")

# function to calculate the total sales from the data retrieved from the items_{firstName} & transactions tables
def TotalSales():
    # sum variable to store the total sales
    total = 0
    # sort the values from the transactions dictionary by the iid and call the function to combine the tuples with the same iid
    val = sorted(transactDict.values(), key=lambda x: x[0])
    sorted_list = checkDuplicate(val)
    # loop through the sorted list and get the total sales by adding the sum to the product of the price and the quantity of each item
    for value in sorted_list:
        total += itemDict[value[0]][2]*value[1]
    print("\033[48;5;122mGetting Total Sales...\033[0m")
    list(map(loading, range(101)))
    print("\n")
    print(f"\033[38;5;122mTotal Sales: CA$ {total}\033[0m")

# function to get the items that sold more than 3 quantities and print them along with their total sales
def quantGE3():
    print("\033[48;5;122mGetting items with quantity > 3...\033[0m")
    list(map(loading, range(101)))
    print("\n")
    # the header of the table
    print(f"\033[48;5;122m{'ItemID':<10}|{'Item':<20}|{'Transaction ID':<20}|{'Quantity':<15}|{'Sale (CA$)':<15}|\033[0m")
    # Loop through the transactions dictionary and check if the quantity is greater than 3
    for key, value in transactDict.items():
        if value[1] > 3:
            # get the attributes of the item from the items dictionary
            val = itemDict[value[0]]
            # print the data of the item
            print(f"{value[0]:<10}|{val[0]:<20}|{key:<20}|{value[1]:<15}|{val[2]*value[1]:<15}|")

# function to allow the user to send a custom query to the database
def customQuery():
    sql = input("\n\033[0mEnter your query: \033[38;5;51m").lower()
    # check if the query is a select query and if it is related to the items table
    if re.search(r"select.*items_", sql) == None:
        print("\033[48;5;196mInvalid query. Please try again.\033[0m")
        print(f"\033[48;5;122mYou are only allowed to send queries related to retrieving data from the items table.\033[0m\n")
        customQuery()
    else:
        print("\033[48;5;122mGetting results...\033[0m")
        list(map(loading, range(101)))
        print("\n")
        # check if the query ends with a semicolon and add it if it doesn't
        if sql.find(";") == -1:
            sql += ";"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        # get the column names of the result from the cursor object
        cols = mycursor.column_names
        # print the column names
        for col in cols:
            print(f"\033[48;5;122m{col:<15}|", end="")
        print("\033[0m")
        # print the result
        for line in myresult:
            for item in line:
                print(f"{str(item):<15}|", end="")
            # new line for seperating the rows
            print()
        print()

def main():
    user, passwd, dB = userCredentials()
    # try to connect to the database and if it fails, print the error and exit the program
    try:
        connectDatabase(user, passwd, dB)
    except Exception as e:
        print(f"\033[48;5;196mError: {e}\033[0m")
        sys.exit(3)
    CategoryTables()
    fillTables()
    # loop to keep the program running until the user chooses to exit
    while True:
        # print the menu
        print("\n\033[38;5;122m 1. Get Category Totals\n 2. Get Total Sales\n 3. Get items with quantity > 3\n 4. Custom Query\n 5. Exit\033[0m\n")
        # if the user enters a non-integer value, print an error message and continue the loop
        try:
            choice = int(input("\033[0mEnter your choice: \033[38;5;51m"))
        except ValueError:
            print("\033[48;5;196mIlleagl Value Entered!!. Please try again.\033[0m\n")
            continue
        match choice:
            case 1:
                getCat_Total()
            case 2:
                TotalSales()
            case 3:
                quantGE3()
            case 4:
                # try to execute the custom query and if it fails, print the error message from sql
                try:
                    customQuery()
                except Exception as e:
                    print(f"\033[48;5;196mError: {e}\033[0m")
            case 5:
                print("\033[48;5;122mExiting...\033[0m")
                list(map(loading, range(101)))
                print("\n")
                mydb.close()    # close the database connection in case the user exits the program using the menu
                sys.exit(0)
            case _:
                print("\033[48;5;196mInvalid choice. Please try again.\033[0m\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\033[48;5;122mExiting...\033[0m")
        list(map(loading, range(101)))
        print("\n")
        mydb.close()            # close the database connection in case the user exits the program using ctrl+c
        sys.exit(0)