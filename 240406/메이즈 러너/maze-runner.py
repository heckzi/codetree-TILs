n, m, k = map(int, input().split())
graph = []
for _ in range(n):
    graph.append(list(map(int, input().split())))

for _ in range(m):
    temp = list(map(int, input().split()))
    temp[0] -= 1
    temp[1] -= 1
    graph[temp[0]][temp[1]]=-1

exit_coor = list(map(int, input().split()))
exit_coor[0] -= 1
exit_coor[1] -= 1
graph[exit_coor[0]][exit_coor[1]] = -50 #탈출구 설정

ans=0
cnt=m

def check_dist(x, y, a, b):
    return abs(x - a) + abs(y - b)

def move_runner():
    global ans,cnt,graph
    new_graph = [x[:] for x in graph]
    dx = [-1, 1, 0, 0]  # 상하좌우
    dy = [0, 0, -1, 1]
    for i in range(n):
        for j in range(n):
            if -50<graph[i][j]<0: #러너이면
                dist=check_dist(exit_coor[0],exit_coor[1],i,j)
                for di,dj in zip(dx,dy):
                    ni,nj=i+di, j+dj
                    if 0<=ni<n and 0<=nj<n and graph[ni][nj]<=0 and dist>check_dist(exit_coor[0],exit_coor[1],ni,nj):
                        #맵 안이고, 사람이고, 현재 탈출구거리보다 작으면
                        ans+=graph[i][j] #이동거리 합
                        new_graph[i][j]-=graph[i][j]  #이동 처리, 러너는 음수이므로 빼주면 그자리는 0이됨
                        if graph[ni][nj]==-50: #탈출구이면
                            cnt+=graph[i][j] #탈출처리한다
                        else:#사람이나 빈칸이 있으면
                            new_graph[ni][nj]+=graph[i][j] #음수니까 플러스로 사람추가
                        break
    graph=new_graph #새로운 맵 업데이트



def find_exit(arr):
    for i in range(n):
        for j in range(n):
            if arr[i][j]==-50:
                return [i,j]


def make_square(arr):
    mn = n
    for i in range(n):
        for j in range(n):
            if -11 < arr[i][j] < 0: # 사람일 떄
                mn = min(mn, max(abs(exit_coor[0]-i),abs(exit_coor[1]-j))) # 가장 짧은 가로 혹은 세로 구하기

    for si in range(n-mn):
        for sj in range(n-mn):
            if si <= exit_coor[0] <= si+mn and sj<=exit_coor[1]<=sj+mn: # 출구를 포함한 정사각형
                for i in range(si,si+mn+1):
                    for j in range(sj,sj+mn+1):
                        if -11 < arr[i][j] < 0:
                            return si,sj,mn+1

def rotate_maze():
    global graph,exit_coor
    r, c,l = make_square(graph)
    new_graph=[x[:] for x in graph]
    for i in range(l):
        for j in range(l):
            new_graph[r+i][c+j]=graph[r+l-1-j][c+i]
            if new_graph[r+i][c+j]>0: #벽이면 회전할때 1깎기
                new_graph[r + i][c + j]-=1
    graph=new_graph
    exit_coor=find_exit(graph)

if __name__ == '__main__':
    for i in range(k):
        move_runner()
        if cnt==0:
            break
        rotate_maze()
        # pprint(graph)

    print(-ans)
    print(exit_coor[0]+1, exit_coor[1]+1)