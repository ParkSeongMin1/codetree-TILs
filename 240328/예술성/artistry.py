from collections import deque

n = int(input())
board = []
dx, dy = [0,0,1,-1], [1,-1,0,0]

for _ in range(n):
    board.append(list(map(int, input().split())))

groups = []
score = 0

def out_of_range(x,y):
    if 0 <= x < n and 0 <= y < n:
        return False
    return True

def find_groups():
    global groups
    new_groups = []
    visited = [[False for _ in range(n)] for _ in range(n)]
    for x in range(n):
        for y in range(n):
            group = []
            num = board[x][y]
            if not visited[x][y]:
                queue = deque([(x,y)])
                visited[x][y] = True
                group.append((x,y))
                while queue:
                    cx, cy = queue.popleft()
                    for i in range(4):
                        nx, ny = cx+dx[i], cy+dy[i]
                        if out_of_range(nx, ny) or visited[nx][ny] or board[nx][ny] != num:
                            continue
                        visited[nx][ny] = True
                        queue.append((nx, ny))
                        group.append((nx,  ny))
            if group:
                new_groups.append(group)
    groups = new_groups

def get_score():
    global score
    for idx1 in range(len(groups)):
        for idx2 in range(idx1+1, len(groups)):
            g1, g2 = groups[idx1], groups[idx2]
            lines = 0
            for pos1 in g1:
                px, py = pos1
                for i in range(4):
                    nx, ny = px+dx[i], py+dy[i]
                    if out_of_range(nx, ny) or (nx, ny) not in g2:
                        continue
                    lines += 1
            score += ((len(g1) + len(g2)) * board[g1[0][0]][g1[0][1]] * board[g2[0][0]][g2[0][1]] * lines )
            
def rotate():
    #rotate c_clockwise
    global board
    new_board = [list(a) for a in zip(*board)][::-1]
    spos = [(0,0), (0,n//2+1), (n//2+1, 0), (n//2+1, n//2+1)]
    squares = []
    for pos in spos:
        square = []
        sx, sy = pos
        for d1 in range(n//2):
            temp = []
            for d2 in range(n//2):
                temp.append((sx+d1, sy+d2, board[sx+d1][sy+d2]))
            square.append(temp)
        squares.append(square)
    
    for i in range(4):
        squares[i] = [list(a) for a in zip(*squares[i][::-1])]
    
    for i in range(4):
        square = squares[i]
        sx, sy = spos[i]
        for x in range(n//2):
            for y in range(n//2):
                new_board[sx+x][sy+y] = square[x][y][2]
    board = new_board
    
    
                
    
    
for _ in range(4):
    find_groups()
    get_score()
    rotate()
print(score)