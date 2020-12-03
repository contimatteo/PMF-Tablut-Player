import time
from multiprocessing import Process, Queue
import numpy as np

from fpm_tablut_player.utils import Timer

###

TIMEOUT = 5.0

###


def get_moves() -> list:
    return np.linspace(1, 50, 50)


def my_function(index, thread_count, queue):
    print(" >> [{}] Thread >> starting".format(index))
    timer = Timer().start()
    #
    moves = np.array_split(get_moves(), thread_count)[index]
    print(" >> [{}] Thread >> moves = {}".format(index, moves))
    while True:
        time.sleep(1)
        elapsed_time = timer.get_elapsed_time()
        time_left = timer.get_time_left(TIMEOUT)
        if time_left > 0:
            print(" >> [{}] Thread >> elapsed_time = {:.2f}".format(index, elapsed_time))
        else:
            break
    #
    print(" >> [{}] Thread >> ending".format(index))
    queue.put(moves)


def multithread(threads: int = 1):
    print(" >> ")
    print(" >> ")

    jobs = []
    queue = Queue()

    # params
    indexes = np.linspace(0, threads-1, threads, dtype=np.int)
    indexes = indexes.tolist()

    #
    for i in range(5):
        p = Process(target=my_function, args=(indexes[i], threads, queue))
        jobs.append(p)
        p.start()
    for j in jobs:
        j.join()

    print(" >> ")
    # print(" >> Results = {} ".format(list(queue)))
    while not queue.empty():
        print(" >> Result = {} ".format(queue.get()))
    print(" >> ")

    # Close the pool and wait for the work to finish
    print(" >> ")
    print(" >> ")


###


if __name__ == "__main__":
    multithread(5)
