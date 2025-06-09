import threading
import time
import random

class DiningPhilosophers:
    def __init__(self, num_philosophers=5, eat_count=3):
        self.num_philosophers = num_philosophers
        self.eat_count = eat_count
        self.forks = [threading.Semaphore(1) for _ in range(num_philosophers)]
        self.waiter = threading.Semaphore(num_philosophers - 1)  # Avoid deadlock by allowing max (N-1) to eat
        self.philosopher_threads = []
    
    def philosopher(self, id):
        for _ in range(self.eat_count):
            self.think(id)
            self.hungry(id)
            self.eat(id)
    
    def think(self, id):
        print(f"Philosopher {id} is thinking.")
        time.sleep(random.randint(1, 3))
    
    def hungry(self, id):
        print(f"Philosopher {id} is hungry and trying to pick up forks.")
        
    def eat(self, id):
        left_fork = id
        right_fork = (id + 1) % self.num_philosophers
        
        if id % 2 == 0:  # Even philosophers pick left fork first
            first_fork, second_fork = left_fork, right_fork
        else:  # Odd philosophers pick right fork first
            first_fork, second_fork = right_fork, left_fork
        
        self.waiter.acquire()  # Limit number of philosophers trying to eat
        self.forks[first_fork].acquire()
        self.forks[second_fork].acquire()
        
        print(f"Philosopher {id} is eating.")
        time.sleep(random.randint(1, 3))
        print(f"Philosopher {id} has finished eating and is releasing forks.")
        
        self.forks[second_fork].release()
        self.forks[first_fork].release()
        self.waiter.release()
    
    def start_dining(self):
        for i in range(self.num_philosophers):
            t = threading.Thread(target=self.philosopher, args=(i,))
            self.philosopher_threads.append(t)
            t.start()
        
        for t in self.philosopher_threads:
            t.join()

if __name__ == "__main__":
    dining_philosophers = DiningPhilosophers()
    dining_philosophers.start_dining()
