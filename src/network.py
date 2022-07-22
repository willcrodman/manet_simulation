import threading, time, math

from client import Client

class Network():

    __stop_threads: bool
    __clients: list
    __threads: list

    count: int
    rate: int
    step: float
    seek: float

    def __init__(self, count, step, seek, rate, x_min, x_max, y_min, y_max,
                    seed, range):

        self.__clients = list()
        self.__threads = list()

        self.count = count
        self.step = step
        self.seek = seek
        self.rate = rate
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.seed = seed
        self.range = range

    @classmethod
    def default(cls):
        return cls(10, 1.0, 0.1, 10, 0, 20, 0, 20, False, 8.0)

    @staticmethod
    def __get_vector(x0, y0, x1, y1):
        return math.sqrt((x1 - x0)**2 + (y1 - y0)**2)

    def start(self):
        def target(source_id):

            ### Distance Vector Routing Protocol ###
            while True:
                # get current path of source client and reset neighbors
                self.__clients[source_id].clear_neighbors()
                x_0, y_0 = self.__clients[source_id].get_path()

                # init neighboring clients in table
                for i in range(self.count):
                    x_1, y_1 = self.__clients[i].get_path()
                    neighbor_id = self.__clients[i].get_id()
                    vector = self.__get_vector(x_0, y_0, x_1, y_1)

                    # check if client is neighbor -> add vector to table
                    if vector <= self.range:
                        self.__clients[source_id].set_table(neighbor_id,
                                                            vector,
                                                            neighbor_id,
                                                            neighbor=True)

                # updates per init
                for _ in range(self.rate):

                    # update table with neighboring clients shared tables
                    for id_0 in self.__clients[source_id].get_neighbors():
                        v_0 = self.__clients[source_id].get_table_value(id_0)

                        # iter over clients table
                        for id_1, v_1 in self.__clients[id_0].get_table().items():

                            # check if client has been update previously
                            try:
                                v_2 = self.__clients[source_id].get_table_value(v_1[1])
                                # if vector path is shortest path -> update table
                                if v_0[0] + v_1[0] < v_2[0]:
                                    self.__clients[source_id].set_table(v_1[1],
                                                                        (v_0[0]+v_1[0]),
                                                                        id_1)

                            except KeyError as error:
                                self.__clients[source_id].set_table(v_1[1],
                                                                    (v_0[0]+v_1[0]),
                                                                    id_1)

                    # interval per update
                    time.sleep(self.seek)

                # check if thread will close
                if self.__stop_threads: break

        self.__stop_threads = False

        for i in range(self.count):
            client = Client(self.x_min, self.x_max, self.y_min, self.y_max, \
                                self.seed, i)
            self.__clients.append(client)
            thread = threading.Thread(target=target, args=(i,))
            self.__threads.append(thread)

        for i in range(self.count):
            self.__clients[i].start_walking(self.step)
            self.__threads[i].start()

    def stop(self):
        self.__stop_threads = True

        for i in range(self.count):
            self.__clients[i].stop_walking()
            self.__threads[i].join()

    def get_clients(self):
        return self.__clients
