from random import randint

# Maximum number of generations until the screen is refreshed
MAX_GEN_COUNT = 1000


# 3 x 3 pixel cells, array size = 2640 bytes per array
# GRIDX = 80  # 240
GRIDX = 73  # 219
GRIDY = 33  # 99
CELLXY = 3

# 2 x 2 pixel cells, array size = 6000 bytes per array
"""
GRIDX = 120
GRIDY = 50
CELLXY = 2
"""


class Life():

    def __init__(self):
        # Current grid and newgrid arrays are needed
        self.grid = [[0] * GRIDY for i in range(GRIDX)]
        # The new grid for the next generation
        self.newgrid = [[0] * GRIDY for i in range(GRIDX)]
        # Number of generations
        self.genCount = MAX_GEN_COUNT
        self.initGrid()

    def initGrid(self):
        print("Life: newgen")
        self.genCount = MAX_GEN_COUNT
        for x in range(GRIDX):
            for y in range(GRIDY):
                self.newgrid[x][y] = 0
                if x == 0 or x == GRIDX - 1 or y == 0 or y == GRIDY - 1:
                    self.grid[x][y] = 0
                else:
                    if randint(0, 4) == 1:
                        self.grid[x][y] = 1
                    else:
                        self.grid[x][y] = 0

    def clear(self):
        del self.grid
        del self.newgrid

    def nextGen(self):
        # drawgrid is done by caller
        """
        for x in range(1, GRIDX - 1):
            for y in range(1, GRIDY - 1):
                self.grid[x][y] = self.newgrid[x][y]
        """
        self.grid, self.newgrid = self.newgrid, self.grid
        self.genCount -= 1
        if self.genCount <= 0:
            self.initGrid()

    def computeCA(self):
        for x in range(1, GRIDX -1):
            for y in range(GRIDY - 1):
                neighbors = self.getNumberOfNeighbors(x, y)
                if self.grid[x][y] == 1 and (neighbors in (2,3)):
                    self.newgrid[x][y] = 1
                elif self.grid[x][y] == 1:
                    self.newgrid[x][y] = 0
                if self.grid[x][y] == 0 and (neighbors == 3):
                    self.newgrid[x][y] = 1
                elif self.grid[x][y] == 0:
                    self.newgrid[x][y] = 0

    def getNumberOfNeighbors(self, x, y):
        # print(x,y)
        return self.grid[x - 1][y] + self.grid[x - 1][y - 1] + self.grid[x][y - 1] + self.grid[x + 1][y - 1] \
               + self.grid[x + 1][y] + self.grid[x + 1][y + 1] + self.grid[x][y + 1] + self.grid[x - 1][y + 1]


"""
   The MIT License (MIT)

   Copyright (c) 2016 RuntimeProjects.com
   Copyright (c) 2021 Angainor

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.
"""

