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
#List_Rect=[ClassRectangle.Rectangle(36,1,45,31),ClassRectangle.Rectangle(30,21,47,38)] petit : ClassRectangle.Rectangle(31,25,33,28)
List_Rect=[ClassRectangle.Rectangle(127,0,192,29),ClassRectangle.Rectangle(128,25,193,28)] #,ClassRectangle.Rectangle(128*2-1,23,128*2+20,28)]
E=ClassRectangle.Ensemble(List_Rect)

Origin_Rect=copy.deepcopy(List_Rect) #copy of the original Rectangle list

#exact sol
#create all feasible segments
all_segm=[]
for Rs in E.Rects: #give start
    for Re in E.Rects: #give end
        for Rh in E.Rects: #give hight
            if Rs.xb<Re.xh:
                all_segm.append(ClassRectangle.Segment(Rs.xb,Re.xh,Rh.yh))


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
exact_segm=[all_segm[i] for i in range(len(all_segm)) if m.x[i]==1]

#approximation solution
E.transform_to_laminar()
opti={}
segms=[]
Dpfonction.DPstabbing(E,opti,segms)
segm_feasible=Dpfonction.transform_to_feasible(segms)
sol_approx=opti[E.name]*2


#Ratio
ratio=sol_approx/exact_sol


fig, ax=plt.subplots(3,sharex=True)
fig.set_figheight(8)
fig.set_figwidth(10)

for r in Origin_Rect:
    ax[0].add_patch(Rectangle((r.xb,r.yb),r.w,(r.yh-r.yb),ec="black",fc=(0,0,1,0.2),lw=2))
    ax[1].add_patch(Rectangle((r.xb,r.yb),r.w,(r.yh-r.yb),ec="black",fc=(0,0,1,0.2),lw=2))

for se in exact_segm:
    ax[0].plot([se.s,se.e],[se.h,se.h],color='r')

for se in segm_feasible:
    ax[1].plot([se.s,se.e],[se.h,se.h],color='r')

for R in E.Rects:
    ax[2].add_patch(Rectangle((R.xb,R.yb),R.w,(R.yh-R.yb),ec="black",fc=(0,0,1,0.2),lw=2))

for se in segms:
    ax[2].plot([se.s,se.e],[se.h,se.h],color='r')

ax[0].set_title('True solution on the orignal instance, OPT='+str(exact_sol))
ax[1].set_title('Approximate solution on the original instance, ALG='+str(sol_approx))
ax[2].set_title('Dp solution on the laminar instance, LAM='+str(opti[E.name]))

#tick postion
ax[0].xaxis.set_major_locator(plt.MultipleLocator(16))
ax[1].xaxis.set_major_locator(plt.MultipleLocator(16))
ax[2].xaxis.set_major_locator(plt.MultipleLocator(16))
fig.suptitle("ratio="+str(ratio)+", length="+str(Origin_Rect[0].w))
ax[0].grid()
ax[1].grid()
ax[2].grid()
plt.savefig('limit'+'length'+str(Origin_Rect[0].w))
plt.show()


