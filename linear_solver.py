from solve import solve
import numpy as np
def isSolution(x:np.ndarray,d:int):
    for i in range(d):
        if not float.is_integer(x[i]):
            return False
    return True

cur_max=-float('inf')
cur_values=None

def search(A:np.ndarray,b:np.ndarray,c:np.ndarray,d:int):
    A_=np.copy(A)
    b_=np.copy(b)
    c_=np.copy(c)
    global cur_max
    global cur_values
    #First d variables are integer variables, the rest are continuous variables.
    try:
        (max_,values)=solve(A,b,c)
        print(max_,values)
    except:
        return
    if max_<=cur_max:
        pass
    elif isSolution(values,d):
        cur_max=max_
        cur_values=values
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

def solver_matrix(A:list[list[int]],b:list[int],c:list[int],d:int):
    A=np.array(A,dtype=np.float64)
    b=np.array(b,dtype=np.float64)
    c=np.array(c,dtype=np.float64)
    global cur_max
    cur_max=0
    cur_max=-float('inf')
    search(A,b,c,d)
    return (cur_max,cur_values)

