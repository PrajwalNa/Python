import threading
import time
import random

my_lock = threading.Lock()

class MyThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        print_time(self.name, self.counter, 5)
        print("Exiting " + self.name)

# Without Lock
# def print_time(threadName, delay, counter):
#     while counter:
#         time.sleep(delay)
#         print(threadName, time.ctime(time.time()))
#         counter -= 1

# With Lock
def print_time(threadName, delay, counter): 
    while counter:
        time.sleep(delay)
        my_lock.acquire()
        print(threadName, time.ctime(time.time()))
        print("Locked? ", my_lock.locked())
        counter -= 1
        if my_lock.locked:
            time.sleep(5)
            my_lock.release()
            print("Locked? ", my_lock.locked())

def main():
    # Create new threads
    thread1 = MyThread(1, "Thread-1", random.randint(1,100))
    thread2 = MyThread(2, "Thread-2", random.randint(1,100))

    # Start new Threads
    thread1.start()
    thread2.start()

    # Closing the threads
    thread1.join()
    thread2.join()
    print(thread1.is_alive(), thread2.is_alive())
    print("Exiting Main Thread")

main()