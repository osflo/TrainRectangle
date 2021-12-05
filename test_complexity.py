import ClassRectangle
import Dpfonction
import random as rd
import matplotlib.pyplot as plt
import time
import numpy as np

N=10*np.arange(1,20) #number of rectangles
maxXY=[40]       #change in the possible higher values of x and y
fig=plt.figure()
for maxx in maxXY:
    Time=[]
    for n in N:
        start_time=time.time()
        List_Rect=[]
        for i in range(0,n-1):
            xb=rd.randrange(0,maxx-1)
            yb=rd.randrange(0,maxx-1)
            List_Rect.append(ClassRectangle.Rectangle(xb,yb, rd.randrange(xb+1,maxx), rd.randrange(yb+1,maxx)))
        E=ClassRectangle.Ensemble(List_Rect)

        opti={}
        segm_feasible=[]
        list_E=Dpfonction.cut_connected_component(E)
        for e in list_E:
            segms=[]
            e.transform_to_laminar()
            Dpfonction.DPstabbing(e,opti,segms)
            local_feasible=Dpfonction.transform_to_feasible(e,segms)
            segm_feasible.extend(local_feasible)

        sol_approx=sum(s.l for s in segm_feasible)

        end_time=time.time()
        Time.append(end_time-start_time)
    plt.semilogy(N,Time,label='max(xh,yh)='+str(maxx))
X=[i for i in range(0,N[-1])]
X5=[10**(-8)*x**5 for x in X]
X4=[10**(-8)*x**4 for x in X]
X3=[10**(-8)*x**3 for x in X]
plt.semilogy(X,X5,label='growth in n^5')
plt.semilogy(X,X4,label='growth in n^4')
plt.semilogy(X,X3,label='growth in n^3')
plt.title('Time to run the algorithm in fonction of the number of rectangle n')
plt.ylabel('time in s')
plt.xlabel('n')
plt.legend()
plt.savefig('test_complexity_after_change')
plt.show()


