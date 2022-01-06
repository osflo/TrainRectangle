
#compute the average ratio from different files, 
# to use it its necessary to move the corresponding files from figure to the main directory
f=open('ratio_random.txt','r')
list_ratio=[]

for line in f:
    r=str()
    for char in line:
        if char==' 'or char=='\n':
            if r!='':
                list_ratio.append(float(r))
                r=''
        else:
            r=r+char
    if r!='':
        list_ratio.append(float(r))

f.close()

f=open('ratio_2.txt','r')

for line in f:
    r=str()
    for char in line:
        if char==' 'or char=='\n':
            if r!='':
                list_ratio.append(float(r))
                r=''
        else:
            r=r+char
    if r!='':
        list_ratio.append(float(r))

f.close()

f=open('ratio_allsmall.txt','r')
for line in f:
    r=str()
    for char in line:
        if char==' 'or char=='\n':
            if r!='':
                list_ratio.append(float(r))
                r=''
        else:
            r=r+char
    if r!='':
        list_ratio.append(float(r))

f.close()

f=open('ratio_allsmall2.txt','r')
for line in f:
    r=str()
    for char in line:
        if char==' 'or char=='\n':
            if r!='':
                list_ratio.append(float(r))
                r=''
        else:
            r=r+char
    if r!='':
        list_ratio.append(float(r))

f.close()

f=open('ratio_largebound.txt','r')
for line in f:
    r=str()
    for char in line:
        if char==' 'or char=='\n':
            if r!='':
                list_ratio.append(float(r))
                r=''
        else:
            r=r+char
    if r!='':
        list_ratio.append(float(r))

f.close()

f=open('ratio_smalln_large bound.txt','r')
for line in f:
    r=str()
    for char in line:
        if char==' 'or char=='\n':
            if r!='':
                list_ratio.append(float(r))
                r=''
        else:
            r=r+char
    if r!='':
        list_ratio.append(float(r))

f.close()


avrg=sum(list_ratio)/len(list_ratio)
print(avrg)
print(len(list_ratio))