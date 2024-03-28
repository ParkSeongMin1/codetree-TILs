n,m,h,k = map(int, input().split())

def out_of_range(x,y):
    if 0 <= x < n and 0 <= y < n:
        return False
    return True

dx, dy = [-1,0,1,0], [0,1,0,-1]
pdx, pdy = [[], [0,0], [1,-1]], [[], [1,-1], [0,0]]

route = []
reverse_route = []
score = 0

x,y = n//2, n//2
route.append((x,y,0))
r_len = 1
idx = 0

while True:
    for i in range(r_len):
        x,y = x+dx[idx], y+dy[idx]
        if out_of_range(x,y):
            break
        if i == r_len-1:
            route.append((x,y,(idx+1)%4))
        else:
            route.append((x,y,idx))
    if r_len == n:
        break
    idx = (idx+1) % 4
    if idx % 2 == 0:
        r_len += 1

for x in range(n):
    reverse_route.append((x,0,2))

x,y = n-1, 0
r_len = n-1
idx = 1

while True:
    for i in range(r_len):
        x,y = x+dx[idx], y+dy[idx]
        if i == r_len - 1:
            reverse_route.append((x,y,(idx+3)%4))
        else:
            reverse_route.append((x,y,idx))
    if (x,y) == (n//2, n//2):
        break
    idx = (idx+3) % 4
    if idx % 2 == 1:
        r_len -= 1


prays = []

for _ in range(m):
    x,y,d = map(int, input().split())
    prays.append([x-1,y-1,d,0])

trees = [[False for _ in range(n)] for _ in range(n)]

for _ in range(h):
    x,y = map(int, input().split())
    trees[x-1][y-1] = True

idx = 0

def catch(cx, cy, d, turn):
    global prays
    global score
    temp = [(cx, cy)]
    nx, ny = cx, cy
    for i in range(2):
        nx, ny = nx + dx[d], ny+dy[d]
        if not out_of_range(nx, ny):
            temp.append((nx, ny))
    catched = []
    for p in prays:
        px, py, _, _ = p
        if (px, py) in temp and not trees[px][py]:
            catched.append(p)
    for c in catched:
        prays.remove(c)
    score += (turn * len(catched))

def dist(x1, x2, y1, y2):
    return abs(x1-x2) + abs(y1-y2)
 
def move(cx, cy):
    global prays
    for pidx in range(len(prays)):
        px, py, pd, pi = prays[pidx]
        if dist(cx, px, cy, py) > 3:
            continue
        nx, ny = px+pdx[pd][pi], py+pdy[pd][pi]
        if out_of_range(nx, ny):
            pi = (pi+1) % 2
            nx, ny = px+pdx[pd][pi], py+pdy[pd][pi]
        if (cx, cy) == (nx, ny):
            continue
        prays[pidx] = [nx, ny, pd, pi]

cur_route = route

for turn in range(1, k+1):
    cx, cy, d = cur_route[idx]
    move(cx, cy)
    idx += 1
    if turn % (n**2-1) == 0:
        idx = 0
    if (turn // (n**2-1)) % 2 == 0:
        cur_route = route
    else:
        cur_route = reverse_route
    cx, cy, d = cur_route[idx]
    catch(cx,cy,d,turn) 

print(score)