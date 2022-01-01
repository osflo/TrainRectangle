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
while ratio<8 and iter<100000:
    #creation example random
    
    n=rd.randrange(3,20) #max number of Rectangle in E -1
    maxx=100 #maximum value for x-1 and y-1
    maxy=100
    List_Rect=[]
    for i in range(0,n-1):
        xb=rd.randrange(0,maxx-1)
        yb=rd.randrange(0,maxy-1)
        List_Rect.append(ClassRectangle.Rectangle(xb,yb, rd.randrange(xb+1,maxx), rd.randrange(yb+1,maxy)))
    E=ClassRectangle.Ensemble(List_Rect)
    """
    #creation exemple with w a 2^k+1
    n=rd.randrange(2,15) #max number of Rectangle in E -1
    maxx=40 #maximum value for x-1 and y-1
    maxy=70
    maxk=4 #7=>128,6=>64,5=>32,4=>16
    List_Rect=[]
    for i in range(0,n-1):
        xb=rd.randrange(0,maxx-1)
        yb=rd.randrange(0,maxy-1)
        k=rd.randrange(0,maxk+1)
        List_Rect.append(ClassRectangle.Rectangle(xb,yb, xb+2**k+1, rd.randrange(yb+1,maxy)))
    E=ClassRectangle.Ensemble(List_Rect)
"""
    

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
    Origin_Rect=E.Origin_Rect
    opti={}
    segm_feasible=[]
    segm_laminar=[]
    name=[]
    list_E=Dpfonction.cut_connected_component(E)
    for e in list_E:
        segms=[]
        e.transform_to_laminar()
        Dpfonction.DPstabbing(e,opti,segms)
        segm_laminar.extend(segms)
        local_feasible=Dpfonction.transform_to_feasible(e,segms)
        segm_feasible.extend(local_feasible)
        name.append(e.name)
    sol_approx=sum(s.l for s in segm_feasible)
    sol_laminar=sum(s.l for s in segm_laminar)
    

    #Ratio
    ratio=sol_approx/exact_sol
    iter+=1

    #write on file
    
    fr=open("ratio_random_connected_components_after correction.txt","a")
    if ratio>=1.2:
        fr.write("\n")
    fr.write(str(ratio)+" ")
    fr.close()
    

    
    if ratio>=1.8 :
        f=open("ratio_and_Rect_connectedcomponents_description_after correction.txt","a")
        f.write("ratio="+str(ratio)+" Rectangles:")
        for R in E.Origin_Rect:
            f.write("[("+str(R.xb)+","+str(R.yb)+") , ("+str(R.xh)+","+str(R.yh)+")]")
        f.write("\n")
        for n in name:
            f.write(n +' ')
        f.write("\n")
        f.write("\n")
        f.close()
    

    if ratio>=2.0 :

        fig, ax=plt.subplots(3,sharex=True)
        fig.set_figheight(8)
        fig.set_figwidth(10)

        for R in E.Origin_Rect:
            ax[0].add_patch(Rectangle((R.xb,R.yb),R.w,(R.yh-R.yb),ec="black",fc=(0,0,1,0.2),lw=2))
            ax[1].add_patch(Rectangle((R.xb,R.yb),R.w,(R.yh-R.yb),ec="black",fc=(0,0,1,0.2),lw=2))

        for se in exact_segm:
            ax[0].plot([se.s,se.e],[se.h,se.h],color='r')

        for se in segm_feasible:
            ax[1].plot([se.s,se.e],[se.h,se.h],color='r')

        for R in E.Rects:
            ax[2].add_patch(Rectangle((R.xb,R.yb),R.w,(R.yh-R.yb),ec="black",fc=(0,0,1,0.2),lw=2))

        for se in segm_laminar:
            ax[2].plot([se.s,se.e],[se.h,se.h],color='r')

        ax[0].set_title('True solution on the orignal instance, OPT='+str(exact_sol))
        ax[1].set_title('Approximate solution on the original instance, ALG='+str(sol_approx))
        ax[2].set_title('Dp solution on the laminar instance, LAM='+str(sol_laminar))

        #tick postion
        ax[0].xaxis.set_major_locator(plt.MultipleLocator(4))
        ax[1].xaxis.set_major_locator(plt.MultipleLocator(4))
        ax[2].xaxis.set_major_locator(plt.MultipleLocator(4))

        ax[0].grid()
        ax[1].grid()
        ax[2].grid()
        fig.suptitle("ratio="+str(ratio)+", connected component:"+str(len(list_E))+", n="+str(E.n))
        nom="ratio"+str(ratio)+"iter"+str(iter)+'.png'
        plt.savefig(nom)

