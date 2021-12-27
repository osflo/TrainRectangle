import ClassRectangle
import Dpfonction
import random as rd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import copy

#Create a laminar instance (used for 1st presentation and testing)

n=7 #max number of Rectangle in E -1
maxx=28 #maximum value for x-1 and y-1
maxy=30
List_Rect=[]
for i in range(0,n-1):
    xb=rd.randrange(0,maxx-1)
    yb=rd.randrange(0,maxy-1)
    List_Rect.append(ClassRectangle.Rectangle(xb,yb, rd.randrange(xb+1,maxx), rd.randrange(yb+1,maxy)))
E=ClassRectangle.Ensemble(List_Rect)

Origin_Rect=copy.deepcopy(List_Rect) #copy of the original Rectangle list

list_E=Dpfonction.cut_connected_component(E)
for e in list_E:
    e.transform_to_laminar()

fig, ax=plt.subplots(2,sharex=True)
fig.set_figheight(8)
fig.set_figwidth(10)

for r in Origin_Rect:
    ax[0].add_patch(Rectangle((r.xb,r.yb),r.w,(r.yh-r.yb),ec="black",fc=(0,0,1,0.2),lw=2))
    ax[0].plot()

for R in E.Rects:
    ax[1].add_patch(Rectangle((R.xb,R.yb),R.w,(R.yh-R.yb),ec="black",fc=(0,0,1,0.2),lw=2))
    ax[1].plot()

ax[0].set_title('Original instance')
ax[1].set_title('Laminar instance')

ax[0].xaxis.set_major_locator(plt.MultipleLocator(2))
ax[1].xaxis.set_major_locator(plt.MultipleLocator(2))

ax[0].grid()
ax[1].grid()

plt.savefig('laminar_exemple5.png')
plt.show()