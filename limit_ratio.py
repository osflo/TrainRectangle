import ClassRectangle
import Dpfonction
import random as rd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import gurobipy as gp
from gurobipy import GRB
import copy


maxpower= 14 #must be odd for good graph if //2
if maxpower<=7: #plot the figures
    fig, ax=plt.subplots(2,maxpower//2+1)
    fig.set_figheight(12)
    fig.set_figwidth(25)

else:#plot a graph
    fig=plt.figure(figsize=(10,10))
    power2=[]
    list_ratio=[]


for power in range(0,maxpower+1):
    #
    List_Rect=[ClassRectangle.Rectangle(2**(power+1)-1,0,2**(power+1)-1+2**power+1,29),ClassRectangle.Rectangle(2**(power+1),25,2**(power+1)+2**power+1,28),ClassRectangle.Rectangle(2**(power+2)-1,23,2**(power+2)+1,28)]
    E=ClassRectangle.Ensemble(List_Rect)  


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
    segm_feasible=Dpfonction.transform_to_feasible(E,segms)
    sol_approx=sum(s.l for s in segm_feasible)
    

    #Ratio
    ratio=sol_approx/exact_sol

    #plot
    if maxpower<=7:
        if power<=maxpower//2:
            for R in E.Origin_Rect:
                ax[0,power].add_patch(Rectangle((R.xb,R.yb),R.w,(R.yh-R.yb),ec="black",fc=(0,0,1,0.2),lw=2))
        
            for se in segm_feasible:
                ax[0,power].plot([se.s,se.e],[se.h,se.h],color='r')

            ax[0,power].set_title('ratio={:.3f}, start={:}, lenght={:.3f}'.format(ratio,2**(power+1),2**power+1),fontsize=15)
        
            #tick postion
            ax[0,power].xaxis.set_major_locator(plt.MultipleLocator(4))
            ax[0,power].grid()

        else:
            for R in E.Origin_Rect:
                ax[1,power-maxpower//2-1].add_patch(Rectangle((R.xb,R.yb),R.w,(R.yh-R.yb),ec="black",fc=(0,0,1,0.2),lw=2))
        
            for se in segm_feasible:
                ax[1,power-maxpower//2-1].plot([se.s,se.e],[se.h,se.h],color='r')

            ax[1,power-maxpower//2-1].set_title('ratio={:.3f}, start={:}, lenght={:.3f}'.format(ratio,2**(power+1),2**power+1),fontsize=15)
        
            #tick postion
            if power<=6:
                ax[1,power-maxpower//2-1].xaxis.set_major_locator(plt.MultipleLocator(32))
            else:
                ax[1,power-maxpower//2-1].xaxis.set_major_locator(plt.MultipleLocator(64))
            ax[1,power-maxpower//2-1].grid()

    else:
        power2.append(power)
        list_ratio.append(ratio)


if maxpower<=7:
    fig.suptitle('Limit of the ratio',fontsize=25)
    plt.savefig('limit_ratio_aftermodif_to_line'+str(maxpower))

else:
    plt.plot(power2,list_ratio)
    plt.plot(power2,[8 for p in power2])
    plt.title('Convergence of the ratio to 8')
    plt.savefig('limit_ratio_conv_need2_aftermodif')