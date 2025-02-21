from solve import solve
import numpy as np
import random
def isSolution(x:np.ndarray,d:int):
    for i in range(d):
        if not float.is_integer(x[i]):
            return False
    return True

cur_max=-float('inf')

def search(A:np.ndarray,b:np.ndarray,c:np.ndarray,d:int):
    A_=np.copy(A)
    b_=np.copy(b)
    c_=np.copy(c)
    global cur_max
    print(cur_max)
    #First d variables are integer variables, the rest are continuous variables.
    try:
        (max_,values)=solve(A,b,c)
    except:
        return
    if max_<=cur_max:
        pass
    elif isSolution(values,d):
        cur_max=max_
    else:
        i=0
        while float.is_integer(values[i]):
            i+=1
        x=np.zeros(len(A[0]),dtype=np.float64)
        x[i]=1
        try:
            search(np.append(A_,[x],axis=0),np.append(b_,float(values[i]//1)),c_,d)
        except:
            pass
        y=np.zeros(len(A[0]),dtype=np.float64)
        y[i]=-1
        try:
            search(np.append(A_,[y],axis=0),np.append(b_,-float(values[i]//1+1)),c_,d)
        except:
            pass

def main(A:list[list[int]],b:list[int],c:list[int],d:int):
    A=np.array(A,dtype=np.float64)
    b=np.array(b,dtype=np.float64)
    c=np.array(c,dtype=np.float64)
    global cur_max
    cur_max=0
    cur_max=-float('inf')
    search(A,b,c,d)
    return cur_max
#####################################
#####################################
#Test case:
# Problem size
n = 100  # number of variables (size of x)
m = 100  # number of constraints
k = 50   # first k variables are integer
A=[]
for i in range(n):
    A.append([])
    for j in range(m):
        A[i].append(10*random.random())
b=[]
for i in range(m):
    b.append(1000000*random.random())
c=[]
for i in range(n):
    c.append(random.random())
print(main(A,b,c,k))

import gurobipy as gp
from gurobipy import GRB
import numpy as np
model = gp.Model("milp_example")

x_continuous = model.addVars(range(k, n), vtype=GRB.CONTINUOUS, lb=0, name="x_cont")
x_integer = model.addVars(range(k), vtype=GRB.INTEGER, lb=0, name="x_int")
x = {**x_integer, **x_continuous}

model.setObjective(gp.quicksum(c[i] * x[i] for i in range(n)), GRB.MAXIMIZE)

for i in range(m):
    model.addConstr(gp.quicksum(A[i][j] * x[j] for j in range(n)) <= b[i], f"c{i}")

model.optimize()

# Print the maximized value of the objective
if model.status == GRB.OPTIMAL:
    print(f"Maximized objective value: {model.objVal}")
else:
    print("No optimal solution found")
