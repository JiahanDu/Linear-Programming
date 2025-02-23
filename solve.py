import numpy as np
def simplex(x: np.ndarray,b:np.ndarray,z:np.ndarray,a:int,vector:np.ndarray,extra_1=None,extra_2=None):
    # z is used to denote the objective function. If all entries of z is nonpositive, then -a is the maximum value.
    if max(z)<=0:
        return -a
    # On the other hand, if there is an entry of z is positive, we find the biggest number of z.
    pivot_column=np.argmax(z)
    #pivot_column is the pivot column.
    rows={}
    for i in range(len(x)):
        #For every row i such that x[i][pivot_column]>0, we record b[i]/x[i][pivot_column],
        # this is as much as we can increase variable pivot_column
        if x[i][pivot_column]>0:
            rows[i]=b[i]/x[i][pivot_column]        
    pivot_row=min(rows,key=rows.get) 
    #pivot_row is the pivot row. 
    #We now perform row reductions.
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
    #We update the non free variable for pivot_row is pivot_column.
    vector[pivot_row]=pivot_column
    if extra_1 is not None:
        y=extra_1[pivot_column]
        extra_1-=y*x[pivot_row]
        extra_2[0]-=y*b[pivot_row]
    #Perform the last row operation.
    return simplex(x,b,z,a,vector,extra_1,extra_2)


def solve(A:np.ndarray, b:np.ndarray, c:np.ndarray):
    #The solve function implements the simplex method and maximizes the objective function.
    #The constraints are Ax<=b, Px=r, x>=0 and the objective function is c*x.
    #We introduce slack variables.
    if min(b)>=0:
        A=np.hstack((A,np.eye(len(b),dtype=np.float64)))
        c=np.concatenate((c,np.zeros(len(b),dtype=np.float64)))
        #We use vector to keep track of non free variables.
        vector=len(A[0])-len(A)+np.array(list(range(len(b))))
        ans=simplex(A,b,c,0,vector)
        values=[0.0]*len(A[0])
        for i in range(len(vector)):
            values[vector[i]]=b[i]
        return (ans,values[:len(A[0])-len(A)])
    else:
        #If there are negative terms in b, we introduce an auxilliary variable, we want to maximize the auxilliary variable.
        A=np.insert(A, 0,-1,axis=1)
        #d is the objective function for the auxilliary problem.
        d=np.zeros(len(A[0]))
        d[0]=-1
        A=np.array(A,dtype=np.float64)
        b=np.array(b,dtype=np.float64)
        #vector keeps track of the non free variables.
        vector=len(A[0])+np.array(list(range(len(b))))
        #c is the original objective function.
        c=np.insert(c,0,0)
        extra_1=np.concatenate((c,np.zeros(len(b),dtype=np.float64)))
        extra_2=np.array([0],dtype=np.float64)
        #We first find the pivot row.
        row_num=np.argmin(b)
        vector[row_num]=0
        A=np.hstack((A,np.eye(len(b),dtype=np.float64)))
        d=np.concatenate((d,np.zeros(len(b),dtype=np.float64)))
        #We do row reductions. We don't need to alter extra_1 or extra_2.
        A[row_num]*=-1
        b[row_num]*=-1
        for i in range(len(A)):
            if i==row_num:
                continue
            A[i]+=A[row_num]
            b[i]+=b[row_num]
        d+=A[row_num]
        result=simplex(A,b,d,b[row_num],vector,extra_1,extra_2)
        #After applying the simplex algorithm, the problem becomes maximizing w, where -w+extra_1*x=extra_2[0], 
        #under the assumption that Ax<=b.
        if result==0 and 0 not in vector:
            #If result=0, the original system is feasible. 0 is not in vector means 0 is not
            #a basic variable. So we simply ignore it.
            vector-=1
            A=np.delete(A,0,axis=1)
            c=extra_1[1:]
            ans=simplex(A,b,c,extra_2[0],vector)
            values=[0.0]*len(A[0])
            for i in range(len(vector)):
                values[vector[i]]=b[i]
            return (ans,values[:len(A[0])-len(A)])
        elif result<0:
            #If result<0, the original system is infeasible, we raise an exception.
            #Recall the objective function for the auxilliary system is (-1)*auxilliary variable.
            raise Exception
        else:
            #If the system is feasible, but 0 is a basic variable, we first need to turn it into a free variable.
            #We first find which row x_0 is in.
            row_num=np.where(vector==0)[0][0]
            #Next we find a nonzero number in that row that isn't the first one.
            col_num=np.where(A[row_num][1:]!=0)[0][0]+1
            #Next we perform row operations.
            y=A[row_num][col_num]
            A[row_num]/=y
            for i in range(len(A)):
                if i!=row_num:
                    A[i]-=A[i][col_num]*A[row_num]
            vector[row_num]=col_num
            y=extra_1[col_num]
            extra_1-=A[row_num]*y
            extra_2[0]-=b[row_num]*y
            #Now that x_0 is a free variable, we can simply ignore it.
            vector-=1
            A=np.delete(A,0,axis=1)
            c=extra_1[1:]
            #We now apply the simplex method.
            ans=simplex(A,b,c,extra_2[0],vector)
            values=[0.0]*len(A[0])
            for i in range(len(vector)):
                values[vector[i]]=b[i]
            return (ans,values[:len(A[0])-len(A)])
        
