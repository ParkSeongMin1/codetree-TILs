from collections import deque

n,m,k = map(int, input().split())

broken = [[False for _ in range(m)] for _ in range(n)]
last_attacked = [[0 for _ in range(m)] for _ in range(n)]
dx, dy = [0,1,0,-1], [1,0,-1,0]
bx, by = [1,1,1,0,-1,-1,-1,0], [-1,0,1,1,1,0,-1,-1]
bombed = []
lazer_route = []
board = []

for _ in range(n):
    board.append(list(map(int, input().split())))

for x in range(n):
    for y in range(m):
        if board[x][y] == 0:
            broken[x][y] = True

def set_attacker(time):
    global board
    temp = []
    for x in range(n):
        for y in range(m):
            if board[x][y] > 0:
                temp.append((board[x][y], last_attacked[x][y], x+y, y, x))
    temp.sort(key=lambda x : (x[0], -x[1], -x[2], -x[3]))
    last_attacked[temp[0][-1]][temp[0][-2]] = time
    board[temp[0][-1]][temp[0][-2]] += (n+m)
    return (temp[0][-1], temp[0][-2])

def set_attacked(attacker):
    global board
    temp = []
    for x in range(n):
        for y in range(m):
            if board[x][y] > 0 and (x, y) != attacker:
                temp.append((board[x][y], last_attacked[x][y], x+y, y, x))
    temp.sort(key=lambda x : (-x[0], x[1], x[2], x[3]))
    if temp:
        return (temp[0][-1], temp[0][-2])
    return []

def find_route(attacked, attacker, visited):
    global lazer_route
    global board
    # print(attacked)
    # print(x1, y1)
    x2, y2 = attacked
    queue = deque([[attacker]])
    min_len = 1000000
    while queue:
        routes = queue.popleft()
        x,y = routes[-1]
        for i in range(4):
            nx, ny = x+dx[i], y+dy[i]
            if nx < 0:
                nx = n - 1
            if nx >= n:
                nx = 0
            if ny < 0:
                ny = m - 1
            if ny >= m:
                ny = 0
            if board[nx][ny] == 0 or visited[nx][ny]:
                continue
            visited[nx][ny] = True
            n_routes = []
            for r in routes:
                n_routes.append(r)
            n_routes.append((nx, ny))
            if (nx, ny) == attacked and len(n_routes) < min_len:
                lazer_route = n_routes
                min_len = len(n_routes)
                continue
            queue.append(n_routes)
            

def lazer(attacker, attacked):
    global board
    x1, y1 = attacker
    x2, y2 = attacked
    # print(attacked)
    visited = [[False for _ in range(m)] for _ in range(n)]
    visited[x1][y1] = True
    find_route(attacked, attacker, visited)
    if not lazer_route:
        bomb(attacker, attacked)
    else:
        for route in lazer_route:
            x,y = route
            if (x,y) == attacker:
                continue
            if (x,y) == (x2, y2):
                board[x][y] = max(board[x][y] - board[x1][y1], 0)
            else:
                board[x][y] = max(board[x][y] - (board[x1][y1] // 2), 0)

def bomb(attacker, attacked):
    global bombed
    global board
    x1, y1 = attacker
    x2, y2 = attacked
    for i in range(8):
        nx, ny = x2+bx[i], y2+by[i]
        if nx < 0:
            nx = n - 1
        if nx >= n:
            nx = 0
        if ny < 0:
            ny = m - 1
        if ny >= m:
            ny = 0
        if board[nx][ny] == 0:
            continue
        bombed.append((nx, ny))
        board[nx][ny] = max(board[nx][ny] - board[x1][y1] // 2, 0)
    board[x2][y2] = max(board[x2][y2] - board[x1][y1], 0)

for time in range(1, k+1):
    attacker = set_attacker(time)
    attacked = set_attacked(attacker)
    # print(attacker, attacked)
    lazer(attacker, attacked)
    if lazer_route:
        for x in range(n):
            for y in range(m):
                if (x,y) not in lazer_route and board[x][y] > 0:
                    board[x][y] += 1
    else:
        for x in range(n):
            for y in range(m):
                if (x,y) != attacker and (x,y) != attacked and (x,y) not in bombed and board[x][y] > 0:
                    board[x][y] += 1
    lazer_route = []
    bombed = []

res = 0

for x in range(n):
    for y in range(m):
        res = max(res, board[x][y])
print(res)