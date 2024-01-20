'''
Dev: Prajwal Nautiyal
Date: 31 March 2023
Course: PROG23199 - Python Programming
Instructor: Syed Tanbeer
Description: A Marbles Game with 3 players, Player 1, Player 2 and the Admin. It uses threading to play the game.
'''

import threading
import random

# Global Variables
# available_marbles = 100
lock = threading.Lock()

# Function to check if a number is even, it uses bitwise operators to check if the number is even
isEven = lambda x: x >> 1 << 1 == x

class Player(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.marbles_collected = 0
        self.points_earned = 0
        
    def run(self):
        global available_marbles
        while True:
            lock.acquire() # acquire lock
            # get a random number between 1 and 10
            m = random.randint(1, 10)
            # check if the number of marbles in the bucket is greater than or equal to the number of marbles collected by the player
            if available_marbles >= m and available_marbles > 0:
                available_marbles -= m # subtract the number of marbles collected by the player from the bucket
                print(f"{self.name} collected {m} marbles")
                lock.release() # release lock
                self.marbles_collected += m # add the number of marbles collected by the player to the total number of marbles collected by the player
                if isEven(m): # check if the number of marbles collected by the player is even and add the appropriate number of points to the player
                    self.points_earned += 2
                else:
                    self.points_earned += 1
            else:   # if the number of marbles in the bucket is less than the number of marbles collected by the player
                lock.release()
                break
    
    # getters for the number of marbles collected and the number of points earned by the player

    def getMarbles(self):
        return self.marbles_collected
    
    def getPoints(self):
        return self.points_earned

class Admin(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    # run method for the admin thread    
    def run(self):
        global available_marbles
        p1_points = 0
        p2_points = 0
        while True:
            lock.acquire()
            # check if the number of marbles in the bucket is less than or equal to 0
            if available_marbles == 0:
                # if the number of marbles in the bucket is less than or equal to 0, then the game is over
                lock.release()
                break
            lock.release()
            # get the number of points earned by the players
            p1_points = player1.getPoints()
            p2_points = player2.getPoints()
            # print the current status of the game
            lock.acquire()
            if p1_points > p2_points:
                print("\n\033[48;5;82mCurrent winner: Player 1\033[0m")
            elif p2_points > p1_points:
                print("\n\033[48;5;82mCurrent winner: Player 2\033[0m")
            else:
                print("\n\033[48;5;226mCurrent winner: Tie\033[0m")
            print(f"\033[48;5;122mCurrent bucket size: {available_marbles}\033[0m\n")
            lock.release()

def userInput():
    # get the number of marbles from the user
    N = int(input("Enter the number of marbles in the bucket: "))
    return N

if __name__ == "__main__":
    # get the number of marbles from the user
    global available_marbles 
    available_marbles = userInput()
    # create player threads
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    i = 0
    # create admin thread
    admin = Admin()
    print(f"\033[48;5;122m{'-'*20}Game started{'-'*20}\033[0m")
    # start all threads
    player1.start()
    player2.start()
    admin.start()
    # wait for all threads to finish
    player1.join()
    player2.join()
    admin.join()

    # print summary
    print(f"\033[48;5;122m{'-'*20}Game finished{'-'*20}\033[0m")
    print(f"Player 1 collected {player1.getMarbles()} marbles and earned {player1.getPoints()} points")
    print(f"Player 2 collected {player2.getMarbles()} marbles and earned {player2.getPoints()} points")