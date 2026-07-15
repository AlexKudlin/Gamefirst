# 🌲 🌊 🚁 🟩 🔥 🏥 ❤️ 🪣 🏦 ☁️ 🌧️ 🏆 ⬛️
from pynput import keyboard
from map import Map
import time
import os
import json
from Songapp.Game.cloud import Cloud
from helicopter import Helicopter as Helico

TICK_SLEEP = 0.05
TREE_UPDATE = 50
FIRE_UPDATE = 75
CLOUDS_UPDATE = 100
MAP_W, MAP_H = 20,10


field = Map(MAP_W, MAP_H)
helicopter = Helico(MAP_W, MAP_H)
clouds = Cloud(MAP_W, MAP_H)
tick = 1



MOVES = {'w': (-1,0), 'd': (0,1), 's': (1,0), 'a': (0,-1)}
# f - save, g - return
def process_key(key):
    global helicopter, tick, clouds, field
    c = key.char.lower()
    # обработка движений вертолета
    if c in MOVES.keys():
        dx, dy = MOVES[c][0], MOVES[c][1]
        helicopter.move(dx, dy)
        helicopter.move(-dx, -dy)
    # сохранение игры
    elif c == 'f':
        data = {'helicopter': helicopter.export_data(),
                'clouds': clouds.export_data(),
                'field': field.export_data(),
                'tick': tick
        }
        with open('level.json', 'w') as lvl:
           json.dump(data, lvl)
    # загрузка игры
    elif c == 'g':
        with open('level.json', 'r') as lvl:
            data = json.load(lvl)
            helicopter.import_data(data['helicopter'])
            tick = data['tick'] or 1
            field.import_data(data['field'])
            clouds.import_data(data['clouds'])

listener = keyboard.Listener(
    on_press=None,
    on_release=process_key)
listener.start()



while True:
    os.system('clear')
    field.process_helicopter(helicopter, clouds)
    helicopter.print_stats()
    field.print_map(helicopter, clouds)
    print('TICK', tick)
    tick += 1
    time.sleep(TICK_SLEEP)
    if (tick % TREE_UPDATE) == 0:
        field.add_tree()
    if (tick % FIRE_UPDATE) == 0:
        field.update_fires()
    if (tick % CLOUDS_UPDATE) == 0:
        field.clouds()

if __name__ == '__main__':
    app.run(debug=False)
