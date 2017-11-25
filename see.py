import numpy as np
import pickle

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
    A = np.zeros((len(ids), len(ids)))
    subscr_p = load_obj("subscr_p")
    subscr_g = load_obj("subscr_g")
    followers = load_obj("followers")
    for d in [subscr_p, subscr_g, followers]:
        for k, v in d.iteritems():
            if k in id_to_n:
                for val in v:
                    if val in id_to_n:
                        A[id_to_n[k], id_to_n[val]] = 1
                        A[id_to_n[val], id_to_n[k]] = 1
    with open("A.mat", "w") as f:
        for i in xrange(len(ids) - 1):
            print i
            for j in xrange(i + 1, len(ids)):
                if A[i,j] != 0:
                    f.write(str(i) + "\t" + str(j) + "\n")
    print len(ids)

if __name__ == "__main__":
    main()
