import ClassRectangle
import Dpfonction
import random as rd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import gurobipy as gp
from gurobipy import GRB

ratio=0
iter=0
while ratio<8 and iter<10000:
    #creation example
    n=rd.randrange(2,20) #max number of Rectangle in E -1
    maxx=70 #maximum value for x-1 and y-1
    maxy=70
    List_Rect=[]
    for i in range(0,n-1):
        xb=rd.randrange(0,maxx-1)
        yb=rd.randrange(0,maxy-1)
        List_Rect.append(ClassRectangle.Rectangle(xb,yb, rd.randrange(xb+1,maxx), rd.randrange(yb+1,maxy)))
    E=ClassRectangle.Ensemble(List_Rect)

    Origin_Rect=list(List_Rect) #copy of the original Rectangle list

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
    iter+=1

    #write on file
    fr=open("ratio.txt","a")
    if ratio>=3:
        fr.write("\n")
    fr.write(str(ratio)+" ")
    fr.close

    if ratio>=3.8 or ratio<=1.65:
        f=open("Rectangle_and_ratio.txt","a")
        f.write("ratio="+str(ratio)+" Rectangles:")
        for R in E.Rects:
            f.write("[("+str(R.xb)+","+str(R.yb)+") , ("+str(R.xh)+","+str(R.yh)+")]")
        f.write("\n")
        f.close


    if ratio>=4 or ratio<=1.5:
        fig, ax=plt.subplots(2)

        for R in Origin_Rect:
            ax[0].add_patch(Rectangle((R.xb,R.yb),R.w,(R.yh-R.yb),ec="black",fc=(0,0,1,0.2),lw=2))

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

        ax[0].grid()
        ax[1].grid()
        plt.title("ratio="+str(ratio))
        nom="ratio"+str(ratio)+".jpg"
        plt.savefig(nom)
        plt.show()
        print(Origin_Rect)
        print(ratio)

if ratio>=8:
    print("!!!")