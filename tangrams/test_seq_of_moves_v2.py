from tangrams import *
import random
import numpy as np
import matplotlib.pyplot as plt


np.random.seed(3)
random.seed(3)

json_all_pieces = '{"pieces": [["square", "0", "0 0"], ["small triangle2", "0", "0 1"], ["small triangle1", "90", "1 0"], ["large triangle1", "0", "1 1"], ["parrallelogram", "0", "2 0"], ["medium triangle", "0", "3 1"], ["large triangle2", "180", "1 1"]], "size": "5 5"}'
task_all_pieces = Task()
task_all_pieces.create_from_json(json_all_pieces)

sol = Solver()
task = Task()
# task.create_from_json('{"pieces": [["square", "0", "2 2"], ["small triangle2", "270", "3 2"], ["small triangle1", "0", "1 2"]], "size": "5 5"}')
task.create_from_json('{"pieces": [["large triangle2", "180", "1 1"], ["medium triangle", "180", "0 1"], ["square", "0", "2 0"], ["small triangle2", "90", "1 0"], ["small triangle1", "0", "2 3"], ["large triangle1", "0", "1 1"]], "size": "5 5"}')

sol.set_initial_task(task)
sol.run_task(task, duration=300, stop=True)
seq = sol.get_seq_of_moves_v2(task_all_pieces)
print seq
temp = Task()
plt.figure()
print(len(seq))
for s in seq:
    print s
    temp.create_from_json(s)
    plt.imshow(temp.x, interpolation='none')
    plt.pause(2)

