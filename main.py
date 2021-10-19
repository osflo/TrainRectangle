import ClassRectangle
import Dpfonction
import random as rd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np


"""
#test exemple 1
R1=ClassRectangle.Rectangle(1,2,2,4)
R2=ClassRectangle.Rectangle(2,3,5,5)
R3=ClassRectangle.Rectangle(4,8,5,9)
R4=ClassRectangle.Rectangle(4,2,5,5)
E=ClassRectangle.Ensemble([R1,R2,R3,R4])



"""
#test exemple 2,
n=rd.randrange(1,20) #max number of Rectangle in E -1
maxx=100 #maximum value for x-1 and y-1
maxy=100
List_Rect=[]
for i in range(0,n-1):
    xb=rd.randrange(0,maxx-1)
    yb=rd.randrange(0,maxy-1)
    List_Rect.append(ClassRectangle.Rectangle(xb,yb, rd.randrange(xb+1,maxx), rd.randrange(yb+1,maxy)))
E=ClassRectangle.Ensemble(List_Rect)

fig, ax=plt.subplots()


#main
E.transform_to_laminar()

opti={}
segms=[]
Dpfonction.DPstabbing(E,opti,segms)
#Dpfonction.transform_to_feasible(segms)
print(opti[E.name]*2)

#plot : faire le plot pour laminar et le vrai

for R in E.Rects:
    rgb = np.random.rand(3, )
    ax.add_patch(Rectangle((R.xb,R.yb),R.w,(R.yh-R.yb),ec="black",fc="None"))

for se in segms:
    ax.plot([se.s,se.e],[se.h,se.h],color='r')

plt.show()

#longuer algo/opt <8, ex big diff
