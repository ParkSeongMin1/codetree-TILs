n,m,k = map(int, input().split())
dx, dy = [0,0,1,-1], [1,-1,0,0]
board = []

for _ in range(n):
    board.append(list(map(int, input().split())))

people = []

for _ in range(m):
    x,y = map(int, input().split())
    people.append((x-1, y-1))

ex,ey = map(int, input().split())
exit = (ex-1, ey-1) 

moved = 0

def distance(r1,r2,c1,c2):
    return abs(r1-r2) + abs(c1-c2)

def out_of_range(x,y):
    if 0 <= x < n and 0 <= y < n:
        return False
    return True

def move():
    global exit
    global moved
    global people
    
    ex, ey = exit
    new_people = []
    for p in people:
        px, py = p
        temp = []
        for i in range(4):
            nx, ny = px+dx[i], py+dy[i]
            if out_of_range(nx, ny) or board[nx][ny] > 0:
                continue
            # if p == (0,0):
            #     print(nx, ny)
            #     print(distance(px, ex, py, ey), distance(nx, ex, ny, ey))
            if distance(px, ex, py, ey) > distance(nx, ex, ny, ey):
                temp = [nx, ny]
        if not temp:
            new_people.append((px, py))
        else:
            nx, ny = temp
            if (nx, ny) != exit:
                new_people.append((nx, ny))
            moved += 1
    people = new_people
    # print(new_people)

def find_square():
    global exit
    global people
    ex, ey = exit
    squares = []
    for p in people:
        px, py = p
        s_len = max(abs(ex-px), abs(ey-py))
        tx, ty = max(ex, px), max(ey, py)
        sx, sy = max(0, tx - s_len), max(0, ty - s_len)
        squares.append((s_len, sx, sy))
    squares.sort(key=lambda x : (x[0], x[1], x[2]))
    return squares[0]

for _ in range(k):
    #모든 사람 탈출
    if not people:
        break
    move()
    #print(people)
    square = find_square()
    s_len, sx, sy = square
    before = []
    for x in range(sx, sx+s_len+1):
        temp = []
        for y in range(sy, sy+s_len+1):
            temp.append((x,y))
        before.append(temp)
    # before = before[::-1]
    after = list(zip(*before))
    after = after[::-1]
    new_board = []
    for b in board:
        temp = []
        for i in b:
            temp.append(i)
        new_board.append(temp)
        # print(temp)
    new_people = []
    moved_people = []
    for bx in range(sx, sx+s_len+1):
        for by in range(sy, sy+s_len+1):
            ax, ay = after[bx-sx][by-sy]
            # print(bx, by, ax, ay)
            if (bx, by) in people:
                new_people.append((ax, ay))
                moved_people.append((bx, by))
            elif (bx, by) == exit:
                exit = (ax, ay)
            else:
                # print(board[bx][by])
                new_board[ax][ay] = max(0, board[bx][by] - 1)    
    temp = []
    for p in people:
        if p in moved_people:
            continue
        temp.append(p)
    for p in new_people:
        temp.append(p)

    people = temp 
    board = new_board
    # for b in new_board:
    #     print(b)
    # print(people, exit)

    # print(after)

print(moved)
for i in exit:
    print(i+1, end=' ')