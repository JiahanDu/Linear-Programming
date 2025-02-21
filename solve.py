import numpy as np
def reduce(x: np.ndarray,b:np.ndarray,z:np.ndarray,a:int,vector:list[int],extra_1=None,extra_2=None):
    # The solve function assumes that each term of b is nonnegative.
    if max(z)<=0:
        return -a
    #If all numbers in the last row are nonpositive, then the problem has been solved.
    pivot_column=np.argmax(z)
    #pivot_column is the pivot column.
    rows={}
    for i in range(len(x)):
        if x[i][pivot_column]>0:
            rows[i]=b[i]/x[i][pivot_column]
    pivot_row=None
    min_=float('inf')
    for key in rows:
        if rows[key]<min_:
            pivot_row=key
            min_=rows[key]
    #pivot_row is the pivot row.
    y=x[pivot_row][pivot_column]
    x[pivot_row]/=y
    b[pivot_row]/=y
    for i in range(len(x)):
        if i==pivot_row:
            continue
        y=x[i][pivot_column]
        x[i]-=y*x[pivot_row]
        b[i]-=y*b[pivot_row]
    y=z[pivot_column]
    z-=y*x[pivot_row]
    a-=y*b[pivot_row]
    vector[pivot_row]=pivot_column
    if extra_1 is not None:
        y=extra_1[pivot_column]
        extra_1-=y*x[pivot_row]
        extra_2[0]-=y*b[pivot_row]
    #Perform the necessary row operation.
    return reduce(x,b,z,a,vector,extra_1,extra_2)


def solve(A:np.ndarray, b:np.ndarray, c:np.ndarray):
    #The solve function implements the simplex method. 
    #The solve function maximizes.
    if min(b)>=0:
        A=np.hstack((A,np.eye(len(b),dtype=np.float64)))
        c=np.concatenate((c,np.zeros(len(b),dtype=np.float64)))
        vector=len(A[0])-len(A)+np.array(list(range(len(b))))
        ans=reduce(A,b,c,0,vector)
        values=[0.0]*len(A[0])
        for i in range(len(vector)):
            values[vector[i]]=b[i]
        return (ans,values[:len(A[0])-len(A)])
    else:
        A=np.insert(A, 0,-1,axis=1)
        d=np.zeros(len(A[0]))
        d[0]=-1
        A=np.array(A,dtype=np.float64)
        b=np.array(b,dtype=np.float64)
        vector=len(A[0])+np.array(list(range(len(b))))
        c=np.insert(c,0,0)
        extra_1=np.concatenate((c,np.zeros(len(b),dtype=np.float64)))
        extra_2=np.array([0],dtype=np.float64)
        row_num=np.argmin(b)
        vector[row_num]=0
        A=np.hstack((A,np.eye(len(b),dtype=np.float64)))
        d=np.concatenate((d,np.zeros(len(b),dtype=np.float64)))
        A[row_num]*=-1
        b[row_num]*=-1
        for i in range(len(A)):
            if i==row_num:
                continue
            A[i]+=A[row_num]
            b[i]+=b[row_num]
        d+=A[row_num]
        reduce(A,b,d,b[row_num],vector,extra_1,extra_2)
        vector-=1
        A=np.delete(A,0,axis=1)
        c=extra_1[1:]
        ans=reduce(A,b,c,extra_2[0],vector)
        values=[0.0]*len(A[0])
        for i in range(len(vector)):
            values[vector[i]]=b[i]
        return (ans,values[:len(A[0])-len(A)])
