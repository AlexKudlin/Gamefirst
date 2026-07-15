from utils import randbol
from utils import randcell
from utils import randcell2
from Songapp.Game.cloud import Cloud

# 0 - field
# 1 - tree
# 2 - river
# 3 - hospital
# 4 - up grate-shop
# 5 - fire


CELL_TYPES = '🟩🌲🌊🏥🏦🔥'

TREE_BONUS = 100
UPGRADE_PRICE = 5000
LIVE_COST = 10000

class Map:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[0 for _ in range(w)] for _ in range(h)]
        self.generate_forest(5,10)
        self.generate_river(10)
        self.generate_river(10)
        self.generate_upgrade_shop()
        self.generate_hospital()
        self.clouds = Cloud(w, h)


    def check_bounds(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h
    def print_map(self, helicopter, clouds):
        print('⬛' * (self.w+2))
        for ri in range(self.h):
            print('⬛', end ='')
            for ci in range(self.w):
                if clouds.cells[ri][ci] == 1:
                    print('☁️', end ='')
                elif self.clouds.cells[ri][ci] == 2:
                    print('🌀', end ='')
                cell = self.cells[ri][ci]
                if helicopter.x == ri and helicopter.y == ci:
                    print('🚁', end='')
                elif 0 <= cell < len(CELL_TYPES):
                    print(CELL_TYPES[cell], end='')
            print('⬛')
        print('⬛' * (self.w + 2))


    def generate_river(self, l):
        rc = randcell(self.h, self.w)
        rx, ry = rc[0], rc[1]
        if not self.check_bounds(rx, ry):
            return
        self.cells[rx][ry] = 2
        while l > 0:
            nx, ny = randcell2(rx, ry)
            if not self.check_bounds(nx, ny):
                break
            if nx == rx and ny == ry:
                break
            self.cells[nx][ny] = 2
            rx, ry = nx, ny
            l -= 1
    def generate_forest(self, r, mxr):
        for ri in range(self.h):
            for ci in range(self.w):
                if randbol(r, mxr):
                    self.cells[ri][ci] = 1
    def add_tree(self):
        c = randcell(self.h, self.w)
        cx,cy = c[0], c[1]
        if  self.cells[cx][cy] == 0:
            self.cells[cx][cy] = 1
    def generate_upgrade_shop(self):
        c = randcell(self.h, self.w)
        cx,cy = c[0], c[1]
        self.cells[cx][cy] = 4
    def generate_hospital(self):
        c = randcell(self.h, self.w)
        cx,cy = c[0], c[1]
        if self.cells[cx][cy] != 4:
            self.cells[cx][cy] = 3
        else:
            self.generate_hospital()

    def add_fire(self):
        c = randcell(self.h, self.w)
        cx,cy = c[0], c[1]
        if self.cells[cx][cy] == 1:
            self.cells[cx][cy] = 5
    def update_fires(self):
        for ri in range(self.h):
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if cell == 5:
                         self.cells[ri][ci] = 0
        for i in range(10):
            self.add_fire()

    def process_helicopter(self, helicopter, clouds):
        c = self.cells[helicopter.x][helicopter.y]
        d = clouds.cells[helicopter.x][helicopter.y]
        if c == 2:
            helicopter.tank = helicopter.mxtank
        if c == 5 and helicopter.tank > 0:
            helicopter.tank -= 1
            helicopter.score += TREE_BONUS
            self.cells[helicopter.x][helicopter.y] = 1
        if c==4 and helicopter.score >= UPGRADE_PRICE:
            helicopter.tank += 1
            helicopter.score -= UPGRADE_PRICE
        if c==3 and helicopter.score >= LIVE_COST:
            helicopter.lives += 10
            helicopter.score -= LIVE_COST
        if d==2:
            helicopter.lives -= 1
            if helicopter.lives == 0:
                helicopter.game_over()

    def export_data(self):
        return {'cells': self.cells}

    def import_data(self, data):
        self.cells = data['cells'] or [[0 for x in range(self.w)] for y in range(self.h)]