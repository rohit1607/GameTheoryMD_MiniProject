"""
The Recursive Probabilistic Serial Algorithm as in Algorithm 1 of https://arxiv.org/abs/2005.14122
Best of Both Worlds: Ex-ante and ex-post fairness in resource allocation

The algorithm makes use of two key components:
    1. Probabilistic Serial algorithm for the "eating()" protocol. This has been implemented by me
        in probabilistic_serial.py
    2. Birkhoff von Neumann decomposition: The implementation of the same has been borrowed from
        https://github.com/jfinkels/birkhoff and is named here as bvn.py

"""



import numpy as np
from probabilistic_serial import probabilistic_serial
from bvn import birkhoff_von_neumann_decomposition
from scipy import stats


def eating(M,prefs):
    """
    eating protocol. Uses probabilistic_serial.py
    Input:
    M: list of available set of goods
    prefs: prefernce matrix as a numpy array

    Returns:
    X: fractional allocation matrix as a np array
    """

    prob = probabilistic_serial(prefs)
    print(prob.pref_profile)
    X = prob.run_algorithm(method='dt=1')
    return X


def sample_integral_allocation(ws, As):
    """
    samples an integral allocation matrix A from the list of allocation matrices As
    based on the probabilites defined by ws

    Input: 
    ws: list of coeffs
    As: list of integral allocation matices

    Returns:
    Bt: Sampled integral allocation matrix
    """
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
    """
    updates M and B based on Bt
    Inputs:
    Bt: Sampled integral allocation matrix

    Outputs
    M: list of set of available goods
    B: list of sets of assigned goods to agents
    """
    n,m = Bt.shape
    for i in range(n):
        g = np.where(Bt[i,:]==1)[0][0]
        # print("g=", g)
        M.remove(g)
        B[i].add(g)
    return M, B

def recursive_prob_serial(M, B, prefs):
    """
    Recursive Probabilistic Serial Algorithm as in Algorithm 1 of https://arxiv.org/abs/2005.14122
    Inputs:
    prefs: prefernce matrix as a numpy array
    
    Outputs:
    M: list of set of available goods
    B: list of sets of assigned goods to agents
    """

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



if __name__ == "__main__":

    # prefs = np.array([[1,2,3,4],
    #             [1,3,2,4]],dtype=np.int)

    # prefs: prefernce matrix as a numpy array

    prefs = np.array([[1,2,3,4],  
                [1,3,2,4],
                [3,4,2,1],
                [4,3,2,1]],dtype=np.int)
    prefs = prefs - 1
    n,m = prefs.shape
    assert(m==n),"m not equal to n. matrices must be square matrices"

    #     M: list of set of available goods
    M = [0,1,2,3]

    #     B: list of sets of assigned goods to agents
    B = [set() for i in range(n)]

    
    B, M = recursive_prob_serial(M, B, prefs)
    print("Allocations to each agent:", B)
