from linear_solver import solver_matrix
class Model:
    def __init__(self):
        self.A=[]
        self.num=0
        self.b=[]
        self.c=[]
        self.l={}
        self.d=0

    def addVar(self,type,name):
        if type=='continuous':
            for i in range(len(self.A)):
                self.A[i].append(0)
            self.l[name]=self.num
            self.num+=1
        elif type=='integer':
            for i in range(len(self.A)):
                self.A[i].insert(0,0)
            for key in self.l:
                self.l[key]+=1
            self.l[name]=0
            self.d+=1
            self.num+=1
        elif type=='binary':
            self.addVar('integer',name)
            self.addConstr({name:1},1)
    
    def addConstr(self,equation,bound,type):
        if type=='<=':
            x=[0]*self.num
            for key in equation:
                x[self.l[key]]=equation[key]
            self.A.append(x)
            self.b.append(bound)
        elif type=='>=':
            pass
        elif type=='=':
            pass

    def setObjective(self,equation):
        x=[0]*self.num
        for key in equation:
            x[self.l[key]]=equation[key]
        self.c=x 

    def optimize(self):
        result=solver_matrix(self.A,self.b,self.c,self.d)
        print(result)

########################################################
########################################################
n = 2  # Number of tasks
M = 2000  # Large constant for Big M method
for k in range(1,n):
    # Task times
    t = [4, 3]

    # Waiting time matrix
    A = [[1, 4],
        [3, 2]]
    

    # Create model
    model = Model()

    # Decision variables
    x = {}  # Dictionary to store variables
    for i in range(n):
        for j in range(n):
            if i != j:
                model.addVar('binary',f"x_{i}_{j}")
    
    # for i in range(n):
    #     model.addVar('continuous', f'y_{i}')  # Start times
    #     model.addVar('continuous', f'z_{i}')  # Finish times
    
    # # Constraints: Each task appears once in sequence
    for i in range(n):
        if i!=k:
            equation={}
            for j in range(n):
                if j!=i:
                    equation[f'x_{i}_{j}']=1
            model.addConstr(equation,1)
            equation={}
            for j in range(n):
                if j!=i:
                    equation[f'x_{i}_{j}']=-1
            model.addConstr(equation,-1)
        if i!=0:
            equation={}
            for j in range(n):
                if j!=i:
                    equation[f'x_{j}_{i}']=1
            model.addConstr(equation,1)
            equation={}
            for j in range(n):
                if j!=i:
                    equation[f'x_{j}_{i}']=-1
            model.addConstr(equation,-1)

    # for i in range(n):
    #     if i!=0:
    #         model.addConstr({f'x_{i}_0':1},0)
    #         model.addConstr({f'x_{i}_0':-1},0)
    #     if i!=k:
    #         model.addConstr({f'x_{k}_{i}':1},0)
    #         model.addConstr({f'x_{k}_{i}':-1},0)

    # Task timing constraints
    # for i in range(n):
    #     for j in range(n):
    #         if i != j:
    #             equation={f'y_{j}':-1,f'z_{i}':1,f'x_{i}_{j}':(A[i][j]+M)}
    #             model.addConstr(equation,M)
    #             equation={f'y_{j}':1,f'z_{i}':-1,f'x_{i}_{j}':-(A[i][j]-M)}
    #             model.addConstr(equation,M)

    # Task duration constraints
    # for i in range(n):
    #     model.addConstr({f'z_{i}':1,f'y_{i}':-1},t[i])
    #     model.addConstr({f'z_{i}':-1,f'y_{i}':1},-t[i])

    # for i in range(n):
    #     model.addConstr({f'y_{i}':1},100)
    # Objective function: minimize total cost
    equation={}
    for i in range(n):
        for j in range(n):
            if i!=j:
                equation[f'x_{i}_{j}']=-A[i][j]
    model.setObjective(equation)
    print(model.l)
    print(model.A,model.b,model.c,model.d)
    # Optimize model
    model.optimize()
