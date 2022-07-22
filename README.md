# Mobile Ad Hoc Network Simulation

This application simulates a Mobile Ad Hoc Network of non-stationary clients
linked through wireless connections.

Clients use Distance Vector Routing Protocol to build the network, such that
clients in range of wireless connection are neighbors. By default, a clients
table is cleared when the locations of its device changes.

### Distance Vector Routing Protocol

*"A distance-vector routing protocol in data networks determines the best route
for data packets based on distance. Distance-vector routing protocols measure
the distance by the number of routers a packet has to pass; one router counts
as one hop."* -- wikiwand.com

### Command Line Flags

Before running the application, flags can be written in a terminal command line
to modify the simulation environment.

* `--count` the number of clients in the simulation; takes arguments of type
**int**.

* `--step` time padding in seconds between pseudo random location
movements; takes arguments of type **float**.

* `--seek` time padding in seconds between clients clearing tables;
takes arguments of type **float**.

* `--rate` time padding in seconds between clients updating tables;
takes arguments of type **float**.

* `--x_min` minimum x-axis boundary of simulation space; takes arguments of
type **float**.

* `--x_max` maximum x-axis boundary of simulation space; takes arguments of
type **float**.

* `--y_min` minimum y-axis boundary of simulation space; takes arguments of
type **float**.

* `--y_max` maximum y-axis boundary of simulation space; takes arguments of
type **float**.

* `--seed` denotes if initial locations are pseudo random; takes
**no arguments**

* `--range` maximum wireless range clients can establish connection; takes
arguments of type **float**.

* `--map` denotes if output will be to `MatPlotLib` visualizer; takes
**no arguments**

* `--refresh` time padding in seconds between refreshing output data during
simulation; takes arguments of type **float**.

### Examples

Command to start simulation with text output.  
```
python3 src/app.py --seed

```

![text_output_gif](text_output.gif)


Command to start simulation with MatPlotLib visual output.  
```
python3 src/app.py --seed --map

```
![visual_output_gif](visual_output.gif)
