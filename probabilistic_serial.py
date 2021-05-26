from fractions import Fraction
import numpy as np



MAX_ITER = 10

class probabilistic_serial:

    # input preferences over goods for each player in the form of np array
    # n: no. of agents
    # m: No. of goods
    def __init__(self, pref_matrix):
        self.n, self.m = pref_matrix.shape
        print("pref_profile.shape=", pref_matrix.shape)
        self.N = [i for i in range(self.n)] #list of agents
        self.M = [j for j in range(self.m)] #list of goods
        self.allocations = np.zeros((self.n,self.m))
        self.supply = np.ones((1,self.m))
        self.pref_profile = { i:[ pref_matrix[i,j] for j in range(self.m) ]  for i in range(self.n)}
        self.eater_info = None
        self.n_eaters = None
        self.method = None
    
    def get_eater_info(self):
        # eater_info will be an array with row entries of form [agent, pref]
        # print(goods_left)
        eater_info = []
        for i in self.N:
            pref = self.pref_profile[i][0]
            print("pref:",pref)
            while pref<self.m:
                if self.supply[0,pref]>0:             #if the preferred good is left, eat it
                    eater_info.append([i,pref])
                    break
                else:                               #else, check if the next pref is available
                    pref+=1
        self.eater_info = np.array(eater_info, dtype=np.int)
        print("eater_info=", self.eater_info, self.eater_info.shape)
        return self.eater_info

    def count_eaters(self):
        self.n_eaters = np.zeros((1,self.m), dtype=np.int)
        nrows,_ =  self.eater_info.shape
        for agnt in range(nrows):
            g = self.eater_info[agnt,1]
            self.n_eaters[0,g]+=1
        print("self.n_eaters= ",self.n_eaters)
        return self.n_eaters

    def eat(self, time_left):
        fin_goods=[]
        times_reqd = np.array([self.supply[0,i]/self.n_eaters[0,i] for i in range(self.m) if self.supply[0,i]!=0 and self.n_eaters[0,i]!=0])
       
        if self.method == 'full':
            dt = np.min(times_reqd)
        if self.method == 'dt=1':
            dt = np.min((np.min(times_reqd), time_left))
            print("time left < min(times_reqd)", time_left, np.min(times_reqd))

        print("times_reqd=",times_reqd, times_reqd.shape)
        print("dt=",dt)
        nrows,_ =  self.eater_info.shape

        for i in range(nrows):
            row_vals = self.eater_info[i,:]
            agnt, g = row_vals[0], row_vals[1]
            self.supply[0,g] -= dt
            self.allocations[agnt,g] += dt
            if self.supply[0,g]==0:
                fin_goods.append(g)

        for i in range(self.n):
            for g in fin_goods:
                self.pref_profile[i].remove(g)

        return dt, self.allocations, self.supply


    def condition_satisfied(self, method, count, time_left):
        if method == 'full':
            return np.max(self.supply) > 0 and count<MAX_ITER

        if method == 'dt=1':
            return time_left > 0 and count<MAX_ITER


    def run_algorithm(self, method='full'):
        count = 1
        time_left = 1
        self.method = method
        while self.condition_satisfied(method, count, time_left):
            print("\n\n count = ", count)
            print("self.supply=", self.supply)
            self.get_eater_info()
            self.count_eaters()
            dt, _, _ = self.eat(time_left)
            time_left -= dt
            count+=1
            print(self.allocations)
            print("time_left=" , time_left)

        if method=='full' and np.max(self.supply) == 0:
            print("Allocation computed")
        if method=='dt=1' and time_left == 0:
            print('Allocation computed for dt=1')
        if count == MAX_ITER:
            print("Error: Max count exceed")

        return self.allocations, self.supply



# a = np.array([[1,2,3,4],
#             [1,3,2,4],
#             [3,4,2,1],
#             [4,3,2,1]],dtype=np.int)

# a = np.array([[1,2,3,4],
#             [1,3,2,4]],dtype=np.int)
# a = a-1
# print(a)
# # print(np.where(a>1))
# prob = probabilistic_serial(a)
# print(prob.pref_profile)
# allocation, supply = prob.run_algorithm(method='dt=1')
# print(allocation)
# print(supply)