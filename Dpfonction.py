import ClassRectangle
import copy
import igraph

#main part of the dynamic program, take an Ensemble E on which he operates, 
# a dictionary opti to remember the already computed values and a list segm which contains the segments in the solution
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

    #the optimal choice to place the segment in MaxRect to cut between the top and bottom
    Rins=E.inside()
    optvert=0
    value=False #to record if optvert is a true value
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
    

#transform the set of segments to make a feasible solution for the original problem:
#check how much augmenting is necessary on each sides of a segment
def transform_to_feasible(E,segm):
    if not(E.is_laminar): #if E is laminar no changes are needed
        segm_feasible=[]
        for s in segm:
            doubled_end=s.e+s.l
            start=doubled_end
            end=s.s
            for R in E.Origin_Rect:
                stabbed=R.xb>=s.s and R.xh<=doubled_end and R.yb<=s.h and R.yh>=s.h #if R is stabbed by s
                if ( stabbed and start>=R.xb): #check if the new segment need to be extended to stab R
                    start=R.xb
                if (stabbed and end<=R.xh):
                    end=R.xh
            segm_feasible.append(ClassRectangle.Segment(start,end,s.h))
        return segm_feasible
    else:
        return segm


#To cut the problem into a list of connected component to run seperately the use of graph is necessary
def cut_connected_component(E):
    #E is an ensemble and the fonction return a list of ensemble that can be treated independentaly
    g=igraph.Graph()
    g.add_vertices(E.n) #vertex i will correspond to Rects[i]

    #create an edge if two rectangles are touching each other
    for i in range(0,E.n):
        R1=E.Rects[i]
        for j in range(i+1,E.n):
            R2=E.Rects[j]
            #test if intersect : 1st line test x, 2nd line test y
            if ((R1.xb<=R2.xb and R2.xb<=R1.xh) or (R1.xb<=R2.xh and R2.xh<=R1.xh)or(R2.xb<=R1.xb and R1.xb<=R2.xh) or (R2.xb<=R1.xh and R1.xh<=R2.xh)) \
            and ((R1.yb<=R2.yb and R2.yb<=R1.yh) or (R1.yb<=R2.yh and R2.yh<=R1.yh)or(R2.yb<=R1.yb and R1.yb<=R2.yh) or (R2.yb<=R1.yh and R1.yh<=R2.yh)) :
                g.add_edges([(i,j)])
    
    #find the connected components in the graph
    Conn_comp=g.clusters()

    #associate each connected component in the graph to the corresponding ensemble
    List_E=[]
    for cluster in Conn_comp:
        List_Rect=[]
        for v in cluster:
            List_Rect.append(E.Rects[v])
        List_E.append(ClassRectangle.Ensemble(List_Rect))
    
    return List_E

