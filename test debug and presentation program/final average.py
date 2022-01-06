#compute the average ratio on one file
#to use it its necessary to move the corresponding file to the main directory
f=open('ratio_random_connected_components_after correction.txt','r')
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

avrg=sum(list_ratio)/len(list_ratio)
print(avrg)
print(len(list_ratio))