import numpy as np
def reduce(x: np.ndarray,b:np.ndarray,z:np.ndarray,a:int,vector:list[int],extra_1=None,extra_2=None):
    print("This is an iteration:")
    print(x)
    print(b)
    print(z)
    print(vector)
    print(".................................")
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


def solve(A:list[list[int]], b:list[int], c:list[int]):
    #The solve function implements the simplex method. 
    #The solve function maximizes.
    if min(b)>=0:
        A=np.array(A,dtype=np.float64)
        b=np.array(b,dtype=np.float64)
        c=np.array(c,dtype=np.float64)
        A=np.hstack((A,np.eye(len(b),dtype=np.float64)))
        c=np.concatenate((c,np.zeros(len(b),dtype=np.float64)))
        vector=len(A[0])-len(A)+np.array(list(range(len(b))))
        ans=reduce(A,b,c,0,vector)
        values=[0]*len(A[0])
        for i in range(len(vector)):
            values[vector[i]]=b[i]
        return (ans,values[:len(A[0])-len(A)])
    else:
        for i in range(len(A)):
            A[i].insert(0,-1)
        d=np.zeros(len(A[0]))
        d[0]=-1
        A=np.array(A,dtype=np.float64)
        b=np.array(b,dtype=np.float64)
        vector=len(A[0])+np.array(list(range(len(b))))
        print("..............",vector)
        c.insert(0,0)
        c=np.array(c,dtype=np.float64)
        extra_1=np.concatenate((c,np.zeros(len(b),dtype=np.float64)))
        extra_2=np.array([0],dtype=np.float64)
        row_num=np.argmin(b)
        vector[row_num]=0
        print("..............",vector)
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
        values=[0]*len(A[0])
        for i in range(len(vector)):
            values[vector[i]]=b[i]
        return (ans,values[:len(A[0])-len(A)])

#Test case 0:
#print(solve([[2,3,1],[4,1,2],[3,4,2]],[5,11,8],[5,4,3]))
#Test case 1 
# print(solve([[2,-1,2],[2,-3,1],[-1,1,-2]],[4,-5,-1],[1,-1,1]))
import gurobipy as grb
# model=grb.Model('test')
# x=model.addVar(name='x')
# y=model.addVar(name='y')
# z=model.addVar(name='z')
# model.setObjective(x-y+z,grb.GRB.MAXIMIZE)
# model.addConstr(2*x-y+2*z<=4)
# model.addConstr(2*x-3*y+z<=-5)
# model.addConstr(-x+y-2*z<=-1)
# model.addConstr(x>=0)
# model.addConstr(y>=0)
# model.addConstr(z>=0)
# model.optimize()
# print(model.objVal)
# for v in model.getVars():
#     print(f"{v.VarName} = {v.X}")

# #Test case 2
print(solve([[2,3,-1],[3,2,-40],[4,2,5.5]],[-20,180,200],[8,6,10]))
model=grb.Model("test")
x=model.addVar(name='x')
y=model.addVar(name='y')
z=model.addVar(name='z')
model.setObjective(8*x+6*y+10*z,grb.GRB.MAXIMIZE)
model.addConstr(2*x+3*y-z<=-20)
model.addConstr(3*x+2*y-40*z<=180)
model.addConstr(4*x+2*y+5.5*z<=200)
model.addConstr(x>=0)
model.addConstr(y>=0)
model.addConstr(z>=0)
model.optimize()
print(model.ObjVal)
for v in model.getVars():
    print(f"{v.VarName} = {v.X}")
