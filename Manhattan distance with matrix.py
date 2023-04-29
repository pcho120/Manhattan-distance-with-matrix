#Hyunkun Cho, Jacob McGrew, Christopher Pfefferle, Chase Baxter
import turtle
import time
class screensetup:
    screen = turtle.Screen()
    screen.setup(500,500)
    screen.setworldcoordinates(0,0,200.0,200.0)
    screen.tracer(0)  
    turtle.speed(0) 
    turtle.hideturtle()

    def grawGrid(matrix, N):
        global gridX
        global gridY
        global next_value
        gridX = []
        gridY = []

        for i in range(N + 1):
            x = i * (200 / N)
            turtle.pu()
            turtle.goto(x, 0)
            turtle.pd()
            turtle.goto(x, 200)
            gridX.append(x)

        for i in range(N + 1):
            y = i * (200 / N)
            turtle.pu()
            turtle.goto(0, y)
            turtle.pd()
            turtle.goto(200, y)
            gridY.append(y)

        # draw the squares based on the matrix
        square_size = 200 / N
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                turtle.pu()
                turtle.goto(gridX[col], gridY[row])
                turtle.setheading(0)

                #if -1 in matrix, color it (obstacle)
                if matrix[row][col] == -1:
                    turtle.begin_fill()
                    for i in range(4):
                        turtle.forward(square_size)
                        turtle.left(90)
                    turtle.end_fill()

                elif matrix[row][col] == 1:
                    for i in range(2):
                        turtle.forward(square_size/2)
                        turtle.left(90)
                    turtle.write("1")

                #if 999 in matrix, print 999 in center of the squre
                elif matrix[row][col] == 999:
                    for i in range(2):
                        turtle.forward(square_size/2)
                        turtle.left(90)
                    turtle.write("999")
                elif matrix[row][col] > 1:
                    for i in range(2):
                        turtle.forward(square_size/2)
                        turtle.left(90)
                    turtle.write(matrix[row][col])
                    """
                #if 1 in matrix, print 1 in center of the squre
                if next_value > 1 and next_value != 999:
                    for i in range(2):
                        turtle.forward(square_size/2)
                        turtle.left(90)
                    turtle.write(next_value)
                
                elif matrix[row][col] == 1:
                    for i in range(2):
                        turtle.forward(square_size/2)
                        turtle.left(90)
                    turtle.write("1")
                    """
                
                


class keyboard:
    def __init__(self):
        global N
        keyboard.end=0

        screensetup.screen.onscreenclick(self.leftClick)
        screensetup.screen.onscreenclick(self.rightClick, 3)

    def kend(self):
        keyboard.end=1                                      #program ends


    def leftClick(self, x, y):
        global matrix
        global N

        #calculate the row and column of the clicked box
        r = int(y // (200 / N))
        l = int(x // (200 / N))

        #update the matrix 
        if matrix [r][l] == 0:
            matrix [r][l] = -1
        else:
            matrix [r][l] = 0
        turtle.clear()
        screensetup.grawGrid(matrix, N)

    def rightClick(self, x, y):
        global matrix
        global N
        global c
        r = int(y // (200 / N))
        l = int(x // (200 / N))
        if c == 0:
            c += 1
            matrix[r][l] = 1
            screensetup.grawGrid(matrix, N)
        elif c == 1:
            c += 1
            matrix[r][l] = 999
            screensetup.grawGrid(matrix, N)

def update_matrix(target, row, col):
    global matrix
    global N
    global gridX
    global gridY
    global next_value
    global notReached

    if col > 0 and matrix[row][col-1] == 999:
        notReached = False
    elif col < N-1 and matrix[row][col+1] == 999:  
        notReached = False
    elif row > 0 and matrix[row-1][col] == 999:
        notReached = False
    elif row < N-1 and matrix[row+1][col] == 999:
        notReached = False

    if target == "left":
        if col > 0 and matrix[row][col-1] == 0:
            matrix[row][col-1] = next_value   
            

    elif target == "right":
        if col < N-1 and matrix[row][col+1] == 0:  
            matrix[row][col+1] = next_value
            

    elif target == "up": #actually down
        if row > 0 and matrix[row-1][col] == 0:
            matrix[row-1][col] = next_value
            
            
    elif target == "down": #actually up
        if row < N-1 and matrix[row+1][col] == 0:
            matrix[row+1][col] = next_value
    

def path_planning():
    global matrix
    global next_value
    global N
    global notReached
    global startIndex
    global endIndex

    next_value = 1
    if notReached:
        for row in range(N):
            for col in range(N):
                if matrix[row][col] == 1:
                    startIndex = [row, col]
                    print("start Index: " + str(startIndex))
                if matrix[row][col] == 999:
                    endIndex = [row, col]
                    print("end index: " + str(endIndex))

                if matrix[row][col] > next_value and matrix[row][col] != 999:
                    next_value = matrix[row][col]
                if matrix[row][col] == next_value and notReached:
                    
                    next_value += 1
                    update_matrix("left", row, col)
                            
                    update_matrix("right", row, col)
                            
                    update_matrix("up", row, col)
                            
                    update_matrix("down", row, col)
                    time.sleep(1)

                    print(matrix)
                    turtle.clear()
                    screensetup.grawGrid(matrix, N)
                    screensetup.screen.update()


def heuristic(pointA, pointB):
    return abs(pointA[0] - pointB[0]) + abs(pointA[1] - pointB[1])

def drawLine(trace):
    global matrix
    global gridX
    global gridY

    moveLength = gridX[1] - gridX[0]

    for i in range(len(trace)):

        row = trace[i][0]
        col = trace[i][1]

        turtle.pu()
        turtle.goto(gridX[col] + (moveLength/2), gridY[row] + (moveLength/2))
        turtle.pd()
        turtle.circle(5)
        time.sleep(1)
        screensetup.screen.update() 
        if matrix[row][col] == 1:
            break
        
def tracking(totalTrace):
    global matrix
    global startIndex
    global endIndex
    #nextTrace = 0 
    currentX = endIndex[0]
    currentY = endIndex[1]
    trace = []
    
    for i in range(totalTrace, -1, -1):
        trace.append([currentX,currentY])
        #matrix[end[0]][end[1]] == 999 == end
        if currentY < N-1 and matrix[currentX][currentY+1] != 0 and matrix[currentX][currentY+1] != -1 and matrix[currentX][currentY+1] < i:
            #nextTrace = matrix[currentX][currentY+1]
            currentY = currentY + 1

        elif currentY > 0 and matrix[currentX][currentY-1] != 0 and matrix[currentX][currentY-1] != -1 and matrix[currentX][currentY-1] < i:
            #nextTrace = matrix[currentX][currentY-1]
            currentY = currentY - 1

        elif currentX < N-1 and matrix[currentX+1][currentY] != 0 and matrix[currentX+1][currentY] != -1 and matrix[currentX+1][currentY] < i:
            #nextTrace = matrix[currentX+1][currentY]
            currentX = currentX + 1

        elif currentX > 0 and matrix[currentX-1][currentY] != 0 and matrix[currentX-1][currentY] != -1 and matrix[currentX-1][currentY] < i:
            #nextTrace = matrix[currentX-1][currentY]
            currentX = currentX - 1

        #when it reaches to 1 (start point) save and break
        if matrix[currentX][currentY] == 1:
            #nextTrace = matrix[currentX][currentY]
            trace.append([currentX, currentY])
            break

        print(trace)
    drawLine(trace)


global N
global matrix
global c
global next_value
global notReached
global startIndex
global endIndex
N = 5
matrix = [[0 for i in range(N)] for i in range(N)]
c = 0
next_value = 0
notReached = True
startIndex = 0
endIndex = 0

while not keyboard().end:
    screensetup.grawGrid(matrix, N)
    screensetup.screen.update() 
    if c == 2 and notReached:
        print(matrix)
        path_planning()
    
    if not notReached:
        print(next_value)
        tracking(next_value)

#Hyunkun Cho, Jacob McGrew, Christopher Pfefferle, Chase Baxter