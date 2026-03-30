import threading

counter = 0
lock = threading.Lock()

def increament():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1

# running increment() 10 times 
threads = [threading.Thread(target=increament) for _ in range(10)]

[t.start() for t in threads]

[t.join() for t in threads]

print(f"Final counter: {counter}")