# 0- none
# 1- clouds
# 2- storm
from utils import randbol

class Cloud:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[0 for x in range(w)] for y in range(h)]

    def update(self,r = 1, mxr = 20, g = 1, mxg = 10):

        for i in range(self.h):
            for j in range(self.w):
                if randbol(r, mxr):
                    self.cells[i][j] = 1
                    if randbol(g, mxg):
                        self.cells[i][j] = 2
                else:
                    self.cells[i][j] = 0

    def export_data(self):
        return {'cells': self.cells}

    def import_data(self, data):
        self.cells = data['cells'] or [[0 for x in range(self.w)] for y in range(self.h)]

