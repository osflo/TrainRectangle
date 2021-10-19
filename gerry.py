import random
import numpy as np
import gurobipy as gp
from gurobipy import GRB
import matplotlib.pyplot as plt

gap=0
counter=0
while gap < 4 and counter<5000:
    l = []
    a = []
    for i in range(200):
        l.append([random.randint(0,50), random.randint(0,50), random.randint(0,50), random.randint(0,50)])
        # l.append(random.sample(rang202010),4))
        #l.append([random.uniform(0, 10), random.uniform(0, 10), random.uniform(0, 10), random.uniform(0, 10)])

    # build list of valid tuples=rectangles (non-empty interior)
    # accept only 'small' rectangles
    for i in range(len(l)):
        if l[i][0] < l[i][1] and l[i][2] < l[i][3] and l[i][1]-l[i][0]<15 and l[i][3]-l[i][2]<30:
            a.append(l[i])

    s1 = []  # build all possible segments
    for m in range(len(a)):
        for j in range(len(a)):
            for k in range(len(a)):
                s1.append([a[m][0], a[j][1], a[k][3]])

    s = []  # feasible segments
    for i in range(len(s1)):
        if s1[i][0] < s1[i][1]:
            s.append(s1[i])

    w = []  # building weights of sets (length of segments)
    for i in range(len(s)):
        w.append(s[i][1] - s[i][0])

    M = np.zeros((len(a), len(s)))  # build matrix of set cover constraints
    for i in range(len(a)):
        for j in range(len(s)):
            if a[i][2] <= s[j][2] and s[j][2] <= a[i][3] and a[i][0] >= s[j][0] and a[i][1] <= s[j][
                1]:  # conditions for a segment s to cover rectangle a
                M[i][j] = 1
            else:
                M[i][j] = 0

    #print(len(a), len(a) ** 3, len(s))
    #print(a)
    #print(s1)
    #print(s)
    #print(w)
    #print(M)

    m2 = gp.Model("stab_lp")  # model LP
    y = m2.addMVar(shape=len(s), lb=0.0, vtype=GRB.CONTINUOUS, name="y")  # variables
    obj = np.array(w)  # objective function coefficients (weights)
    m2.setObjective(obj @ y, GRB.MINIMIZE)  # define objective function
    rhs = np.ones(len(a))
    m2.addConstr(M @ y >= rhs, name='c2')

    m = gp.Model("stab1")  # model IP
    x = m.addMVar(shape=len(s), vtype=GRB.BINARY, name="x")  # variables
    # obj=np.array(w) #objective function coefficients (weights)
    m.setObjective(obj @ x, GRB.MINIMIZE)  # define objective function
    m.addConstr(M @ x >= rhs, name='c')

    m2.optimize()
    m.optimize()
    # cont=[]
    # for i in range(len(y.X)):
    #     if y.X[i] <1 and y.X[i]>0:
    #         cont.append([y.X[i], i])
    #
    # print(cont)
    #print('Obj LP: %g' % m2.objVal)
    #print('Obj IP: %g' % m.objVal)
    gap = m.objVal - m2.objVal
    counter=counter+1
    #print('Gap: %g' %gap)

print('Counter: %g' %counter)
print('Obj LP: %g' % m2.objVal)
print('Obj IP: %g' % m.objVal)
print('Gap: %g' %gap)
print('RECTANGLES')
print(a)
#print(s)
#print(M)
#print(x.X)#binary
#print(y.X)#continuous


indici_bin=[]
for i in range(len(x.X)):
    if x.X[i]>0:
        indici_bin.append([i,x.X[i]]) #creo lista con indice e valore delle variabili non nulle
segm_ip=[]
for i in range(len(indici_bin)):
    segm_ip.append([s[indici_bin[i][0]],x.X[indici_bin[i][0]]]) #creo lista di segmenti utilizzati, con valore della variabile corrispondente

indici_lp=[]
for i in range(len(y.X)):
    if y.X[i]>0:
        indici_lp.append([i, y.X[i]])  # creo lista con indice e valore delle variabili lp non nulle
segm_lp = []
for i in range(len(indici_lp)):
    segm_lp.append([s[indici_lp[i][0]], y.X[indici_lp[i][0]]])  # creo lista di segmenti utilizzati, con valore della variabile corrispondente

print("SEGMENTI IP")
#print(indici_bin)
print(segm_ip)
print("SEGMENTI LP")
#print(indici_lp)
print(segm_lp)

#plot rectangles
fig, axs = plt.subplots(2)
rect=a
coord_rect=[]
for r in range(len(rect)):
    coord_rect.append([[rect[r][0],rect[r][0],rect[r][1],rect[r][1],rect[r][0]],[rect[r][2],rect[r][3],rect[r][3],rect[r][2],rect[r][2]]])
for i in range(len(coord_rect)):
    axs[0].plot(coord_rect[i][0],coord_rect[i][1], color='black', linewidth=0.5)
    axs[1].plot(coord_rect[i][0],coord_rect[i][1], color='black', linewidth=0.5)
#plot segments IP
coord_segm_ip=[]
for i in range(len(segm_ip)):
    coord_segm_ip.append([[segm_ip[i][0][0],segm_ip[i][0][1]],[segm_ip[i][0][2],segm_ip[i][0][2]]])
for i in range(len(coord_segm_ip)):
    axs[0].plot(coord_segm_ip[i][0],coord_segm_ip[i][1], color='r')

#plot segments LP
coord_segm_lp=[]
for i in range(len(segm_lp)):
    coord_segm_lp.append([[segm_lp[i][0][0],segm_lp[i][0][1]],[segm_lp[i][0][2],segm_lp[i][0][2]]])
for i in range(len(coord_segm_lp)):
    axs[1].plot(coord_segm_lp[i][0],coord_segm_lp[i][1], color='green',linestyle='dashed')


plt.show()