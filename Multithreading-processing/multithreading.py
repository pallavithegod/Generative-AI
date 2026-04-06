import threading, time

# 1 CORE - MULTIPLE THREADS
def take_order():
    for i in range(1,4):
        print(f"taking order : {i}")
        time.sleep(4)


def make_order():
    for i in range(1,4):
        print(f"Making order : {i}")
        time.sleep(10)

# create thread
taking  = threading.Thread(target = take_order)
making = threading.Thread(target = make_order)

# start thread
taking.start()
# taking.join()          here, taking runs fully first, then only making starts
making.start()

taking.join()           # both happen simulaneously acc to time
making.join()

