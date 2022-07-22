import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np

import threading, sys, time, os

from network import Network

if __name__ != '__main__':
    raise Exception(f"cannot run {__file__} from {__name__} as import")

MAP = False
REFRESH = 1.0

network = Network.default()

for i in range(1, len(sys.argv)):
    if sys.argv[i] == "--count":
        network.count = int(sys.argv[i+1])
    if sys.argv[i] == "--step":
        network.step = int(sys.argv[i+1])
    if sys.argv[i] == "--seek":
        network.seek = float(sys.argv[i+1])
    if sys.argv[i] == "--rate":
        network.rate = int(sys.argv[i+1])
    if sys.argv[i] == "--x_min":
        network.x_min = int(sys.argv[i+1])
    if sys.argv[i] == "--x_max":
        network.x_max = int(sys.argv[i+1])
    if sys.argv[i] == "--y_min":
        network.y_min = int(sys.argv[i+1])
    if sys.argv[i] == "--y_max":
        network.y_max = int(sys.argv[i+1])
    if sys.argv[i] == "--seed":
        network.seed = True
    if sys.argv[i] == "--range":
        network.range = float(sys.argv[i+1])
    if sys.argv[i] == "--map":
        MAP = True
    if sys.argv[i] == "--refresh":
        REFRESH = float(sys.argv[i+1])

network.start()

if MAP == False:

    def target():
        global run_thread
        input("")
        run_thread = False

    run_thread = True
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

    while run_thread:
        clients = network.get_clients()

        os.system('clear')
        print("**************************************")
        print("*** MANET Network Simulation ***")
        print("************************************** \n")

        for client in clients:
            id = client.get_id()
            x, y = client.get_path()
            table_length = len(client.get_table())

            print(f"Client {id}:")
            print(f"    position: ({x}, {y}) -- table lenght: {table_length} \n")

        print("________________________________________")
        print("Click ENTER or RETURN to exit program...")

        time.sleep(REFRESH)

    thread.join()

else:

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)

    def imscatter(x, y, image, zoom, ax):
        try:
            image = plt.imread(image)
        except TypeError:
            pass
        im = OffsetImage(image, zoom=zoom)
        x, y = np.atleast_1d(x, y)
        artists = []
        for x0, y0 in zip(x, y):
            ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
            artists.append(ax.add_artist(ab))
            ax.update_datalim(np.column_stack([x, y]))
            ax.autoscale()
        return artists

    def animate(i):
        global network

        clients = network.get_clients()
        xs, ys, ids, edges = list(), list(), list(), set()

        for client in clients:
            id = client.get_id()
            x, y = client.get_path()
            neighbors = client.get_neighbors()

            ids.append(id)
            xs.append(x)
            ys.append(y)

            for neighbor in neighbors:
                if neighbor != id:
                    edges.add(frozenset([id, neighbor]))

        ax.clear()

        for edge in edges:
            v0, v1, = edge
            x0, x1, y0, y1 = xs[v0], xs[v1], ys[v0], ys[v1]
            plt.plot([x0, x1], [y0, y1], color='royalblue', linewidth=3)

        imscatter(xs, ys, 'laptop.png', zoom=0.25, ax=ax)

        ax.set_xlim([network.x_min, network.x_max])
        ax.set_ylim([network.y_min, network.y_max])
        ax.set_aspect('equal')
        plt.title(f"MANET Network Simulation -- Clients: {network.count}")

    ani = animation.FuncAnimation(fig, animate, repeat_delay=int(REFRESH*1000),
                                    interval=1000)
    plt.show(block=False)

    input("Click ENTER or RETURN to exit program...")

    plt.close()

network.stop()
