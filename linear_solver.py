from solve import solve
import numpy as np

def isSolution(x:np.ndarray,d:int):
    for i in range(d):
        if not float.is_integer(x[i]):
            return False
    return True

cur_max=-float('inf')

def search(A:np.ndarray,b:np.ndarray,c:np.ndarray,d:int):
    global cur_max
    #First d variables are integer variables, the rest are continuous variables.
    (max_,values)=solve(A,b,c)
    if max_<=cur_max:
        return
    elif isSolution(values,d):
        cur_max=max_
        return
    else:
        i=0
        while float.is_integer(values[i]):
            i+=1
        x=np.zeros(len(A[0]),dtype=np.float64)
        x[i]=1
        try:
            search(np.append(A,[x],axis=0),np.append(b,max_//1),c,d)
        except:
            pass
        y=np.zeros(len(A[0]),dtype=np.float64)
        y[i]=-1
        try:
            search(np.append(A,[y],axis=0),np.append(b,max_//1+1),c,d)
        except:
            pass

def main(A:list[list[int]],b:list[int],c:list[int],d:int):
    A=np.array(A,dtype=np.float64)
    b=np.array(b,dtype=np.float64)
    c=np.array(c,dtype=np.float64)
    global cur_max
    cur_max=-float('inf')
    search(A,b,c,d)
    return cur_max
