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
            for key in equation:
                equation[key]*=(-1)
                self.addConstr(equation,-bound,'<=')
        elif type=='=':
            self.addConstr(equation,bound,'<=')
            self.addConstr(equation,bound,'>=')

    def setObjective(self,equation):
        x=[0]*self.num
        for key in equation:
            x[self.l[key]]=equation[key]
        self.c=x 

    def optimize(self):
        result=solver_matrix(self.A,self.b,self.c,self.d)
        print(result)
