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

def find_route(attacked, route, cnt, visited):
    global lazer_route
    global board
    # print(attacked)
    pos= route[-1]
    x1, y1 = pos
    # print(x1, y1)
    x2, y2 = attacked
    for i in range(4):
        nx, ny = x1+dx[i], y1+dy[i]
        if nx < 0:
            nx = n - 1
        if nx >= n:
            nx = 0
        if ny < 0:
            ny = m - 1
        if ny >= m:
            ny = 0
        # print(nx, ny)
        if board[nx][ny] == 0 or visited[nx][ny]:
            continue
        if (nx, ny) == attacked:
            print(attacked, (nx, ny))
            route.append(attacked)
            print(route)
            temp = []
            for i in range(len(route) - 1):
                temp.append((route[i][0], route[i][1]))
            if not lazer_route:
                lazer_route = [temp, cnt+1]
            else:
                if lazer_route[-1] > cnt + 1:
                    lazer_route = [temp, cnt+1]
            return
        route.append((nx, ny))
        visited[nx][ny] = True
        find_route(attacked, route, cnt+1, visited)
        route.pop()
        visited[nx][ny] = False


def lazer(attacker, attacked):
    global board
    x1, y1 = attacker
    x2, y2 = attacked
    # print(attacked)
    visited = [[False for _ in range(m)] for _ in range(n)]
    visited[x1][y1] = True
    find_route(attacked, [attacker], 0, visited)
    if not lazer_route:
        bomb(attacker, attacked)
    else:
        for route in lazer_route[0]:
            x,y = route
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
    print(lazer_route)