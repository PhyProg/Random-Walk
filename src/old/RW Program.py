import numpy
import matplotlib
import matplotsave
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from random import choice
from RandomWalk import RandomWalk
from RandomWalk import Settings
from RandomWalk import Setup
from RandomWalk import Plot


#set = Settings()
st = Setup(0, 0, 0, 0.5, 0.5, 0.5, 10, 20)
rw = RandomWalk(st)
pl = Plot(st)


def process_1():
    rw.add_wormhole_1D(1, 5)
    rw.add_wormhole_1D(-1, -5)
    rw.add_wormhole_1D(6,100)
    rw.add_wormhole_1D(4, 90)
    rw.add_wormhole_1D(-4, -80)
    rw.add_wormhole_1D(-6, -100)
    rw.add_wall_1D(3)
    rw.add_wall_1D(-3)
    rw.add_black_hole_1D(3)
    rw.add_black_hole_1D(-3)

    #print(rw.wormhole_1D, rw.wall_1D)

#process_1()

def process_2()
	rw.add_wormhole_1D(1,5)
	rw.add_wormhole_1D(5,1)
	rw.add_wall_1D(7)
	rw.add_wall_1D(-1)

rw.exotic_walk_1D()

plt.plot(rw.t, rw.x)
plt.show()


