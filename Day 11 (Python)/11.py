import sys

def markRows(universe):
    markedRows = []
    for r in range(len(universe)):
        if not "#" in universe[r]:
            markedRows.append(r)
            
    return markedRows

def markCols(universe):
    markedCols = []
    for c in range(len(universe[0])):
        foundGalaxy = False
        for r in range(len(universe)):
            if universe[r][c] == "#":
                foundGalaxy = True
        if not foundGalaxy:
            markedCols.append(c)

    return markedCols

def findGalaxyCoords(universe):
    galaxies = []
    for row in range(len(universe)):
        for col in range(len(universe[0])):
            if universe[row][col] == "#":
                galaxies.append((row,col))
    return galaxies

def shortestPath(universe, origin, destination, markedRows, markedCols, extra):
    #extra is how much to embiggen empty rows/cols by
    lowR = min(origin[0], destination[0])
    highR = max(origin[0], destination[0])

    lowC = min(origin[1], destination[1])
    highC = max(origin[1], destination[1])

    ret = 0

    for r in range(lowR,highR):
        ret += 1
        if r in markedRows:
            ret += extra
    for c in range(lowC,highC):
        ret += 1
        if c in markedCols:
            ret += extra
            
    return ret

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a filepath and a task number.")
    else:
        with open(sys.argv[1]) as infile:
            
            if sys.argv[2] == "1":
                print("Running task 1.")
                extra = 1
            elif sys.argv[2] == "2":
                print("Running task 2.")
                extra = 999999
                
            universe = []
            for line in infile:
                line = line[0:-1]
                universe.append(list(line))

            markedRows = markRows(universe)
            markedCols = markCols(universe)

            galaxyCoords = findGalaxyCoords(universe)

            distances = []
            for i in range(len(galaxyCoords)):
                for p in range(i+1,len(galaxyCoords)):
                    fromGal = galaxyCoords[i]
                    toGal = galaxyCoords[p]
                    distances.append(shortestPath(universe, fromGal,toGal,
                                                  markedRows, markedCols,
                                                  extra))

            print(sum(distances))
