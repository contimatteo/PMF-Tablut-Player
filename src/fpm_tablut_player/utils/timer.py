import time


###


class Timer:
    start_time: float

    def __init__(self):
        self.start_time = None

    def start(self):
        if self.start_time is not None:
            raise Exception(f"Timer is running. Use .stop() to stop it")

        self.start_time = time.perf_counter()

        return self

    def stop(self):
        if self.start_time is None:
            raise Exception(f"Timer is not running. Use .start() to start it")

        self.start_time = None

        return self

    def get_elapsed_time(self) -> float:
        if self.start_time is None:
            raise Exception(f"Timer is not running. Use .start() to start it")

        return time.perf_counter() - self.start_time

    def get_time_left(self, threshold: float) -> float:
        return float(threshold) - self.get_elapsed_time()
