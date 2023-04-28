import copy
import timeit
import marshal
import json
import ujson
import pickle
import jsonpickle

from game import *

players = [
    ai_random(1, "red"),
    ai_random(2, "blue"),
    ai_random(3, "yellow"),
    ai_random(4, "green"),
]
inter = board_interface(players)
inter.board.players[0].victory_points = 10


methods = {
    "copy.deepcopy(inter)": 0,
    "copy.copy(inter)": 0,
    "ujson.loads(ujson.dumps(inter))": 0,
    "json.loads(json.dumps(inter))": 0,
    "pickle.loads(pickle.dumps(inter, -1))": 0,
    "jsonpickle.decode(jsonpickle.encode(inter))": 0,
    "marshal.loads(marshal.dumps(inter))": 0,
}

for method in methods.keys():
    try:
        times = timeit.repeat(method, globals=globals(), number=1, repeat=1000)
        average = sum(times) / len(times)
        methods[method] = average
    except Exception as e:
        methods[method] = math.inf

methods = {k: v for k, v in sorted(methods.items(), key=lambda item: item[1])}

for method in methods.keys():
    print(method.ljust(50), "{:.20f}".format(methods[method]))

assert copy.deepcopy(inter) == inter
assert copy.copy(inter) == inter
assert pickle.loads(pickle.dumps(inter, -1)) == inter
