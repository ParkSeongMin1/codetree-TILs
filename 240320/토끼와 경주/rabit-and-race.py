from queue import PriorityQueue

q = int(input())

dx, dy = [0,0,1,-1], [1,-1,0,0]
n,m = 0,0

for _ in range(q):
    cmd = tuple(map(int, input().split()))
    if cmd[0] == 100:
        rabbits = PriorityQueue()
        n,m = cmd[1], cmd[2]
        board = [[0 for _ in range(cmd[2])] for _ in range(cmd[1])]
        jump = {}
        scores = {}
        for i in range(cmd[3]):
            rabbit = (0,0,0,0,cmd[4+i*2])
            jump[cmd[4+i*2]] = cmd[4+i*2+1]
            scores[cmd[4+i*2]] = 0
            rabbits.put(rabbit)
            # print(jump)
    if cmd[0] == 200:
        k,s = cmd[1], cmd[2]
        for turn in range(k):
            rabbit = rabbits.get()
            # print(rabbit)
            # rabbits.put(rabbit)
            rx, ry = rabbit[2], rabbit[3]
            jump_pow = jump[rabbit[-1]]
            pos = PriorityQueue()
            for i in range(4):
                # print(i)
                if i == 0:
                    j = jump_pow + rx
                    p = j % (n-1)
                    if (j // (n-1)) % 2 == 1:
                        nx, ny = n - p - 1, ry
                    else:
                        nx, ny = p, ry
                    pos.put((-(nx+ny), -nx, -ny))
                if i == 1:
                    j = abs(rx - jump_pow)
                    p = j % (n-1)
                    if (j // (n-1)) % 2 == 1:
                        nx, ny = n - 1 - p, ry
                    else:
                        nx, ny = p, ry
                    pos.put((-(nx+ny), -nx, -ny))
                if i == 2:
                    j = jump_pow + ry
                    p = j % (m-1)
                    if (j // (m-1)) % 2 == 1:
                        nx, ny = rx, m - p - 1
                    else:
                        nx, ny = rx, p
                    pos.put((-(nx+ny), -nx, -ny))
                if i == 3:
                    j = abs(ry - jump_pow)
                    p = j % (m-1)
                    if (j // (m-1)) % 2 == 1:
                        nx, ny = rx, m - 1 - p
                    else:
                        nx, ny = rx, p
                    # if turn == 2:
                    #     print(j, p, nx, ny) 
                    pos.put((-(nx+ny), -nx, -ny))
                # if turn == 2:
                #     print((nx, ny))
            # if turn  == 2:
            #     print(pos.queue)
            _, nx, ny = pos.get()
            nx, ny = -nx, -ny
            for key, value in scores.items():
                if key != rabbit[-1]:
                    scores[key] += (nx+ny+2)
            rabbits.put((rabbit[0]+1, nx+ny, nx, ny, rabbit[-1]))
            # print(rabbits.queue)
            # print(scores)
        temp = []
        for rabbit in rabbits.queue:
            jumped, summation, x, y, rid = rabbit
            if jumped == 0:
                continue
            temp.append((-summation, -x, -y, -rid))
        temp.sort(key = lambda x : (x[0], x[1], x[2], x[3]))
        scores[-temp[0][-1]] += s
        # print(scores)
    if cmd[0] == 300:
        jump[cmd[1]] *= cmd[2]
    if cmd[0] == 400:
        score = 0
        for key, value in scores.items():
            score = max(score, value)
        print(score)