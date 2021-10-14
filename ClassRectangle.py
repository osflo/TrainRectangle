class Rectangle:
    def __init__(self,xb,yb,xh,yh):
        #(xb,yb) coordinate of the lower left corner, (xh,yh) coordinate of the upper right corner, w the lenght
        self.xb = xb
        self.yb=yb
        self.xh=xh
        self.yh=yh
        self.w=xh-xb

class Segment:
    def __init__(self,start,end,h):
        #Construct the segment starting at (s,h) and finishing at (e,h) with lenght l=e-s
        self.s=start
        self.e=end
        self.h=h
        self.l=end-start

class Ensemble:
    def __init__(self,List_Rects):
        #Construct the ensemble of rectangle containing the n rectangles from Rects, minxb/minyb is the smallest coordinate for the left/bottom of a rectangle, 
        # maxxh/maxyh  is the largest coordinate for the right/top of a rectangle, maxRect is the rectangle with the biggest lenght w
        self.Rects=List_Rects
        self.n=len(List_Rects)
        self.minxb=
        self.minyb=
        self.maxxh=
        self.maxyh=
        self.maxRect=
        


