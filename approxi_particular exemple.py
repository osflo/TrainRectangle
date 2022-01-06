import ClassRectangle
import Dpfonction
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import gurobipy as gp
from gurobipy import GRB

#this file return a figure with 3 subfigures corresponding to the optimal solution, 
# the final solution given by our algorithm and the solution on the laminar instance given by the dynamic program

ratio=0

#example 1 : previous tight instances
#List_Rect=[ClassRectangle.Rectangle(36,1,45,31),ClassRectangle.Rectangle(30,21,47,38)] petit : ClassRectangle.Rectangle(31,25,33,28)
#List_Rect=[ClassRectangle.Rectangle(15,0,34,29),ClassRectangle.Rectangle(16,25,35,28)] ,ClassRectangle.Rectangle(128*2-1,23,128*2+20,28)]
#E=ClassRectangle.Ensemble(List_Rect)

#example 2 : put the coordinates wanted in the order xb,yb,xh,yh for each rectangle
R1=ClassRectangle.Rectangle(0,60,64,81)
R2=ClassRectangle.Rectangle(32,75,64,100)
R3=ClassRectangle.Rectangle(64,9,83,20)
R4=ClassRectangle.Rectangle(60,15,84,22)
E=ClassRectangle.Ensemble([R1,R2,R3,R4])


#exact solution
#create all feasible segments
all_segm=[]
for Rs in E.Rects: #gives start
    for Re in E.Rects: #gives end
        for Rh in E.Rects: #gives hight
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
        if s.h>=R.yb and s.h<=R.yh and s.s<=R.xb and s.e>=R.xh:  # conditions for a segment s to cover rectangle R
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
opti={}
segm_feasible=[]
segm_laminar=[]

list_E=Dpfonction.cut_connected_component(E)
for e in list_E:
    segms=[]
    e.transform_to_laminar()
    Dpfonction.DPstabbing(e,opti,segms)
    segm_laminar.extend(segms)
    local_feasible=Dpfonction.transform_to_feasible(e,segms)
    segm_feasible.extend(local_feasible)
sol_approx=sum(s.l for s in segm_feasible)
sol_laminar=sum(s.l for s in segm_laminar)


#Ratio
ratio=sol_approx/exact_sol

#plot
fig, ax=plt.subplots(3,sharex=True)
fig.set_figheight(8)
fig.set_figwidth(10)

for r in E.Origin_Rect:
    ax[0].add_patch(Rectangle((r.xb,r.yb),r.w,(r.yh-r.yb),ec="black",fc=(0,0,1,0.2),lw=2))
    ax[1].add_patch(Rectangle((r.xb,r.yb),r.w,(r.yh-r.yb),ec="black",fc=(0,0,1,0.2),lw=2))

for se in exact_segm:
    ax[0].plot([se.s,se.e],[se.h,se.h],color='r')

for se in segm_feasible:
    ax[1].plot([se.s,se.e],[se.h,se.h],color='r')

for R in E.Rects:
    ax[2].add_patch(Rectangle((R.xb,R.yb),R.w,(R.yh-R.yb),ec="black",fc=(0,0,1,0.2),lw=2))

for se in segm_laminar:
    ax[2].plot([se.s,se.e],[se.h,se.h],color='r')

#titles
ax[0].set_title('True solution on the original instance, OPT='+str(exact_sol))
ax[1].set_title('Approximate solution on the original instance, ALG='+str(sol_approx))
ax[2].set_title('Dp solution on the laminar instance, LAM='+str(sol_laminar))
fig.suptitle("ratio="+str(ratio)+", length="+str(E.Origin_Rect[0].w))

#tick postion
ax[0].xaxis.set_major_locator(plt.MultipleLocator(4))
ax[1].xaxis.set_major_locator(plt.MultipleLocator(4))
ax[2].xaxis.set_major_locator(plt.MultipleLocator(4))

#show the grid
ax[0].grid()
ax[1].grid()
ax[2].grid()

#plt.savefig('limit'+'length'+str(Origin_Rect[0].w))
plt.show()


