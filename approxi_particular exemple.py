import ClassRectangle
import Dpfonction
import random as rd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import gurobipy as gp
from gurobipy import GRB
import copy

ratio=0


#creation example
#List_Rect=[ClassRectangle.Rectangle(36,1,45,31),ClassRectangle.Rectangle(30,21,47,38)]
List_Rect=[ClassRectangle.Rectangle(15,0,24,29),ClassRectangle.Rectangle(16,25,25,28),ClassRectangle.Rectangle(31,25,33,28)]
E=ClassRectangle.Ensemble(List_Rect)

Origin_Rect=copy.deepcopy(List_Rect) #copy of the original Rectangle list

#exact sol
#create all feasible segments
all_segm=[]
for i in range(E.minxb,E.maxxh):
    for j in range(i+1,E.maxxh+1):
        for h in range(E.minyb,E.maxyh+1):
            all_segm.append(ClassRectangle.Segment(i,j,h))

    #create list of weight/lenght
w=[s.l for s in all_segm]

    #create M
M = np.zeros((E.n, len(all_segm)))  # build matrix of set cover constraints
i=0
j=0
for i in range(E.n):
    R=E.Rects[i]
    for j in range(len(all_segm)):
        s=all_segm[j]
        if s.h>=R.yb and s.h<=R.yh and s.s<=R.xb and s.e>=R.xh:  # conditions for a segment s to cover rectangle a
            M[i][j] = 1
        else:
            M[i][j] = 0
            
#solve IP
m = gp.Model("stab1")  # model IP
x = m.addMVar(shape=len(all_segm), vtype=GRB.BINARY, name="x")  # variables
obj=np.array(w) #objective function coefficients (weights)
rhs = np.ones(E.n)
m.setObjective(obj @ x, GRB.MINIMIZE)  # define objective function
m.addConstr(M @ x >= rhs, name='c')
m.optimize()
exact_sol=m.objVal

#approximation solution
E.transform_to_laminar()
opti={}
segms=[]
Dpfonction.DPstabbing(E,opti,segms)
segm_feasible=Dpfonction.transform_to_feasible(segms)
sol_approx=opti[E.name]*2
print(sol_approx)

#Ratio
ratio=sol_approx/exact_sol




fig, ax=plt.subplots(2)

for r in Origin_Rect:
    ax[0].add_patch(Rectangle((r.xb,r.yb),r.w,(r.yh-r.yb),ec="black",fc=(0,0,1,0.2),lw=2))

for se in segm_feasible:
    ax[0].plot([se.s,se.e],[se.h,se.h],color='r')

for R in E.Rects:
    ax[1].add_patch(Rectangle((R.xb,R.yb),R.w,(R.yh-R.yb),ec="black",fc=(0,0,1,0.2),lw=2))

for se in segms:
    ax[1].plot([se.s,se.e],[se.h,se.h],color='r')

ax[0].set_title('Final solution on the original rectangles')
ax[1].set_title('Dp solution on the laminar instance')

#tick postion
ax[0].xaxis.set_major_locator(plt.MultipleLocator(4))
ax[1].xaxis.set_major_locator(plt.MultipleLocator(4))
plt.title("ratio="+str(ratio))
ax[0].grid()
ax[1].grid()
plt.show()
print(ratio)

