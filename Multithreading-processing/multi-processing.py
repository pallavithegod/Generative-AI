import time
from multiprocessing import Process 

# MANY CORE - SIMULTANEOUS EXECUTION
def prepare_order(value):
  
    print(f"Take : {value}")
    time.sleep(3)
    print(f"Make : {value}")

# Prevents child processes from accidentally running the main code again in an infinite loop.
if __name__ == "__main__": 

    # List Comprehension
    prepare = [
        Process(target = prepare_order, args = (f"Order {i}", ))       # passing a tuple to append in prepare list
        for i in range(1,4)
    ]
    # start all processes
    for i in prepare:
        i.start()
        # i.join()             TAKE1 --(wait)--> MAKE1 ->TAKE2 --(wait)--> MAKE2 ->TAKE3

    # runs next line only after all processes are complete
    for i in prepare:
        i.join()

    print("\nAll orders prepared")