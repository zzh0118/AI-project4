import numpy as np

file = "InputFile5.txt"

p_emission = []
emissions = []

with open(file, "r") as f:
    f.readline()
    p_notswitch = float(f.readline())
    f.readline()
    print("Emission probabilities are:","\n")
    for i in range(3):
            p_emission.append([float(p) for p in (f.readline().split(','))])
            print(p_emission[i],"\n")
    f.readline()
    emissions = [int(p) for p in f.readline()[1: -1].split(',')]
f.close()

def helper(obs, states, initial_p, trans_p, emit_p):
    max_p = np.zeros((len(obs), len(states)))
    path = np.zeros((len(states), len(obs)))
    for i in range(len(states)):
        max_p[0][i] = initial_p[i] * emit_p[i][obs[0] - 1]
        path[i][0] = i
    for t in range(1, len(obs)):
        newpath = np.zeros((len(states), len(obs)))
        for x in range(len(states)):
            cur_prob = -1
            for x0 in range(len(states)):
                temp_prob = max_p[t - 1][x0] * trans_p[x0][x] * emit_p[x][obs[t] - 1]
                if temp_prob > cur_prob:
                    cur_prob = temp_prob
                    state = x0
                    max_p[t][x] = cur_prob
                    for m in range(t):
                        newpath[x][m] = path[state][m]
                    newpath[x][t] = x
        path = newpath
    max_prob = -1
    path_state = 0
    for y in range(len(states)):
        if max_p[len(obs) - 1][y] > max_prob:
            max_prob = max_p[len(obs) - 1][y]
            path_state = y

    return path[path_state], max_prob

trans_matrix = [[0.0]*3 for i in range(3)]
p_switch = (1 - p_notswitch)/2

print("Transition probabilities:","\n")

for i in range(3):
    for j in range(3):
        if i == j :
            trans_matrix[i][j] = p_notswitch;
        else:
            trans_matrix[i][j] = p_switch;
    print(trans_matrix[i],"\n")

hidden_state = ["1", "2", "3"]
result, max_prob = helper(emissions, [1, 2, 3], [1/3, 1/3, 1/3], np.array(trans_matrix), np.array(p_emission))

print("The sequence states which best explains the sequence of rolls: ")
print([hidden_state[int(i)] for i in result],"\n")




