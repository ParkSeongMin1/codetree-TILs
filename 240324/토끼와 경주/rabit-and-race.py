import heapq

n = int(input())

li = list(map(int, input().split()))

n,m = li[1], li[2]

dx = [0,0,-1,1]
dy = [1,-1,0,0]

rabbits = []
scores = {}

idx = 4

while idx < len(li):
    rid, dist = li[idx], li[idx+1]
    scores[rid] = 0
    rabbits.append((rid, dist, 0, 0, 0)) #rid, dist, rx, ry, jumped num
    idx += 2


while True:
    query = list(map(int, input().split()))
    if len(query) == 1:
        break
    Q, K, S = query
    if Q == 400:
        break
    if Q == 200:
        visited = {}
        for key, value in scores.items():
            visited[key] = False
        for i in range(K):
            rabbits.sort(key = lambda x : (x[4], (x[2]+x[3]), x[2], x[3], x[0]))
            #print(rabbits)
            rabbit = rabbits[0]
            r_id = rabbit[0]
            dist = rabbit[1]
            jnum = rabbit[4]
            rx, ry = rabbit[2], rabbit[3]
            tmp = []
            for i in range(4):
                nx = rx + dx[i] * dist
                ny = ry + dy[i] * dist
                nx = nx % (2 * n - 2)
                ny = ny % (2 * m - 2)
                if nx > (n - 1):
                    if nx % (n-1) == 0:
                        nx = 0
                    else:
                        nx = (n - 1) - nx % (n-1)
                if ny > (m - 1):
                    if ny % (m-1) == 0:
                        ny = 0
                    else:
                        ny = (m - 1) - ny % (m-1)
                tmp.append((nx, ny))
            tmp.sort(key=lambda x : (-(x[0] + x[1]), -x[0], -x[1]))
            x,y = tmp[0][0], tmp[0][1]
            for key, value in scores.items():
                if key != r_id:
                    scores[key] += (x+y+2)
            visited[r_id] = True
            rabbits[0] = (r_id, dist, x, y, jnum+1)
            #print(rabbits)
            #print(scores)
        idx = 0
        rabbits.sort(key = lambda x : (-(x[2] + x[3]), -x[2], -x[3], -x[0]))
        while True:
            if visited[rabbits[idx][0]]:
                break
            idx += 1
        #print(rabbits)
        scores[rabbits[idx][0]] += S
        #print(scores)
    if Q == 300:
        idx = 0
        for rabbit in rabbits:
            if rabbit[0] == K:
                break
            idx += 1
        n_dist = rabbits[idx][1] * S
        rabbits[idx] = (rabbits[idx][0], n_dist, rabbits[idx][2], rabbits[idx][3], rabbits[idx][4])
        #print(rabbits)
res = 0

for key, value in scores.items():
    if value > res:
        res = value
print(res)