import sys

def move(graph, cur, instruction):
    if instruction == "R":
        return graph[cur][1]
    else:
        return graph[cur][0]

def ghostMove(graph, cur, instruction):
    newCur = []
    #writing two loops is unaesthetic but saves us from thousands of if checks
    if instruction == "R":
        for pos in cur:
            newCur.append(graph[pos][1])
    else:
        for pos in cur:
            newCur.append(graph[pos][0])
    return newCur

def ghostDone(cur):
    for pos in cur:
        if pos[-1] != "Z":
            return False
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a filepath and a task number.")
    else:
        with open(sys.argv[1]) as infile:
            mode = sys.argv[2]
            instructions = infile.readline()[:-1]
            infile.readline() #skip blank line
            graph = {}
            count = 0
            index = 0
            instructionLength = len(instructions)
            if mode == "2":
                cur = []
                
            for line in infile:
                #lines are constant length
                #this means we can just use indices directly
                origin = line[:3]
                left = line[7:10]
                right = line[12:15]
                graph[origin] = (left,right)
                if mode == "2" and origin[-1] == "A":
                    cur.append(origin)
                    
            if mode == "1":
                print("Running task 1.")
                cur = "AAA"
                while cur != "ZZZ":
                    count += 1
                    #tmp = cur
                    cur = move(graph, cur, instructions[index])
                    #print(f"Moved from {tmp} to {cur}.")
                    index += 1
                    if index >= instructionLength:
                        index = 0
                print(f"Result: {count}")
                        
                    
                    

            elif mode == "2":
                print("Running task 2.")
                print(cur)
                while not ghostDone(cur):
                    count += 1
                    if count % 1000000000 == 0:
                        print(count)
                    cur = ghostMove(graph, cur, instructions[index])

                    index += 1
                    if index >= instructionLength:
                        index = 0
                print(f"Result: {count}")
                
                
