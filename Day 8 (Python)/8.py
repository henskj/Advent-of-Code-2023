import sys

def move(graph, cur, instruction):
    if instruction == "R":
        return graph[cur][1]
    else:
        return graph[cur][0]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a filepath and a task number.")
    else:
        with open(sys.argv[1]) as infile:
            if sys.argv[2] == "1":
                print("Running task 1.")
                instructions = infile.readline()[:-1]
                infile.readline() #skip blank line
                graph = {}
                for line in infile:
                    #lines are constant length
                    #this means we can just use indices directly
                    origin = line[:3]
                    left = line[7:10]
                    right = line[12:15]
                    graph[origin] = (left,right)
                cur = "AAA"
                count = 0
                index = 0
                instructionLength = len(instructions)
                while cur != "ZZZ":
                    count += 1
                    tmp = cur
                    cur = move(graph, cur, instructions[index])
                    #print(f"Moved from {tmp} to {cur}.")
                    index += 1
                    if index >= instructionLength:
                        index = 0
                print(f"Result: {count}")
                        
                    
                    

            elif sys.argv[2] == "2":
                print("Running task 2.")
                
                
