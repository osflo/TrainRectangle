import ClassRectangle
import Dpfonction
import random as rd
import matplotlib.pyplot as plt
import time
import numpy as np

N=10*np.arange(1,70)
maxXY=[100]
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

        #main
        E.transform_to_laminar()

        opti={}
        segms=[]
        Dpfonction.DPstabbing(E,opti,segms)
        segm_feasible=Dpfonction.transform_to_feasible(segms)
        sol_approx=opti[E.name]*2
        end_time=time.time()
        Time.append(end_time-start_time)
    plt.semilogy(N,Time,label='max(xh,yh)='+str(maxx))
X=[i for i in range(0,N[-1])]
X5=[10**(-8)*x**5 for x in X]
X4=[10**(-8)*x**4 for x in X]
plt.semilogy(X,X5,label='growth in n^5')
plt.semilogy(X,X4,label='growth in n^4')
plt.title('Time to run the algorithm in fonction of the number of rectangle n')
plt.ylabel('time in s')
plt.xlabel('n')
plt.legend()
plt.savefig('test_complexity')
plt.show()


