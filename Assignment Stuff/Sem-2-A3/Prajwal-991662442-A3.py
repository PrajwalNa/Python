"""
Assignment No.: 3
Course: PROG23199
Student ID: 991662442
Student Name: Prajwal Nautiyal
Submission date: 16 April 2023
Instructor's name: Syed Tanbeer
------------------------------------------------------------------------------------------------------------------------
This program simulates a zoo feeding system. The zoo has 5 animals: Elephant, Giraffe, Zebra, Horse, and Deer.
This program uses a lock and a condition to control access to the zoo. The zoo begins with a balance of 0 units of food.
------------------------------------------------------------------------------------------------------------------------
"""

import threading
import random
import time

# Global variables
balance = 0
n = 0


# class Animal, which represents an animal in the zoo
class Animal:
    """
    Name
    --------------------
    Animal

    Description
    --------------------
    This class represents an animal in the zoo.

    Attributes
    --------------------
    name: str
        The name of the animal.
    food: int
        The amount of food the animal consumes per feeding.
    feedCount: int
        The number of times the animal has been fed, initialized to 0.
    timesHungry: int
        The number of times the animal has been hungry, initialized to 0.
    
    Methods
    --------------------
    getName()
        Returns the name of the animal.
    getFood()
        Returns the amount of food the animal consumes per feeding.
    getFeedCount()
        Returns the number of times the animal has been fed.
    getTimesHungry()
        Returns the number of times the animal has been hungry.
    addTimesHungry()
        Increments the number of times the animal has been hungry by 1.
    addFeedCount()  
        Increments the number of times the animal has been fed by 1.
    totalFoodConsumed()
        Returns the total amount of food consumed by the animal.
    """
    def __init__(self, name, food) -> None:
        """
        Name
        --------------------
        __init__

        Description
        --------------------
        This method initializes the Animal class.

        Parameters
        --------------------
        name: str
            The name of the animal.
        food: int
            The amount of food the animal consumes per feeding.
        """
        self.name = name
        self.food = food
        # feedCount and timesHungry are initialized to 0 and need not be passed as parameters
        self.feedCount = 0
        self.timesHungry = 0

    # accessor methods

    def getName(self) -> str:
        """
        Name
        --------------------
        getName

        Description
        --------------------
        This method returns the name of the animal.

        Parameters
        --------------------
        None

        Returns
        --------------------
        str
            The name of the animal.
        """
        return self.name

    def getFood(self) -> int:
        """
        Name
        --------------------
        getFood
        
        Description
        --------------------
        This method returns the amount of food the animal consumes per feeding.

        Parameters
        --------------------
        None

        Returns
        --------------------
        int
            The amount of food the animal consumes per feeding.
        """
        return self.food

    def getFeedCount(self) -> int:
        """
        Name
        --------------------
        getFeedCount
        
        Description
        --------------------
        This method returns the number of times the animal has been fed.
        
        Parameters
        --------------------
        None
        
        Returns
        --------------------
        int
            The number of times the animal has been fed.
        """
        return self.feedCount
    
    def getTimesHungry(self) -> int:
        """
        Name
        --------------------
        getTimesHungry
        
        Description
        --------------------
        This method returns the number of times the animal has been hungry.
        
        Parameters
        --------------------
        None
        
        Returns
        --------------------
        int
            The number of times the animal has been hungry.
        """
        return self.timesHungry
    
    # mutator methods

    def addTimesHungry(self) -> None:
        """
        Name
        --------------------
        addTimesHungry
        
        Description
        --------------------
        This method increments the number of times the animal has been hungry by 1.
        
        Parameters
        --------------------
        None
        
        Returns
        --------------------
        None
        """
        self.timesHungry += 1
    
    def addFeedCount(self) -> None:
        """
        Name
        --------------------
        addFeedCount
        
        Description
        --------------------
        This method increments the number of times the animal has been fed by 1.
        
        Parameters
        --------------------
        None
        
        Returns
        --------------------
        None
        """
        self.feedCount += 1

    # other methods

    def totalFoodConsumed(self) -> int:
        """
        Name
        --------------------
        totalFoodConsumed
        
        Description
        --------------------
        This method returns the total amount of food consumed by the animal.
        
        Parameters
        --------------------
        None
        
        Returns
        --------------------
        int
            The total amount of food consumed by the animal.
        """
        return self.feedCount * self.food


# feedAnimals function, which feeds the animals in the zoo
def feedAnimals(animals, zooLock: threading.Lock, zooCon: threading.Condition):
    """
    Name
    --------------------
    feedAnimals

    Description
    --------------------
    This function feeds the animals in the zoo.

    Parameters
    --------------------
    animals: list
        The list of animals in the zoo.
    zooLock: threading.Lock
        The lock used to control access to the zoo.
    zooCon: threading.Condition
        The condition used to control access to the zoo.

    Returns
    --------------------
    None
    """
    # declare global variables
    global n
    global balance
    # while there are animals to feed
    while n > 0:
        time.sleep(0.45)
        # using the condition object, wait until there is enough food to feed an animal
        with zooCon:
            # choose a random animal to feed
            currentAnimal = random.choice(animals)
            print(f'\n\033[38;5;51m{currentAnimal.getName()} is hungry.\033[0m')
            # increment the number of times the animal has been hungry
            currentAnimal.addTimesHungry()
            # while there is not enough food to feed the animal
            while balance < currentAnimal.getFood():
                print(f'\033[38;5;226mInsufficient Food. Waiting for delivery.\033[0m')
                # increment the number of times the animal has been hungry
                currentAnimal.addTimesHungry()
                # wait until there is enough food to feed the animal
                zooCon.wait()
            # acquire the lock to access the feed the animal
            zooLock.acquire()
            balance -= currentAnimal.getFood()
            # increment the number of times the animal has been fed
            currentAnimal.addFeedCount()
            print(f'\033[38;5;82m{currentAnimal.getName()} was fed {currentAnimal.getFood()} units of food, Feed Count: {currentAnimal.getFeedCount()}. Remaining food: {balance} units.\033[0m\n')
            # release the lock
            zooLock.release()
            # decrease the number of animals to feed by 1
            n -= 1


# Delivery function, which delivers food to the zoo
def Delivery(zooLock: threading.Lock, zooCon: threading.Condition):
    """
    Name
    --------------------
    Delivery

    Description
    --------------------
    This function delivers food to the zoo.

    Parameters
    --------------------
    zooLock: threading.Lock
        The lock used to control access to the zoo.
    zooCon: threading.Condition
        The condition used to control access to the zoo.

    Returns
    --------------------
    None
    """
    # declare global variables
    global n
    global balance
    # while there are animals to feed
    while n > 0:
        # using the condition object, add a random amount of food to the zoo
        time.sleep(0.5)
        with zooCon:
            amount = random.randint(1, 10)
            # acquire the lock to access the zoo
            zooLock.acquire()
            balance += amount
            print(f'\033[38;5;122mDelivery of {amount} units of food received. Total food: {balance} units.\033[0m')
            # release the lock
            zooLock.release()
            # notify all threads waiting on the condition object
            zooCon.notify_all()


# lambda functions

# function to get the user input for the number of animals to feed
usrIn = lambda: int(input('Enter the total number of animals to feed: '))
usrIn.__doc__ = """
    Name
    --------------------
    usrIn

    Description
    --------------------
    This function takes the user input for the number of animals to feed.

    Parameters
    --------------------
    None

    Returns
    --------------------
    int
        The number of animals to feed.
"""


# function to create the animal objects of the class Animal
createAnimals_Prajwal = lambda: [Animal(animal, food) for animal, food in {'Elephant': 15, 'Giraffe': 9, 'Horse': 5, 'Zebra': 5, 'Deer': 3}.items()]
createAnimals_Prajwal.__doc__ = """
    Name
    --------------------
    createAnimals_Prajwal

    Description
    --------------------
    This function creates the animals in the zoo.

    Parameters
    --------------------
    None

    Returns
    --------------------
    list
        The list of animal objects of the class Animal in the zoo.
"""


# function to get the name(s) if the animal(s) that has/have been hungry the most
getHungriest_Prajwal = lambda animals: [animal.getName() for animal in animals if animal.getTimesHungry() == max(animal.getTimesHungry() for animal in animals)]
getHungriest_Prajwal.__doc__ = """
    Name
    --------------------
    getHungriest_Prajwal

    Description
    --------------------
    This function returns the name of the hungriest animal in the zoo.

    Parameters
    --------------------
    animals: list
        The list of animal objects in the zoo.

    Returns
    --------------------
    list
        The list of the names of the hungriest animals in the zoo.
"""


# function to get the name(s) if the animal(s) that has/have consumed the most food
getHighestConsumers_Prajwal = lambda animals: [animal.getName() for animal in animals if animal.totalFoodConsumed() == max(animal.totalFoodConsumed() for animal in animals)]
getHighestConsumers_Prajwal.__doc__ = """
    Name
    --------------------
    getHighestConsumers_Prajwal

    Description
    --------------------
    This function returns the name of the animal that has consumed the most food in the zoo.

    Parameters
    --------------------
    animals: list
        The list of animal objects in the zoo.

    Returns
    --------------------
    list
        The list of the names of the animals that have consumed the most food in the zoo.
"""


# Main function
def main():
    """
    Name
    --------------------
    main

    Description
    --------------------
    This function is the main function of the program. \
    \nIt creates the animals in the zoo, creates the threads for the feeding and delivery tasks, and prints the results.

    Parameters
    --------------------
    None

    Returns
    --------------------
    None
    """
    # declare global variables
    global n
    # print the welcome message
    print('\033[48;5;51;38;5;0m\t\tWelcome to the Zoo Feeding System!\033[0m')
    print('\033[48;5;226;38;5;0m\t\tDeveloped By: Prajwal Nautiyal.\033[0m')
    print('\033[48;5;226;38;5;0m\t\tStudent #: 991662442\033[0m')
    # get the user input for the number of animals to feed
    n = usrIn()
    print('\033[48;5;82;38;5;0mStarting Zoo Feeding System...\033[0m\n')
    # create the condition object and the lock object
    zooCond = threading.Condition()
    zooLock = threading.Lock()
    # create the animals in the zoo
    animals = createAnimals_Prajwal()
    # create the threads for the feeding and delivery tasks
    feedTask = threading.Thread(target=feedAnimals, name='Feeding Task', args=(animals, zooLock, zooCond))
    deliveryTask = threading.Thread(target=Delivery, name='Delivery Task', args=(zooLock, zooCond))
    # start the threads and wait for them to finish
    feedTask.start()
    deliveryTask.start()
    feedTask.join()
    deliveryTask.join()
    # print the final report
    print('\n\033[48;5;122;38;5;0mFinal report:\033[0m')
    for animal in animals:
        print(f'\033[38;5;51m{animal.getName()} got hungry {animal.getTimesHungry()} times, was fed {animal.getFeedCount()} times and consumed {animal.totalFoodConsumed()} units of food.\033[0m')
    print(f'\033[38;5;192mThe hungriest animal: {", ".join(getHungriest_Prajwal(animals))}.')
    print(f'The animal(s) which consumed the most food: {", ".join(getHighestConsumers_Prajwal(animals))}.')
    print(f'The total food consumed by all animals: {sum(animal.totalFoodConsumed() for animal in animals)} units.\033[0m')


# call the main function
if __name__ == '__main__':
    main()