import numpy as np
import pickle
from matplotlib import pyplot as plt

def load_obj(name ):
    with open('./' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def main():
    ids = load_obj("ids")
    n = 0
    id_to_n = {}
    for id in ids:
        id_to_n[id] = n
        n += 1
    x = []
    y = []
    with open("x.vec") as f:
        for line in f:
            x.append(float(line))
    with open("y.vec") as f:
        for line in f:
            y.append(float(line))
    colors = []
    s = []
    for id in ids:
        if id == 69827345:
            colors.append("r")
            s.append(100)
            print "ya"
        elif id == 28674927:
            colors.append("g")
            s.append(100)
            print "l"
        else:
            colors.append("b")
            s.append(10)
    plt.scatter(x, y, s=s, c=colors, alpha=0.25)
    plt.show()

if __name__ == "__main__":
    main()
