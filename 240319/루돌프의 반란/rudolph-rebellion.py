n,m,p,c,d = map(int, input().split())
deer = tuple(map(int, input().split()))
dx = [-1,0,1,0]
dy = [0,1,0,-1]
s_dx = [-1,-1,0,1,1,1,0,-1]
s_dy = [0,1,1,1,0,-1,-1,-1]
board = [[0 for _ in range(n+1)] for _ in range(n+1)]
stunned = [0] * (p+1)
scores = [0] * (p+1)
retired = [False] * (p+1)
board[deer[0]][deer[1]] = -1
for _ in range(p):
    s_id, x, y = map(int, input().split())
    board[x][y] = s_id

def out_of_range(x,y):
    if 1 <= x <= n and 1 <= y <= n:
        return False
    return True

def distance(r1,r2,c1,c2):
    return (r1-r2)**2 + (c1-c2)**2

for turn in range(m):
    #산타 선택
    selected = []
    min_dist = 5001
    dr, dc = deer
    for x in range(1, n+1):
        for y in range(1, n+1):
            if board[x][y] > 0 and distance(dr, x, dc, y) < min_dist:
                min_dist = distance(dr, x, dc, y)
                selected = [(board[x][y], x, y)]
            if board[x][y] > 0 and distance(dr, x, dc, y) == min_dist:
                selected.append((board[x][y], x, y))
    if not selected:
        break
    selected.sort(key=lambda x : (-x[1], -x[2]))
    selected = selected[0]
    #루돌프 움직임
    d_arrow = 0
    min_dist = 5001
    s_idx, sr, sc = selected
    for i in range(8):
        dist = distance(dr+s_dx[i], sr, dc+s_dy[i], sc)
        #print(dist, i)
        if dist < min_dist:
            d_arrow = i
            min_dist = dist
    board[dr][dc] = 0
    deer = (dr+s_dx[d_arrow], dc+s_dy[d_arrow])
    #산타 부딪힘
    dr, dc = deer
    if board[dr][dc] > 0:
        scores[s_idx] += c
        board[dr][dc] = -1
        stunned[s_idx] = 2
        nx, ny = sr + (c * s_dx[d_arrow]), sc + (c * s_dy[d_arrow])
        while True:
            if out_of_range(nx, ny):
                retired[s_idx] = True
                break
            temp = board[nx][ny]
            board[nx][ny] = s_idx
            s_idx = temp
            if s_idx == 0:
                break
            nx, ny = nx+s_dx[d_arrow], ny+s_dy[d_arrow]
    elif board[dr][dc] == 0:
        board[dr][dc] = -1
    #산타 모음
    santas = []
    for x in range(1, n+1):
        for y in range(1, n+1):
            if board[x][y] > 0:
                santas.append((board[x][y], x, y))
    santas.sort(key=lambda x : x[0])
    #산타 움직임
    for santa in santas:
        s_idx, sr, sc = santa
        for x in range(1, n+1):
            for y in range(1, n+1):
                if board[x][y] == s_idx:
                    sr, sc = x, y
        if stunned[s_idx] or retired[s_idx]:
            continue
        arrow = -1
        min_dist = distance(dr, sr, dc, sc)
        for i in range(4):
            nx, ny = sr+dx[i], sc+dy[i]
            dist = distance(dr, sr+dx[i], dc, sc+dy[i])
            if dist < min_dist and board[nx][ny] <= 0:
                arrow = i
                min_dist = dist
        if arrow == -1:
            continue
        board[sr][sc] = 0
        nx, ny = sr+dx[arrow], sc+dy[arrow]
        if board[nx][ny] == 0:
            board[nx][ny] = s_idx
            continue
        if board[nx][ny] == -1:
            #루돌프랑 충돌
            arrow = (arrow + 2) % 4
            nx, ny = nx+(d * dx[arrow]), ny+(d * dy[arrow])
            stunned[s_idx] = 2
            scores[s_idx] += d
            while True:
                if out_of_range(nx, ny):
                    retired[s_idx] = True
                    break
                temp = board[nx][ny]
                board[nx][ny] = s_idx
                s_idx = temp
                if s_idx == 0:
                    break
                nx, ny = nx + dx[arrow], ny + dy[arrow]
    for i in range(1, p+1):
        if stunned[i] > 0:
            stunned[i] -= 1
    for idx in range(1, p+1):
        if not retired[idx]:
            scores[idx] += 1

for i in range(1, p+1):
    print(scores[i], end=' ')