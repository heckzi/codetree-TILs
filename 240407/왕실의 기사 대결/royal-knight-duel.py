l,n,q=map(int,input().split()) # 체스판 크기, 기사의 수, 명령의 수

arr=[[2]*(l+2)]+[[2]+list(map(int,input().split()))+[2] for _ in range(l)] +[[2]*(l+2)]
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
units={}
init_k=[0]*(n+1)
# v=[[0]*(l+2) for _ in range(l+2)] #디버그용 기사 표시 맵

for num in range(1,n+1):
    r,c,h,w,k=map(int,input().split())
    units[num]=[r,c,h,w,k]
    init_k[num]=k

    # for i in range(r,r+h): #디버그용 기사 표시 맵에 넣기
    #     for j in range(c,c+w):
    #         v[i][j]=num

def push_unit(start,dr):
    queue=[]
    push_set=set() #밀려질 대상을 담은 set

    damage=[0]*(n+1)
    queue.append(start)
    push_set.add(start)

    while queue:
        cur=queue.pop(0) #큐에서 데이터 하나 꺼냄
        r,c,h,w,k=units[cur]
        nr,nc =r+dx[dr],c+dy[dr] #명령방향으로 밀고난 좌상단 좌표

        for i in range(nr,nr+h): #그 안을 검사한다
            for j in range(nc,nc+w):
                if arr[i][j]==2: #벽이있다면
                    return #무시한다
                if arr[i][j]==1: #함정인 경우
                    damage[cur]+=1 #데미지 주기

        #벽이 아니고, 다른 기사가 있으면 큐에 삽입
        for idx in units:
            if idx in push_set: continue #
            tr,tc,th,tw,tk=units[idx] #밀려질 기사의 정보
            #다른기사가 있는지 체크하자
            if nr<=tr+th-1 and nc<=tc+tw-1 and nr+h-1>=tr and nc+w-1>=tc:
                queue.append(idx)
                push_set.add(idx)
    #명령 받은 애는 데미지 0 , 데미지 처리하기
    damage[start]=0
    # for i in range(r, r + h):  # 디버그용 원래기사 위치 0으로
    #     for j in range(c, c + w):
    #         v[i][j] = 0
    # 밀려는 애들 처리
    for idx in push_set:
        r,c,h,w,k=units[idx]
        if k<=damage[idx]: #체력이 데미지 보다 작거나 같으면 죽이기
            units.pop(idx)

        else:
            nr,nc,nk=r+dx[dr],c+dy[dr],k-damage[idx]
            units[idx][0]=nr
            units[idx][1]=nc
            units[idx][4]=nk
            # for i in range(nr, nr + h):  # 디버그용 이동한 기사 위치에 넣기
            #     for j in range(nc, nc + w):
            #         v[i][j] = idx

#명령 받고 입력 처리하기
for _ in range(q):
    idx,dr=map(int,input().split()) #명령받은 기사 idx, 방향

    #명령 처리한 뒤 충돌 여부 체크
    if idx in units: #살아있으면
        push_unit(idx,dr) #명령받은 기사 (연쇄적으로 밀기), 벽이 없는경우에


#정답 처리
ans=0
for idx in units:
    ans+=init_k[idx]-units[idx][4]

print(ans)