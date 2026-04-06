from multiprocessing import Process
import time, os
import threading

def crunch_number():   #heavy math

    pid = os.getpid()           # to get current process name
    tid = threading.current_thread().name 
    
    print(f"Process : {pid}, {tid} starting calculation...")

    count = 0
    for _ in range(100_000_000):
        count += 1
    
    print(f"Process : {pid}, {tid} finished...")

if __name__ == "__main__":

    # SLOWER MULTITHREADING - won't run in parallel due to GIL
    # all have same process id (pid)
    thread1 = threading.Thread(target=crunch_number, name="thread-1")
    thread2 = threading.Thread(target=crunch_number, name="thread-2")
    start = time.time()
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
    end = time.time()

    print(f"Total time with multi-threading: {end - start:.2f} sec\n")

    # FASTER MULTIPROCESSING - GIL bypassed and many CPU cores used
    start = time.time()
    p1 = Process(target=crunch_number)
    p2 = Process(target=crunch_number)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    end = time.time()

    print(f"Total time with multi-processing: {end - start:.2f} sec")
