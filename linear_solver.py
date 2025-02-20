from solve import solve
import numpy as np

cur_max=-float('inf')

def isSolution(x:np.ndarray,d:int):
    for i in range(len(d)):
        if not float.is_integer(x[i]):
            return False
    return True

def search(A:np.ndarray,b:np.ndarray,c:np.ndarray,d:int):
    #First d variables are integer variables, the rest are continuous variables.
    (max_,values)=solve(A,b,c)
    