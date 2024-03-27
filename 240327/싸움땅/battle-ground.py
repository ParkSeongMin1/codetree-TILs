import heapq

n,m,k = map(int, input().split())

dx,dy = [-1,0,1,0], [0,1,0,-1]
players = []
board = []
guns = [[[] for _ in range(n)] for _ in range(n)]
players_pos = []
scores = [0] * m

def out_of_range(x,y):
    if 0 <= x < n and 0 <= y < n:
        return False
    return True

for x in range(n):
    board.append(list(map(int, input().split())))

for x in range(n):
    for y in range(n):
        heapq.heappush(guns[x][y], -board[x][y])

for _ in range(m):
    x,y,d,s = map(int, input().split())
    players.append((x-1,y-1,d,s,0))
    players_pos.append((x-1,y-1))

def fight(idx1, idx2):
    global scores
    p1 = players[idx1]
    p2 = players[idx2]
    if p1[-1] + p1[-2] > p2[-1] + p2[-2]:
        scores[idx1] += abs((p1[-1] + p1[-2]) - (p2[-1] + p2[-2]))
        return idx1
    if p1[-1] + p1[-2] < p2[-1] + p2[-2]:
        scores[idx2] += abs((p1[-1] + p1[-2]) - (p2[-1] + p2[-2]))
        return idx2
    if p1[-2] > p2[-2]:
        return idx1
    return idx2

def rotate(idx):
    global guns
    global players
    px, py, pd, ps, pg = players[idx]
    heapq.heappush(guns[px][py], -pg)
    for i in range(4):
        nx, ny = px+dx[pd], py+dy[pd]
        if not out_of_range(nx, ny) and (nx, ny) not in players_pos:
            break
        pd = (pd+1) % 4
    heapq.heappush(guns[nx][ny], 0)
    pg = heapq.heappop(guns[nx][ny])
    players[idx] = (nx, ny, pd, ps, -pg)

def winner_take_gun(idx):
    global guns
    global players
    px, py, pd, ps, pg = players[idx]
    heapq.heappush(guns[px][py], -pg)
    pg = heapq.heappop(guns[px][py])
    players[idx] = (px, py, pd, ps, -pg)

for _ in range(k):
    for pidx in range(m):
        px, py, pd, ps, pg = players[pidx]
        nx, ny = px+dx[pd], py+dy[pd]
        if out_of_range(nx, ny):
            pd = (pd+2) % 4
            nx, ny = px+dx[pd], py+dy[pd]
        players[pidx] = (nx, ny, pd, ps, pg)
        faught = False
        for pidx2 in range(m):
            if pidx == pidx2:
                continue
            px2, py2, pd2, ps2, pg2 = players[pidx2]
            if (px2, py2) == (nx, ny): #fight
                faught = True
                winner = fight(pidx, pidx2)
                if winner == pidx:
                    rotate(pidx2)
                    winner_take_gun(pidx)
                elif winner == pidx2:
                    rotate(pidx)
                    winner_take_gun(pidx2)
        if not faught:
            winner_take_gun(pidx)
    ii = 0

for s in scores:
    print(s, end=' ')