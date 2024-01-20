"""
A marbles game with 3 players, Player 1, Player 2 and the Admin
It uses threading to play the game and utilizes the concept of locks along with classes
"""

import threading
import random
import time

available_marbles = 100
lock = threading.Lock()

class Player:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.marbles_collected = 0

    def collect_marbles(self):
        global available_marbles
        while True:
            lock.acquire()
            if available_marbles == 0:
                lock.release()
                break
            m = random.randint(1, 10)
            if available_marbles >= m:
                available_marbles -= m
                self.marbles_collected += m
                print(f"{self.name} collected {m} marbles")
                points = 2 if m % 2 == 0 else 1
                self.points += points
            else:
                lock.release()
                break
            lock.release()
            time.sleep(random.random())

    def getMarbles(self):
        return self.marbles_collected
    
    def getPoints(self):
        return self.points
    
    def getName(self):
        return self.name


class Admin:
    def __init__(self, players):
        self.players = players

    def run(self):
        while True:
            lock.acquire()
            if available_marbles == 0:
                lock.release()
                break
            else:
                print(f"Current Bucket size: {available_marbles}")
                max_points = max(p.getPoints() for p in self.players)
                winners = [p.getName() for p in self.players if p.getPoints == max_points]
                if len(winners) == 1:
                    print(f"Current Winner: {winners[0]}")
                else:
                    print(f"Tie between: {', '.join(winners)}")
            lock.release()


def main():
    global available_marbles
    n = int(input("Enter the bucket size: "))
    available_marbles = n

    p1 = Player("Player 1")
    p2 = Player("Player 2")
    players = [p1, p2]

    threads = []
    for p in players:
        t = threading.Thread(target=p.collect_marbles)
        threads.append(t)

    admin = Admin(players)
    admin_thread = threading.Thread(target=admin.run)
    threads.append(admin_thread)

    for t in threads:
        t.start()

    for t in threads:
        t.join()
    
    print("Game Over!")
    for p in players:
        print(f"{p.getName()} collected {p.getMarbles()} marbles and earned {p.getPoints()} points")


if __name__ == '__main__':
    main()
