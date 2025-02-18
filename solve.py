import numpy as np

def reduce(x: np.ndarray,b:np.ndarray,z:np.ndarray,a:int):
    # The solve function assumes that each term of b is nonnegative.
    if max(z)<=0:
        return -a
    #If all numbers in the last row are nonpositive, then the problem has been solved.
    pivot_column=0
    while z[pivot_column]<=0:
        pivot_column+=1
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
    #Perform the necessary row operation.
    return reduce(x,b,z,a)

def solve(A:list[list[int]], b:list[int], c:list[int]):
    #The solve function implements the simplex method. 
    #The solve function maximizes.
    if min(b)>=0:
        A=np.hstack((np.array(A,dtype=np.float64),np.eye(len(b),dtype=np.float64)))
        b=np.array(b,dtype=np.float64)
        c=np.concatenate((np.array(c,dtype=np.float64),np.zeros(len(b),dtype=np.float64)))
        return reduce(A,b,c,0)
    

print(solve([[3,2,1],[2,5,3]],[10,15],[2,3,4]))


