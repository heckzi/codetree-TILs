sum=0
i=0
temp=[]
temp=list(map(int,input().split()))
while 1:
    if(temp[i]==0):
        sum=temp[i-1]+temp[i-2]+temp[i-3]
        print(sum)
        break;
    i+=1