import sys

def clamp(mn, x, mx):
    return max(mn, min(x,mx))

def findExits(grid, r, c):
    #examine all adjacent tiles to see if they connect to this one
    #we don't need to confirm that the pipe can lead anywhere; it must loop
    adjacents = []
    if r > 0:
        if grid[r-1][c] in ["|","7","F"]:
            adjacents.append((r-1,c))
    if r < len(grid[0]):
        if grid[r+1][c] in ["|","L","J"]:
            adjacents.append((r+1,c))
    if c > 0 and len(adjacents) < 2:
        if grid[r][c-1] in ["-","L","F"]:
            adjacents.append((r,c-1))
    if c < len(grid[0]) and len(adjacents) < 2:
        if grid[r][c+1] in ["-","7","J"]:
            adjacents.append((r,c+1))
    return adjacents

def findS(grid):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "S":
                return r, c

def compatible(leaving, entering, direction):
    leftcompatible = ["-","L","F"]
    rightcompatible = ["-","J","7"]
    upcompatible = ["|","7","F"]
    downcompatible = ["|","L","J"]
    if direction == "LEFT":
        if entering in leftcompatible:
            return True
    elif direction == "RIGHT":
        if entering in rightcompatible:
            return True
    elif direction == "DOWN":
        if entering in downcompatible:
            return True
    elif direction == "UP":
        if entering in upcompatible:
            return True
    return False
        

def findConnection(grid,r,c,last):
    cangoleft = ["-","J","7"]
    cangoright = ["-","L","F"]
    cangodown = ["|","7","F"]
    cangoup = ["|","L","J"]
    this = grid[r][c]
    lastR = last[0]
    lastC = last[1]

    if this in cangoleft:
        if last != (r,c-1):
            if c > 0:
                leftCell = grid[r][c-1]
                if compatible(this, leftCell, "LEFT"):
                    return (r, c-1),False
                
    if this in cangoright:
        if last != (r, c+1):
            if c < len(grid[0]):
                rightCell = grid[r][c+1]
                if compatible(this, rightCell, "RIGHT"):
                    return (r, c+1),False

    if this in cangoup:
        if last != (r-1, c):
            if r > 0:
                upCell = grid[r-1][c]
                if compatible(this, upCell, "UP"):
                    return (r-1, c),False

    if this in cangodown:
        if last != (r+1, c):
            if r < len(grid):
                downCell = grid[r+1][c]
                if compatible(this,downCell, "DOWN"):
                    return (r+1, c),False
                
    for row in range(clamp(0,r-1,len(grid)), clamp(0,r+2,len(grid))):
        for col in range(clamp(0,c-1,len(grid)), clamp(0, c+2, len(grid))):
            if grid[row][col] == "S":
                return (row,col),True

def passType(grid, r, c):
    passableTypes = []
    this = grid[r][c]
    
    

def findLoop(grid, r, c):
    start = (r,c)
    new, truth = findConnection(grid, r, c, start)
    pipe = [start,new]
    last = start
    count = 2
    while True:
        
        tmp = new
        new, truth = findConnection(grid, new[0], new[1], last)
        if truth == False:
            pipe.append(new)
            last = tmp
            count += 1
        else:
            pipe.append(new)
            count += 1
            break

    return (count // 2, pipe)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a filepath and a task number.")
    else:
        with open(sys.argv[1]) as infile:
            grid = infile.readlines()
            r, c = findS(grid)
            adjacents = findExits(grid, r, c)
            r, c = adjacents[0]

            pipeLength, pipeCoords = findLoop(grid, r, c)
            
            if sys.argv[2] == "1":
                print("Running task 1.")
                print(pipeLength)
                
                
                
                



            elif sys.argv[2] == "2":
                print("Running task 2.")
                passable = []
                for row in range(len(grid)):
                    passable.append([])
                    for col in range(len(grid[row])):
                        passable[row].append(passType(grid[row][col]))
                
