import time
import numpy as np

from multiprocessing.dummy import Pool as ThreadPool
from fpm_tablut_player.utils import Timer

###

TIMEOUT = 5.0

###

def get_moves() -> list:
    return np.linspace(1, 50, 50)

def my_function(params: tuple):
    index, thread_count = params
    #
    print(" >> [{}] Thread >> starting".format(index))
    timer = Timer().start()
    #
    moves = np.array_split(get_moves(), thread_count)[index]
    print(" >> [{}] Thread >> moves = {}".format(index, moves))
    # while True:
    #     time.sleep(1)
    #     elapsed_time = timer.get_elapsed_time()
    #     time_left = timer.get_time_left(TIMEOUT)
    #     if time_left > 0:
    #         print(" >> [{}] Thread >> elapsed_time = {:.2f}".format(index, elapsed_time))
    #     else:
    #         break
    #
    print(" >> [{}] Thread >> ending".format(index))
    return index


def multithread(threads: int = 1):
    print(" >> ")
    print(" >> ")
    # Make the Pool of workers
    pool = ThreadPool(threads)

    # params
    indexes = np.linspace(0, threads-1, threads, dtype=np.int)
    indexes = indexes.tolist()
    threads_count = np.repeat(threads, threads)
    print(" >> indexes = {} ".format(indexes))
    print(" >> threads_count = {} ".format(threads_count))

    #
    results = pool.map(my_function, zip(indexes, threads_count))

    print(" >> ")
    print(" >> Results = {} ".format(results))
    print(" >> ")

    # Close the pool and wait for the work to finish
    pool.close()
    pool.join()
    print(" >> ")
    print(" >> ")


###


if __name__ == "__main__":
    multithread(5)
