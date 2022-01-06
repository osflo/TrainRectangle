import ClassRectangle
import Dpfonction
import random as rd
import matplotlib.pyplot as plt
import time
import numpy as np

#this file was used to debug the program, it plot the time taken for different operations and compare
#the time the algorithm take with and without division into connected components
N=[20,30,40,50]#number of rectangles
maxx=40       #change in the possible higher values of x and y
Timeconn=[]
Timenorm=[]
TIC=[]

List_Rect=[]
for n in N:
    for i in range(0,n-1):
        xb=rd.randrange(0,maxx-1)
        yb=rd.randrange(0,maxx-1)
        List_Rect.append(ClassRectangle.Rectangle(xb,yb, rd.randrange(xb+1,maxx), rd.randrange(yb+1,maxx)))
    E=ClassRectangle.Ensemble(List_Rect)
    opti={}
    segm_feasible=[]

    
    #with connected
    list_E=Dpfonction.cut_connected_component(E)
    start_timeconn=time.time()
    tic=time.time()-start_timeconn
    TIC.append(tic)
    for e in list_E:
        start=time.time()-start_timeconn
        segms=[]
        e.transform_to_laminar()
        tic=time.time()-start
        TIC.append(tic)
        Dpfonction.DPstabbing(e,opti,segms)
        tic=time.time()-start
        TIC.append(tic)
        local_feasible=Dpfonction.transform_to_feasible(e,segms)
        tic=time.time()-start
        TIC.append(tic)
        segm_feasible.extend(local_feasible)
        tic=time.time()-start
        TIC.append(tic)

    sol_approx=sum(s.l for s in segm_feasible)
    end_time=time.time()
    Timeconn.append(end_time-start_timeconn)
    

    #main without connected
    start_timenorm=time.time()
    E.transform_to_laminar()
    opti={}
    segms=[]
    Dpfonction.DPstabbing(E,opti,segms)
    segm_feasible=Dpfonction.transform_to_feasible(E,segms)
    end_time=time.time()
    Timenorm.append(end_time-start_timenorm)

fig,ax=plt.subplots(2)
ax[0].scatter(N,Timeconn,color='r')
ax[0].scatter(N,Timenorm)
ax[0].set_yscale('log')

ax[1].scatter(np.arange(1,len(TIC)+1,1),TIC)
ax[1].set_yscale('log')

plt.show()

