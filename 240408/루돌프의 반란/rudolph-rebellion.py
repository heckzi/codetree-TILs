n, m, p, c, d = map(int, input().split())
ri, rj = map(int, input().split())
ri -= 1
rj -= 1
v = [[0] * n for _ in range(n)]

v[ri][rj] = -1  # 루돌프 표시
santa = [0] * (p + 1)
for _ in range(1, p + 1):
    idx, si, sj = map(int, input().split())
    santa[idx] = (si - 1, sj - 1)
    v[si - 1][sj - 1] = idx  # 산타 표시

score = [0] * (p + 1)
wakeup_turn = [0] * (p + 1)
alive = [1] * (p + 1)
alive[0]=0


def move_santa(si, sj, di, dj, idx, mul):  # 이동해야하는데, 맵밖으로 나가면 탈락, 다른 산타가 없어야함
    queue = [(idx, si, sj, mul)]

    while queue:  # 연쇄작용을 위해서
        s, ci, cj, mul = queue.pop(0)
        ni, nj = ci + di * mul, cj + dj * mul  # mul 칸 만큼 이동해야하니까

        if 0 <= ni < n and 0 <= nj < n:  # 맵안이면
            if v[ni][nj] == 0:  # 땅이면?
                v[ni][nj] = s
                santa[s] = (ni, nj)

            else:
                victim = v[ni][nj]  # 피해자 산타 인덱스
                queue.append((victim, ni, nj, 1))  # 한칸씩이기에 1
                v[ni][nj] = s  # 쳤던 산타로 업뎃
                santa[s]=(ni,nj)

        else:  # 맵 밖이면?
            alive[s]=0
            return


# 게임 시작한다
for turn in range(1, m + 1):
    if sum(alive)==0: # 다 탈락시 종료
        break
    # 루돌프 이동 , 가까운 산타를 향해 1칸 / 탈락 산타 제외 / 산타중 i,j가 큰 것 / 8방향
    mindist = 2 * n ** 2
    for idx in range(1, p + 1):
        if alive[idx] == 0: continue  # 탈락산타제외
        si, sj = santa[idx]
        tempdist = (ri - si) ** 2 + (rj - sj) ** 2  # 현재 거리 계산
        if tempdist < mindist:  # 작으면 갱신
            mindist = tempdist
            nomisanta = [(si,sj,idx)]  # 후보 산타 고르기
        elif mindist==tempdist: # 같은 거리면 추가
            nomisanta.append((si, sj, idx))

    nomisanta.sort(reverse=True)  # r,c를 내림차순으로 정렬
    ti, tj, tidx = nomisanta[0]  # 타겟 산타 (i,j,idx)

    dri = drj = 0  # 루돌프의 방향벡터 초기화
    if ri < ti:  # 루돌프가 더 위에 있으면
        dri += 1  # 방향벡터는 아래로
    elif ri > ti:  # 아래있으면
        dri -= 1
    if rj < tj:
        drj += 1
    elif rj > tj:
        drj -= 1
    # 루돌프 이동 처리
    v[ri][rj] = 0  # 루돌프 원래자리서 지우고
    ri += dri  # 루돌프 이동하기
    rj += drj
    v[ri][rj] = -1

    # 루돌프가 박은 충돌처리
    if (ri,rj)==(ti,tj):  # 산타이면?
        score[tidx] += c  # 루돌프에게 박혀서 c점 얻는다
        move_santa(ti, tj, dri, drj, tidx, c)  # 산타가 움직이는 함수
        wakeup_turn[tidx] = turn + 2  # 충돌됐으니 기절시키기

    # 산타의 이동 / 상우하좌 순 / 기절 or 탈락 제외 / 맵안 or 산타가 없는곳 / 루돌프와 가까워져야함
    for s in range(1, p + 1):
        if wakeup_turn[s] > turn: continue  # 산타가 기절이면패스
        if alive[s] == 0: continue  # 탈락이면 패스
        si, sj = santa[s]
        temp = []
        tempdist = (ri - si) ** 2 + (rj - sj) ** 2
        for di, dj in ((-1, 0), (0, 1), (1, 0), (0, -1)):  # 상우하좌순
            ni, nj = si + di, sj + dj
            ndist = (ri - ni) ** 2 + (rj - nj) ** 2
            if 0<=ni<n and 0<=nj<n and v[ni][nj]<=0 and tempdist > ndist:  # 이동했을때 루돌프랑 더 가까우면
                tempdist = ndist
                temp.append((di, dj))  # 제일 뒤에서 들어간게 진짜 가야할 위치
        if not temp: continue
        di, dj = temp[-1]
        ni, nj = si + di, sj + dj

        if (ri,rj) == (ni,nj):  # 이동한 칸이 루돌프일 때
            v[si][sj]=0
            score[s] += d  # 점수 획득
            wakeup_turn[s]=turn+2 #기절시키기
            move_santa(ni, nj, -di, -dj, s, d)  # 반대 방향으로 밀려난다
        else:
            v[si][sj]=0
            v[ni][nj]=s
            santa[s]=(ni,nj)


    # 살아남은산타들 1점씩
    for a in range(len(alive)):
        if alive[a]==1:
            score[a]+=1

# 정답출력
print(*score[1:])