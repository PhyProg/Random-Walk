"""This part of program is for all of the calculations.
   Classes will be imported in other program."""

#import libraries

import numpy
import matplotlib
import matplotsave
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from random import choice

const = 100000000000000

class Settings():

   def __init__(self,st):
       self.a = st

class Setup():

    def __init__(self,x_0, y_0, z_0, p_x, p_y, p_z, r, st):
        self.start_x = x_0
        self.start_y = y_0
        self.start_z = z_0
        self.p_x_l = p_x
        self.p_y_l = p_y
        self.p_z_l = p_z
        self.repeat = r
        self.steps = st

class RandomWalk():

    """Initialization of basic variables used in programs."""

    def __init__(self,setup):

        #Number of steps, speed, probabilities, etc.

        self.steps = setup.steps
        self.speed = 2
        self.p_x_l = setup.p_x_l
        self.p_x_r = 1-self.p_x_l
        self.p_y_l = setup.p_y_l
        self.p_y_r = 1-self.p_y_l
        self.p_z_l = setup.p_z_l
        self.p_z_r = 1-self.p_z_l
        self.x_min = 0
        self.y_min = 0
        self.z_min = 0
        self.x_max = 0
        self.y_max = 0
        self.z_max = 0

        #Coordinates and time for appropriate plots

        self.x = [0]
        self.y = [0]
        self.z = [0]
        self.t = [0]

        self.x[0] = setup.start_x
        self.y[0] = setup.start_y
        self.z[0] = setup.start_z

        #Number of occurences of appropriate coordinate

        self.num_x = [0 for i in range(2 * self.steps)]
        self.num_y = [0 for i in range(2 * self.steps)]
        self.num_z = [0 for i in range(2 * self.steps)]

        #Exotic possibilities

        self.wormhole_1D = []
        self.wormhole_2D = [[],[]]
        self.wormhole_3D = [[],[],[]]
        self.wall_1D = []
        self.wall_2D = []
        self.wall_3D = []
        self.black_hole_1D = []
        self.black_hole_2D = []
        self.black_hole_3D = []

    """Next three functions are used to generate random walk in 1,2 and 3 dimensions. Besides that, number of
       occurences of each coordinate is calculated, which will later be used to calculate probabilities and check
       if theoretical predictions are in good agreement with stochastic model."""

    #Generating 1D Random Walk

    def walk_1d(self):
        for i in range(1, self.steps):
            r = choice([-1, 1])
            if r == 1:
                self.x.append(self.x[i-1] + self.p_x_l * self.speed)
            elif r == -1:
                self.x.append(self.x[i-1] - self.p_x_r * self.speed)

            self.t.append(i)
            self.check_min_1D(i)

        # Occurences

        for i in range(self.steps):
            self.num_x[int(self.x[i]*const/(2*self.p_x_r*const))+self.steps]+=1
            #print(i, self.x[i], self.num_x[int(self.x[i]/(2*self.p_x_r))+self.steps], '\n')

    #Generating 2D Random Walk

    def walk_2d(self):
        for i in range(1, self.steps):
            r_x = choice([-1, 1])
            r_y = choice([-1, 1])
            if r_x == 1:
                self.x.append(self.x[i-1] + self.p_x_l * self.speed)
            elif r_x == -1:
                self.x.append(self.x[i-1] - self.p_x_r * self.speed)
            if r_y == 1:
                self.y.append(self.y[i-1] + self.p_y_l * self.speed)
            elif r_y == -1:
                self.y.append(self.y[i-1] - self.p_y_r * self.speed)

            self.t.append(i)
            self.check_min_2D(i)

        for i in range(self.steps):
            self.num_x[int(self.x[i] * const / (2 * self.p_x_r * const)) + self.steps] += 1
            self.num_y[int(self.y[i] * const / (2 * self.p_y_r * const)) + self.steps] += 1

    #Generating 3D Random Walk

    def walk_3d(self):
        for i in range(1, self.steps):
            r_x = choice([-1, 1])
            r_y = choice([-1, 1])
            r_z = choice([-1, 1])
            if r_x == 1:
                self.x.append(self.x[i - 1] + self.p_x_l * self.speed)
            elif r_x == -1:
                self.x.append(self.x[i - 1] - self.p_x_r * self.speed)
            if r_y == 1:
                self.y.append(self.y[i - 1] + self.p_y_l * self.speed)
            elif r_y == -1:
                self.y.append(self.y[i - 1] - self.p_y_r * self.speed)
            if r_z == 1:
                self.z.append(self.z[i - 1] + self.p_z_l * self.speed)
            elif r_z == -1:
                self.z.append(self.z[i - 1] - self.p_z_r * self.speed)

            self.t.append(i)
            self.check_min_3D(i)

        for i in range(self.steps):
            self.num_x[int(self.x[i] * const / (2 * self.p_x_r * const)) + self.steps] += 1
            self.num_y[int(self.y[i] * const / (2 * self.p_y_r * const)) + self.steps] += 1
            self.num_z[int(self.z[i] * const / (2 * self.p_z_r * const)) + self.steps] += 1

    def check_min_1D(self, i):
        if self.x[i] < self.x_min: self.x_min = self.x[i]
        if self.x[i] > self.x_max: self.x_max = self.x[i]

    def check_min_2D(self, i):
        if self.x[i] < self.x_min: self.x_min = self.x[i]
        if self.x[i] > self.x_max: self.x_max = self.x[i]
        if self.y[i] < self.y_min: self.y_min = self.y[i]
        if self.y[i] > self.y_max: self.y_max = self.y[i]

    def check_min_3D(self, i):
        if self.x[i] < self.x_min: self.x_min = self.x[i]
        if self.x[i] > self.x_max: self.x_max = self.x[i]
        if self.y[i] < self.y_min: self.y_min = self.y[i]
        if self.y[i] > self.y_max: self.y_max = self.y[i]
        if self.z[i] < self.z_min: self.z_min = self.z[i]
        if self.z[i] > self.z_max: self.z_max = self.z[i]

    """Special and complicated type of random walk is self-avoiding walk, for example it is used to 
       model polymer chain."""

    #Self-Avoiding random walks

    def self_avoiding_walk_2d(self):
        self.table = [[]]
        for i in range(1, self.steps):
            check = True
            while check:
                r_x = choice([-1, 1])
                r_y = choice([-1, 1])
                if r_x == 1:
                    self.x.append(self.x[i-1] + self.p_x_l * self.speed)
                elif r_x == -1:
                    self.x.append(self.x[i-1] - self.p_x_r * self.speed)
                if r_y == 1:
                    self.y.append(self.y[i-1] + self.p_y_l * self.speed)
                elif r_y == -1:
                    self.y.append(self.y[i-1] - self.p_y_r * self.speed)

                if len(self.table) < self.x[i]:
                    self.table.append([0 for j in range(len(self.table[0]))])
                    check = False

                if len(self.table[0]) < self.y[i]:
                    for j in range(len(self.table)):
                        self.table[j].append(0)
                    check = False

                if not check:
                    self.table[int(self.x[i])][int(self.y[i])] = 1
                    continue

                if self.table[int(self.x[i])][int(self.y[i])] == 1:
                    self.x.remove(self.x[i-1] + self.p_x_l * self.speed)
                    self.y.remove(self.y[i-1] + self.p_y_l * self.speed)
                elif self.table[int(self.x[i])][int(self.y[i])] == 0:
                    self.table[int(self.x[i])][int(self.y[i])] = 1
                    check = False


            self.t.append(i)

            if self.x[i] < self.x_min: self.x_min = self.x[i]
            if self.x[i] > self.x_max: self.x_max = self.x[i]
            if self.y[i] < self.y_min: self.y_min = self.y[i]
            if self.y[i] > self.y_max: self.y_max = self.y[i]

        for i in range(self.steps):
            self.num_x[int(self.x[i] * const / (2 * self.p_x_r * const)) + self.steps] += 1
            self.num_y[int(self.y[i] * const / (2 * self.p_y_r * const)) + self.steps] += 1

    def self_avoiding_walk_3d(self):
        self.table = [[[]]]
        for i in range(1, self.steps):
            check = True
            while check:
                r_x = choice([-1, 1])
                r_y = choice([-1, 1])
                r_z = choice([-1, 1])
                if r_x == 1:
                    self.x.append(self.x[i - 1] + self.p_x_l * self.speed)
                elif r_x == -1:
                    self.x.append(self.x[i - 1] - self.p_x_r * self.speed)
                if r_y == 1:
                    self.y.append(self.y[i - 1] + self.p_y_l * self.speed)
                elif r_y == -1:
                    self.y.append(self.y[i - 1] - self.p_y_r * self.speed)
                if r_z == 1:
                    self.z.append(self.z[i - 1] + self.p_z_l * self.speed)
                elif r_z == -1:
                    self.z.append(self.z[i - 1] - self.p_z_r * self.speed)



                if len(self.table) < self.x[i]:
                    self.table.append([0 for j in range(len(self.table[0]))])
                    check = False

                if len(self.table[0]) < self.y[i]:
                    for j in range(len(self.table)):
                        self.table[j].append(0)
                    check = False

                if not check:
                    self.table[int(self.x[i])][int(self.y[i])][int(self.z[i])] = 1
                    continue

                if self.table[int(self.x[i])][int(self.y[i])][int(self.z[i])] == 1:
                    self.x.remove(self.x[i])
                    self.y.remove(self.y[i])
                    self.z.remove(self.z[i])
                elif self.table[int(self.x[i])][int(self.y[i])] == 0:
                    self.table[int(self.x[i])][int(self.y[i])][int(self.z[i])] = 1
                    check = False

            self.t.append(i)

            if self.x[i] < self.x_min: self.x_min = self.x[i]
            if self.x[i] > self.x_max: self.x_max = self.x[i]
            if self.y[i] < self.y_min: self.y_min = self.y[i]
            if self.y[i] > self.y_max: self.y_max = self.y[i]
            if self.z[i] < self.z_min: self.z_min = self.z[i]
            if self.z[i] > self.z_max: self.z_max = self.z[i]

    """Next part consist of exotic and interesting models:
        - Wormhole
	- Black Holes
        - Walls
        ... 
       And is implemented in next lines. It is consisted of initializations and realizations of walks."""

    def add_wormhole_1D(self, x1, x2):
        self.wormhole_1D.append((x1,x2))

    def add_wormhole_2D(self, x1, x2, y1, y2):
        self.wormhole_2D[0].append((x1, x2))
        self.wormhole_2D[1].append((y1, y2))

    def add_wormhole_3D(self, x1, x2, y1, y2, z1, z2):
        self.wormhole_3D[0].append((x1, x2))
        self.wormhole_3D[1].append((y1, y2))
        self.wormhole_3D[2].append((z1, z2))

    def add_wormhole_1D_two_ways(self, x1, x2):
        self.wormhole_1D.append((x1, x2))
        self.wormhole_1D.append((x2, x1))

    def add_wormhole_2D_two_ways(self, x1, x2, y1, y2):
        self.wormhole_2D[0].append((x1, x2))
        self.wormhole_2D[1].append((y1, y2))
        self.wormhole_2D[0].append((x2, x1))
        self.wormhole_2D[1].append((y2, y1))

    def add_wormhole_3D_two_ways(self, x1, x2, y1, y2, z1, z2):
        self.wormhole_3D[0].append((x1, x2))
        self.wormhole_3D[1].append((y1, y2))
        self.wormhole_3D[2].append((z1, z2))
        self.wormhole_3D[0].append((x2, x1))
        self.wormhole_3D[1].append((y2, y1))
        self.wormhole_3D[2].append((z2, z1))

    def merge_wormholes_1D(self):
        for i in range(len(self.wormhole_1D)):
            for j in range(i+1,len(self.wormhole_1D)):
                if self.wormhole_1D[i][1] == self.wormhole_1D[j][0]:
                    self.wormhole_1D[i][1] == self.wormhole_1D[j][1]

    def merge_wormholes_2D(self):
        for i in range(len(self.wormhole_2D)):
            for j in range(i+1,len(self.wormhole_2D)):
                if self.wormhole_2D[i][0][1] == self.wormhole_2D[j][0][0] \
                    and self.wormhole_2D[i][1][1] == self.wormhole_2D[j][1][0]:
                    self.wormhole_2D[i][0][1] == self.wormhole_2D[j][0][1]
                    self.wormhole_2D[i][1][1] == self.wormhole_2D[j][1][1]

    def merge_wormholes_3D(self):
        for i in range(len(self.wormhole_3D)):
            for j in range(i+1,len(self.wormhole_3D)):
                if self.wormhole_3D[i][0][1] == self.wormhole_3D[j][0][0] \
                        and self.wormhole_3D[i][1][1] == self.wormhole_3D[j][1][0] \
                        and self.wormhole_3D[i][2][1] == self.wormhole_3D[j][2][0]:
                    self.wormhole_3D[i][0][1] == self.wormhole_3D[j][0][1]
                    self.wormhole_3D[i][1][1] == self.wormhole_3D[j][1][1]
                    self.wormhole_3D[i][2][1] == self.wormhole_3D[j][2][1]

    def add_black_hole_1D(self, x):
        self.black_hole_1D.append(x)

    def add_black_hole_2D(self, x, y):
        self.black_hole_2D.append((x, y))

    def add_black_hole_3D(self, x, y, z):
        self.black_hole_3D.append((x, y, z))

    def add_wall_1D(self, x):
        self.wall_1D.append(x)

    def add_wall_2D(self, x, y):
        self.wall_2D.append((x,y))

    def add_wall_3D(self, x, y, z):
        self.wall_3D.append((x, y, z))

    def exotic_walk_1D(self):
        absorbed = False
        self.merge_wormholes_1D()
        #self.t.append(0)
        i = 1
        while i in range(1, self.steps):

            #Checking if walker is absorbed during walk

            if absorbed:
                self.x.append(self.x[i-1])
                self.t.append(i)
                i+=1
                continue

            #Next step

            worm_next = []
            r = choice([-1, 1])
            check_x = False
            __x = int(self.x[i-1] + r * self.p_x_l * self.speed)

            #Check if next step is a wall or it is available for move, then appending appropriate new coordinate

            k = 0
            while k in range(0, len(self.wall_1D)) and not check_x:
                if __x == self.wall_1D[k]:
                    check_x = True
                k+=1

            if check_x:
                self.x.append(self.x[i-1])
                self.t.append(i)
                self.check_min_1D(i)
                i += 1
                continue
            else:
                self.x.append(__x)
                self.t.append(i)
                i += 1

            #Check

            self.check_min_1D(i-1)

            #Wormhole part

            for j in range(len(self.wormhole_1D)):
                if __x == self.wormhole_1D[j][0]:
                    worm_next.append(self.wormhole_1D[j][1])

            if worm_next:
                self.t.append(i)
                self.x.append(choice(worm_next))
                self.check_min_1D(i)
                i += 1

            #Absorber part

            for j in range(len(self.black_hole_1D)):
                if self.x[i-1] == self.black_hole_1D[j]:
                    self.check_min_1D(i-1)
                    absorbed = True

        #Occurences

        #for i in range(self.steps):
            #self.num_x[int(self.x[i]*const/(2*self.p_x_r*const))+self.steps]+=1
            #print(i, self.x[i], self.num_x[int(self.x[i]/(2*self.p_x_r))+self.steps], '\n')

    def exotic_walk_2D(self):
        absorbed = False
        self.merge_wormholes_2D()
        i = 1
        while i in range(1, self.steps):

            #Check if walker is apsorbed

            if absorbed:
                self.x.append(self.x[i - 1])
                self.y.append(self.y[i - 1])
                self.t.append(i)
                i+=1
                continue

            #Next step

            worm_next = []
            r_x = choice([-1, 1])
            r_y = choice([-1, 1])
            check = False
            __x = self.x[i - 1] + r_x * self.p_x_l * self.speed
            __y = self.y[i - 1] + r_y * self.p_y_l * self.speed

            #Check if next step is a wall or not

            k = 0
            while j in range(len(self.wall_2D)) and not check:
                if __x == self.wall_2D[j][0] and __y == self.wall_2D[j][1]:
                    check = True
                k += 1

            if check :
                self.x.append(self.x[i-1])
                self.y.append(self.y[i-1])
                self.t.append(i)
                self.check_min_2D(i)
                i += 1
                continue
            else:
                self.x.append(__x)
                self.y.append(__y)
                self.t.append(i)
                self.check_min_2D(i)
                i += 1

            #Wormhole part

            for j in range(len(self.wormhole_2D)):
                if __x == self.wormhole_2D[j][0][0] and __y == self.wormhole_2D[j][1][0]:
                    worm_next.append(self.wormhole_2D[j][0][1], self.wormhole_2D[j][1][1])

            if worm_next:
                self.t.append(i)
                i += 1
                (__x, __y) = choice(worm_next)
                self.x.append(__x)
                self.y.append(__y)
                self.check_min_2D(i - 1)

            for j in range(len(self.black_hole_2D)):
                if (self.x[i-1], self.y[i-1]) == self.black_hole_2D[j]:
                    self.check_min_2D(i-1)
                    absorbed = True

        for i in range(self.steps):
            self.num_x[int(self.x[i] * const / (2 * self.p_x_r * const)) + self.steps] += 1
            self.num_y[int(self.y[i] * const / (2 * self.p_y_r * const)) + self.steps] += 1

    def exotic_walk_3D(self):
        absorbed = False
        self.merge_wormholes_2D()
        i = 1
        while i in range(1, self.steps):

            # Checking if walker is absorbed during walk

            if absorbed:
                self.x.append(self.x[i - 1])
                self.y.append(self.y[i - 1])
                self.z.append(self.z[i - 1])
                self.t.append(i)
                continue

            #Generating next step

            worm_next = []
            r_x = choice([-1, 1])
            r_y = choice([-1, 1])
            r_z = choice([-1, 1])
            check = False
            __x = self.x[i - 1] + r_x * self.p_x_l * self.speed
            __y = self.y[i - 1] + r_y * self.p_y_l * self.speed
            __z = self.z[i - 1] + r_z * self.p_z_l * self.speed

            #Check if next step is a wall or not

            k = 0
            while k in range(len(self.wall_3D)) and not check:
                if __x == self.wall_3D[j][0] and __y == self.wall_3D[j][1] and __z == self.wall_3D[j][2]:
                    check = True
                k += 1

            if check :
                self.x.append(self.x[i-1])
                self.y.append(self.y[i-1])
                self.z.append(self.z[i-1])
                self.check_min_3D(i)
                self.t.append(i)
                i+=1
                continue
            else:
                self.x.append(__x)
                self.y.append(__y)
                self.z.append(__z)
                self.t.append(i)
                self.check_min_3D(i)
                i += 1

            #Check wormhole

            for j in range(len(self.wormhole_1D)):
                if __x == self.wormhole_3D[j][0][0] and __y == self.wormhole_3D[j][1][0] and __z == self.wormhole_3D[j][2][0]:
                    worm_next.append(self.wormhole_3D[j][0][1], self.wormhole_3D[j][1][1], self.wormhole_3D[j][2][1])

            if worm_next:
                self.t.append(i)
                (__x, __y, __z) = choice(worm_next)
                self.x.append(__x)
                self.y.append(__y)
                self.z.append(__z)
                self.check_min_3D(i)
                i += 1

            for j in range(len(self.black_hole_3D)):
                if (self.x[i-1], self.y[i-1], self.z[i-1]) == self.black_hole_3D[j]:
                    self.check_min_3D(i-1)
                    absorbed = True

        for i in range(self.steps):
            self.num_x[int(self.x[i] * const / (2 * self.p_x_r * const)) + self.steps] += 1
            self.num_y[int(self.y[i] * const / (2 * self.p_y_r * const)) + self.steps] += 1
            self.num_z[int(self.z[i] * const / (2 * self.p_z_r * const)) + self.steps] += 1

    #Reseting variables

    def reset(self):
        self.x = [0]
        self.y = [0]
        self.z = [0]
        self.t = [0]
        self.num_x = [0 for i in range(2 * self.steps)]
        self.num_y = [0 for i in range(2 * self.steps)]
        self.num_z = [0 for i in range(2 * self.steps)]
        self.wormhole_1D = []
        self.wormhole_2D = [[], []]
        self.wormhole_3D = [[], [], []]
        self.wall_1D = []
        self.wall_2D = []
        self.wall_3D = []
        self.black_hole_1D = []
        self.black_hole_2D = []
        self.black_hole_3D = []

class Plot():

    def __init__(self, setup):
        self.rw = RandomWalk(setup)
        self.num = setup.repeat
        self.a = []
        self.b = []

    def plt_1D_walk(self,setup):
        self.rw.__init__(setup)
        for i in range(self.num):
            self.rw.walk_1d()
            plt.plot(self.rw.t, self.rw.x)
            plt.title('1D Random Walk trajectory')
            plt.ylabel('X')
            plt.xlabel('T')
            self.rw.reset()
        plt.show()

    def plt_1D_walk_mean(self,setup):
        self.mean = [0 for i in range(setup.steps)]
        self.mean_s = [0 for i in range(setup.steps)]
        self.rw.__init__(setup)
        for i in range(self.num):
            self.rw.walk_1d()
            for j in range(setup.steps):
                self.mean[j] += self.rw.x[i]
                self.mean_s[j] += self.rw.x[i]*self.rw.x[i]
            self.rw.reset()
        for j in range(setup.steps):
            self.mean[j] /= self.num
            self.mean_s[j] /= self.num

        plt.plot(self.mean)
        plt.plot(self.mean_s)
        plt.show()

    def plt_1D_walk_prob(self, setup):
        self.rw.__init__(setup)
        self.rw.walk_1d()
        min = 0
        while self.rw.num_x[min] == 0 :
            min += 1
        max = min
        while self.rw.num_x[max] != 0 :
            max += 1
        print(min,max)
        a = []
        for i in range(min, max):
            a.append(self.rw.num_x[i])

        plt.plot(self.rw.x)

        plt.show()
        plt.plot(a)
        plt.show()
        plt.hist(a)
        plt.show()

    def plt_2D_walk(self,setup):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('t')

        self.rw.__init__(setup)
        for i in range(self.num):
            self.rw.walk_2d()
            plt.plot(self.rw.x, self.rw.y, self.rw.t)
            plt.title('2D Random Walk')
            self.rw.reset()
        plt.show()

    def plt_2D_walk_x_v_y(self,setup):
        self.rw.__init__(setup)
        for i in range(self.num):
            self.rw.walk_2d()
            plt.plot(self.rw.x, self.rw.y)
            plt.title('2D Random Walk trajectory')
            plt.ylabel('Y')
            plt.xlabel('X')
            self.rw.reset()
        plt.show()

    def plt_3D_walk(self,setup):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        self.rw.__init__(setup)
        for i in range(self.num):
            self.rw.walk_3d()
            ax.plot(self.rw.x, self.rw.y, self.rw.z)
            plt.title('3D Random Walk trajectory')
            self.rw.reset()
        plt.show()

