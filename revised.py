import numpy as np

def simplex(A: np.ndarray,b:np.ndarray,c:np.ndarray,B=None):
    #We implement the revised simplex method, the constraints are Ax<=b, x>=0 and we want to maximize c*x.
    #We assume b>=0.
    m,n=A.shape
    A=np.hstack((A,np.eye(m,dtype=np.float64)))
    c=np.concatenate((c,np.zeros(m,dtype=np.float64)))
    #B keeps track of the basic variables.
    if B==None:
        B=list(range(n,m+n))
    while True:  
        N=[i for i in range(n+m) if i not in B]
        #x_B=A_B^{-1}*b
        x_B=np.linalg.solve(A[:,B],b)
        #y solves y=c_B*A_B^{-1}
        y=np.linalg.solve(A[:,B].T,c[B])
        #z=c_N-c_B*B^(-1)*A_N
        z=c[N]-y@A[:,N]
        if max(z)<=0:
            values=[0]*(n+m)
            for i in range(len(B)):
                values[B[i]]=x_B[i]
            return (np.dot(x_B,c[B]),values[:n],B)
        last_seen=None
        pivot_col=None
        for i in range(len(z)):
            if z[i]>0 and N[i]==0:
                pivot_col=0
                break
            elif z[i]>0 and N[i]!=0:
                last_seen=i
        if pivot_col==None:
            pivot_col=last_seen
        a=A[:,pivot_col]
        d=np.linalg.solve(A[:,B],a)
        if max(d)<=0:
            raise Exception
        pivot_row=None
        max_increase=float('inf')
        for i in range(len(d)):
            if d[i]>0:
                if x_B[i]/d[i]<max_increase:
                    max_increase=x_B[i]/d[i]
                    pivot_row=i
        B[pivot_row]=pivot_col

def auxilliary(A: np.ndarray,b:np.ndarray):
    #The auxilliary problem determines if Ax<=b, x>=0 is feasible. Here, at least one entry of b is negative.
    m,n=A.shape
    #We first add an auxilliary variable and the slack variables.
    A=np.hstack((np.full((m,1),-1,dtype=np.float64),A,np.eye(m,dtype=np.float64)))
    c=np.concatenate((np.array([-1]),np.zeros(n+m,dtype=np.float64)))
    row_num=np.argmin(b)
    A[row_num]*= -1
    b[row_num]*= -1
    for i in range(m):
        if i == row_num:
            continue
        A[i]+=A[row_num]
        b[i]+=b[row_num]
    c+=A[row_num]
    y=b[row_num]
    (result,values,B)=simplex(A,b,c)
    return (result-y,B)

def two_phase(A: np.ndarray,b:np.ndarray,c:np.ndarray):
    m,n=A.shape
    #In the two_phase function, we remove the restriction b>=0 in the simplex method.
    if min(b)>=0:
        (result,values,B)=simplex(A,b,c)
        return (result,values[:n])
    (result,B)=auxilliary(A,b)
    if result<0:
        #The system is infeasible.
        raise Exception
    else:
        for i in range(len(B)):
            B[i]-=1
        A=np.hstack((A,np.eye(m,dtype=np.float64)))
        c=np.concatenate((c,np.zeros(m,dtype=np.float64)))
        (result,values,B)=simplex(A,b,c,B)
        return (result,values[:n])
    

    

A=np.array([[2,3],[-1,4]],dtype=np.float64)
b=np.array([12,23],dtype=np.float64)
c=np.array([1,1],dtype=np.float64)
print(two_phase(A,b,c))
        
import gurobipy as gp
from gurobipy import GRB
import numpy as np

def solve_lp(A, b, c):
    m, n = A.shape
    
    # Create a new model
    model = gp.Model()
    
    # Add variables x >= 0
    x = model.addMVar(n, lb=0, name="x")
    
    # Set objective: maximize c * x
    model.setObjective(c @ x, GRB.MAXIMIZE)
    
    # Add constraints Ax <= b
    model.addMConstr(A, x, "<=", b)
    
    # Optimize model
    model.optimize()
    print(model.display())
    # Extract solution
    if model.status == GRB.OPTIMAL:
        return x.X
    else:
        return None

solution = solve_lp(A, b, c)
print("Optimal solution:", solution)
        






