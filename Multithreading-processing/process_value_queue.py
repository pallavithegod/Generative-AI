from multiprocessing import Process, Value, Queue

def increment(counter):
    for _ in range(100000):
        with counter.get_lock():           # no need to make lock explicitely
            counter.value += 1


if __name__ == "__main__":
    counter = Value('i', 0)        # initial - 0 assigned to i

    # 4 processes will be geting their mutual lock - sharing the value of counter 
    processes = [Process(target=increment, args=(counter, )) for _ in range(4)]
    [p.start() for p in processes]
    [p.join() for p in processes]

    print("Final counter value: ",counter.value )


    how_lock_works = ''' When a process executes with counter.get_lock():

    It grabs a "key." If another process already has the key, the current process stops and waits (blocks).

    While holding the key, it performs the Read -> Increment -> Write cycle.

    Once the with block ends, it "drops" the key for the next process to grab.

    '''