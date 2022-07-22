import random

class Path:

    __rand_seed: bool
    __rand: int

    _x: int
    _y: int

    _x_min: int
    _x_max: int
    _y_min: int
    _y_max: int

    def __init__(self, x_min, x_max, y_min, y_max, seed):
        self.__seed = seed
        self.__rand = random.randint(1, 4)

        self._x_min = x_min
        self._x_max = x_max
        self._y_min = y_min
        self._y_max = y_max

        if self.__seed:
            self._x = random.randint(self._x_min, self._x_max)
            self._y = random.randint(self._y_min, self._y_max)
        else:
            self._x, self._y = 0, 0

    def __get_rand(self):
        ints_ = [1, 2, 3, 4]

        if self.__rand % 2 == 0:
            ints_.remove(self.__rand - 1)
        else:
            ints_.remove(self.__rand + 1)

        return random.choice(ints_)


    def _step(self):
        self.__rand = self.__get_rand()

        if self.__rand == 1:
            if self._x + 1 <= self._x_max:
                self._x = self._x + 1
            else:
                self._x = self._x - 1

        elif self.__rand == 2:
            if self._x - 1 >= self._x_min:
                self._x = self._x - 1
            else:
                self._x = self._x + 1

        elif self.__rand == 3:
            if self._y + 1 <= self._y_max:
                self._y = self._y + 1
            else:
                self._y = self._y - 1

        else:
            if self._y - 1 >= self._y_min:
                self._y = self._y - 1
            else:
                self._y = self._y + 1

    def get_path(self):
        return self._x, self._y
