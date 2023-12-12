sum=0
i=0
temp=[]
temp=list(map(int,input().split()))
while 1:
    if(temp[i]==0):
        print(sum)
        break;
    sum+=temp[i]
    i+=1