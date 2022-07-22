import time, threading, math

from table import Table
from path import Path

class Client(Table, Path):

    __id: int
    __is_walking: bool

    def __init__(self, x_min, x_max, y_min, y_max, rand_seed, id):
        Table.__init__(self)
        Path.__init__(self, x_min, x_max, y_min, y_max, rand_seed)
        self.__id = id
        self.__is_walking = False

    def __eq__(self, other):
        return self.__id == other.get_id()

    def start_walking(self, step):
        def target():
            self.__is_walking = True
            while self.__is_walking:
                self._step()
                time.sleep(step)

        self.__thread = threading.Thread(target=target)
        self.__thread.start()

    def stop_walking(self):
        self.__is_walking = False
        self.__thread.join()

    def get_id(self):
        return self.__id
