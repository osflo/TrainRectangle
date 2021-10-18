from operator import attrgetter
import ClassRectangle

#main part of the dynamic program, take an Ensemble E on which he operate, a dictionary opti to remember the already computed value and a list segm which contain the segments in the solution
def DPstabbing(E,opti,segm):
    #already computed
    if E.name in opti :
        return opti[E.name]

    #simple cases
    if E.n==0 : 
        opti[E.name]=0
        return 0
    if E.n==1 :
        opti[E.name]=E.maxRect.w
        segm.append(ClassRectangle.Segment(E.maxRect.xb,E.maxRect.xh,E.maxRect.yh))
        return opti[E.name]

    #the lenght of the maxRect and the solution of the problem on its left and right
    opti[E.name]=E.maxRect.w + DPstabbing(E.coupure(E.minxb,E.minyb,E.maxRect.xb,E.maxyh),opti,segm) + DPstabbing(E.coupure(E.maxRect.xh,E.minyb,E.maxxh,E.maxyh),opti,segm) 

    #the optimal choice to place the segment to cut btw the top and bottom
    Rins=E.inside()
    optvert=0
    value=False #to record if potvert a true value
    Ropti=E.maxRect
    for R in Rins: #without loop ? 
        tomin=DPstabbing(E.coupure(E.maxRect.xb,E.minyb,E.maxRect.xh,R.yh-1),opti,segm)+DPstabbing(E.coupure(E.maxRect.xb,R.yh+1,E.maxRect.xh,E.maxyh),opti,segm)
        if tomin<optvert or value==False :
            optvert=tomin
            Ropti=R
            value=True

    opti[E.name]+=optvert
    segm.append(ClassRectangle.Segment(E.maxRect.xb,E.maxRect.xh,Ropti.yh))

    return opti[E.name]
    

#create the lists to run the DP(not necessary to do a fonction for that ...)
#def initialize():
    opti={}
    segm=[]
    return opti,segm

#transform the set of segment to make a feasible solution for the original problem
def transform_to_feasible(segm):
    for s in segm:
        s.e=2*s.e