import numpy as np
from probabilistic_serial import probabilistic_serial
from bvn import birkhoff_von_neumann_decomposition
from scipy import stats



def eating(M,prefs):
    prob = probabilistic_serial(prefs)
    print(prob.pref_profile)
    X = prob.run_algorithm(method='dt=1')
    return X

def sample_integral_allocation(ws, As):
    xk = np.arange(len(ws))
    pk = ws
    distr = stats.rv_discrete(name='custm', values=(xk, pk))
    x = int(distr.rvs(size=1)[0])
    # print("xk", xk)
    # print("pk", pk)
    # print("x",x)
    Bt = As[x]
    return Bt 

def update_M_B(Bt, M, B):
    n,m = Bt.shape
    for i in range(n):
        g = np.where(Bt[i,:]==1)[0][0]
        # print("g=", g)
        M.remove(g)
        B[i].add(g)
    return M, B

def recursive_prob_serial(M, B, prefs):
    n,m = prefs.shape
    for t in range(int(n/m)):
        print("t=",t)
        X , _ = eating(M,prefs)
        print("X=", X, type(X))
        results = birkhoff_von_neumann_decomposition(X)
        print(results)
        As = []
        ws = []
        for w, A in results:
            ws.append(w)
            As.append(A)
        print("ws", ws)
        print("As", As)
        Bt = sample_integral_allocation(ws, As)
        print("Bt", Bt)
        M,B = update_M_B(Bt, M, B)
        print("B:", B)
        print("M:", M)

    return B,M



# prefs = np.array([[1,2,3,4],
#             [1,3,2,4]],dtype=np.int)

prefs = np.array([[1,2,3,4],  
            [1,3,2,4],
            [3,4,2,1],
            [4,3,2,1]],dtype=np.int)
prefs = prefs - 1
n,m = prefs.shape
assert(m==n),"m not equal to n. matrices must be square matrices"
M = [0,1,2,3]
B = [set() for i in range(n)]
B = recursive_prob_serial(M, B, prefs)