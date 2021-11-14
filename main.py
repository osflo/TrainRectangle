import ClassRectangle
import Dpfonction
import random as rd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np




#test exemple 1
R1=ClassRectangle.Rectangle(0,4,8,8)
R2=ClassRectangle.Rectangle(0,3,4,5)
R3=ClassRectangle.Rectangle(2,0,4,1)
R4=ClassRectangle.Rectangle(4,7,6,9)
E=ClassRectangle.Ensemble([R1,R2,R3,R4])

#List_Rect=[ClassRectangle.Rectangle(15,0,34,29),ClassRectangle.Rectangle(16,25,35,28)]
#E=ClassRectangle.Ensemble(List_Rect)


"""

#test exemple 2,
n=rd.randrange(1,10) #max number of Rectangle in E -1
maxx=100 #maximum value for x-1 and y-1
maxy=100
List_Rect=[]
for i in range(0,n-1):
    xb=rd.randrange(0,maxx-1)
    yb=rd.randrange(0,maxy-1)
    List_Rect.append(ClassRectangle.Rectangle(xb,yb, rd.randrange(xb+1,maxx), rd.randrange(yb+1,maxy)))
E=ClassRectangle.Ensemble(List_Rect)
"""

#copy of the original Rectangle list
Origin_Rect=E.Origin_Rect


#main
E.transform_to_laminar()
opti={}
segms=[]
Dpfonction.DPstabbing(E,opti,segms)
segm_feasible=Dpfonction.transform_to_feasible(E,segms)
print(opti[E.name]*2)


#plot :

fig, ax=plt.subplots(2,sharex=True)

rgb = np.random.rand(3, )
for R in Origin_Rect:
    ax[0].add_patch(Rectangle((R.xb,R.yb),R.w,(R.yh-R.yb),ec="black",fc=(0,0,1,0.2),lw=2))

for se in segm_feasible:
    ax[0].plot([se.s,se.e],[se.h,se.h],color='r')

for R in E.Rects:
    ax[1].add_patch(Rectangle((R.xb,R.yb),R.w,(R.yh-R.yb),ec="black",fc=(0,0,1,0.2),lw=2))

for se in segms:
    ax[1].plot([se.s,se.e],[se.h,se.h],color='r')

ax[0].plot()
ax[1].plot()

ax[0].set_title('Final solution on the original rectangles')
ax[1].set_title('Dp solution on the laminar instance')

#tick postion
ax[0].xaxis.set_major_locator(plt.MultipleLocator(4))
ax[1].xaxis.set_major_locator(plt.MultipleLocator(4))

ax[0].grid()
ax[1].grid()
plt.show()



