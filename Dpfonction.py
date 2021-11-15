from operator import attrgetter
import ClassRectangle
import copy

#main part of the dynamic program, take an Ensemble E on which he operate, a dictionary opti to remember the already computed value and a list segm which contain the segments in the solution
def DPstabbing(E,opti,segm):
    #already computed
    if E.name in opti :
        segs=opti[E.name][1]
        if segs!=[]:
            segm.extend(copy.deepcopy(segs))
        return opti[E.name][0]

    #simple cases
    if E.n==0 : 
        opti[E.name]=[0,[]]
        return 0
    if E.n==1 :
        seg=ClassRectangle.Segment(E.maxRect.xb,E.maxRect.xh,E.maxRect.yh)
        opti[E.name]=[E.maxRect.w,[seg]]
        segm.append(seg)
        return opti[E.name][0]

    #the lenght of the maxRect and the solution of the problem on its left and right
    opti[E.name]=[E.maxRect.w + DPstabbing(E.coupure(E.minxb,E.minyb,E.maxRect.xb,E.maxyh),opti,segm) + DPstabbing(E.coupure(E.maxRect.xh,E.minyb,E.maxxh,E.maxyh),opti,segm),[]]

    #the optimal choice to place the segment to cut btw the top and bottom
    Rins=E.inside()
    optvert=0
    value=False #to record if potvert a true value
    Ropti=E.maxRect
    segmtoadd=[]
    for R in Rins: 
        segmtemp=[]
        tomin=DPstabbing(E.coupure(E.maxRect.xb,E.minyb,E.maxRect.xh,R.yh-1),opti,segmtemp)+DPstabbing(E.coupure(E.maxRect.xb,R.yh+1,E.maxRect.xh,E.maxyh),opti,segmtemp)
        if tomin<optvert or value==False :
            optvert=tomin
            Ropti=R
            value=True
            segmtoadd=copy.deepcopy(segmtemp)

    opti[E.name][0]+=optvert
    opti[E.name][1]=copy.deepcopy(segmtoadd)+[ClassRectangle.Segment(E.maxRect.xb,E.maxRect.xh,Ropti.yh)]
    segm.extend(copy.deepcopy(segmtoadd))
    segm.append(ClassRectangle.Segment(E.maxRect.xb,E.maxRect.xh,Ropti.yh)) 

    return opti[E.name][0]
    

#create the lists to run the DP(not necessary to do a fonction for that ...)
#def initialize():
    opti={}
    segm=[]
    return opti,segm

#transform the set of segment to make a feasible solution for the original problem, check how much augmenting is necessary
def transform_to_feasible(E,segm):
    if not(E.is_laminar):
        segm_feasible=[]
        for s in segm:
            doubled_end=s.e+s.l
            start=doubled_end
            end=s.s
            for R in E.Origin_Rect:
                stabbed=R.xb>=s.s and R.xh<=doubled_end and R.yb<=s.h and R.yh>=s.h
                if ( stabbed and start>=R.xb):
                    start=R.xb
                if (stabbed and end<=R.xh):
                    end=R.xh
            segm_feasible.append(ClassRectangle.Segment(start,end,s.h))
        return segm_feasible
    else:
        return segm