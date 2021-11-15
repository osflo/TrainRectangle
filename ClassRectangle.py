from operator import attrgetter
import math as ma
import copy


class Rectangle:
    def __init__(self,xb,yb,xh,yh):
        #(xb,yb) coordinate of the lower left corner, (xh,yh) coordinate of the upper right corner, w the lenght, must have xb<xh and yb<yh
        self.xb = xb
        self.yb=yb
        self.xh=xh
        self.yh=yh
    
    @property
    def w(self):
        return self.xh-self.xb

class Segment:
    def __init__(self,start,end,h):
        #Construct the segment starting at (s,h) and finishing at (e,h) with lenght l=e-s, must have s<h
        self.s=start
        self.e=end
        self.h=h

    @property
    def l(self):
        return self.e-self.s

class Ensemble:
    def __init__(self,List_Rects):
        #Construct the ensemble of rectangle containing the n rectangles from Rects, minxb/minyb is the smallest coordinate for the left/bottom of a rectangle, 
        # maxxh/maxyh  is the largest coordinate for the right/top of a rectangle, maxRect is the rectangle with the biggest lenght w
        self.Rects=List_Rects
        self.Origin_Rect=copy.deepcopy(List_Rects)
        self.is_laminar=self.test_laminar()
    
    @property
    def n(self):
        return len(self.Rects) #number of rectangles
        
    #coordinate of the frame of the ensemble
    @property
    def minxb(self):
        return min(self.Rects,key=attrgetter('xb')).xb

    @property
    def minyb(self):
        return min(self.Rects,key=attrgetter('yb')).yb

    @property
    def maxxh(self):
        return max(self.Rects,key=attrgetter('xh')).xh

    @property
    def maxyh(self):
        return max(self.Rects,key=attrgetter('yh')).yh

    #Rectangle with the maximum length in the ensemble  
    @property
    def maxRect(self):
        return max(self.Rects,key=attrgetter('w'))

    #name determined by its frame, change if the frame is changed, if empty name is '0'
    @property
    def name(self):
        if self.n==0:
            return '0'
        return str(self.minxb)+','+str(self.minyb)+','+str(self.maxxh)+','+str(self.maxyh)

    #test if laminar
    def test_laminar(self):
        lam=True
        for R1 in self.Origin_Rect: #seen as the "big" one
            for R2 in self.Origin_Rect: #seen as the one included inside
                if (R2.xb>R1.xb and R2.xb<R1.xh and R2.xh>R1.xh) or (R2.xb<R1.xb and R2.xh>R1.xb and R2.xh<R1.xh):
                    lam=False
                    return lam
        return lam
    
    #fonction to transform the general instance into a laminar instance (this change it's name)
    def transform_to_laminar(self):
        if not self.is_laminar:
            for R in self.Rects:
                w=2**(ma.ceil(ma.log2(R.w)))
                R.xb=(R.xb // w)*w
                R.xh=R.xb+w
    
    #fonction to get a smaller sub-ensemble with lower corner (x1,y1) and uper corner (x2,y2)
    def coupure(self,x1,y1,x2,y2):
        return Ensemble([R for R in self.Rects if (R.xb>=x1 and R.yb>=y1 and R.xh<=x2 and R.yh<=y2 )])

    #fonction to get all the Rectangle inside of the maxRect and the maxRect itself
    def inside(self):
        ins=[]
        for R in self.Rects:
            if(R.xb>=self.maxRect.xb and R.xh<=self.maxRect.xh and  R.yh>=self.maxRect.yb and R.yh<=self.maxRect.yh):
                ins.append(R)
        return ins





