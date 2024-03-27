from collections import deque

dx, dy = [-1,0,0,1], [0,-1,1,0]

n,m = map(int, input().split())

board = []
convis = []
people = []
bases = []
red = [[False for _ in range(n)] for _ in range(n)]

for _ in range(n):
    board.append(list(map(int, input().split())))

for _ in range(m):
    x,y = tuple(map(int, input().split()))
    convis.append((x-1, y-1))

for x in range(n):
    for y in range(n):
        if board[x][y] == 1:
            bases.append((x,y))

time = 0

def out_of_range(x,y):
    if 0 <= x < n and 0 <= y < n:
        return False
    return True

def find_route(x1, y1, x2, y2):
    queue = deque([(x1,y1)])
    visited = [[False for _ in range(n)] for _ in range(n)]
    while queue:
        x,y = queue.popleft()
        for i in range(4):
            nx, ny = x+dx[i], y+dy[i]
            if out_of_range(nx, ny) or visited[nx][ny] != False or red[nx][ny]:
                continue
            visited[nx][ny] = (x,y)
            if (nx, ny) == (x2, y2):
                break
            queue.append((nx, ny))
    if visited[x2][y2] == False:
        return False
    cx, cy = visited[x2][y2]
    route = [(x2, y2)]
    while True:
        route.append((cx, cy))
        if (cx, cy) == (x1, y1):
            break
        cx, cy = visited[cx][cy]
    route = route[::-1]
    return route

def set_convi(convi):
    global bases
    cx, cy = convi
    min_len = float('inf')
    temp = []
    for base in bases:
        bx, by = base
        route = find_route(bx,by,cx,cy)
        if not route:
            continue
        if len(route) < min_len:
            min_len = len(route)
            temp = [base]
        elif len(route) == min_len:
            temp.append(base)
    temp.sort(key=lambda x : (x[0], x[1]))
    return temp[0]

while True:
    for idx in range(len(people)):
        if people[idx] == 0:
            continue
        px, py = people[idx]
        cx, cy = convis[idx]
        nx, ny = find_route(px,py,cx,cy)[1]
        if (nx, ny) == (cx, cy):
            people[idx] = 0
            convis[idx] = 0
            red[nx][ny] = True
            continue
        people[idx] = (nx, ny)
    if time < m:
        base = set_convi(convis[time])
        bases.remove(base)
        people.append(base)
        red[base[0]][base[1]] = True
    time += 1
    ps = True
    for p in people:
        if p != 0:
            ps = False
    if ps:
        break
print(time)