import sys

def clamp(mn, x, mx):
    return max(mn, min(x,mx))

def findPossibleSequences(row):
    independentSequences = []
    sequence = ""
    for i in range(len(row)):
        if row[i] == "?" or row[i] == "#":
            sequence += row[i]
            print(sequence)
        elif row[i] == ".":
            if sequence != "":
                independentSequences.append(sequence)
            sequence = ""
    if sequence != "":
        independentSequences.append(sequence)
    return independentSequences

def mappable(index, potential, actual):
    #check if actual can map onto potential starting at index
    if index + actual == len(potential):
        if index == 0:
            return True
        else:
            if potential[index-1] == "#":
                return False
            else:
                return True
    if index + actual > len(potential):
        return False
    if index > 0:
        if potential[index-1] == "#":
            return False
    if potential[index+actual] == "#":
        return False
    return True
    
                

def mapCountSingle(potential, actual):
    #finds amount of ways a single actual value can map onto a potential one
    count = 0
    for i in range(len(potential)):
        if mappable(i, potential, actual):
            count += 1
    return count
            
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a filepath and a task number.")
    else:
        with open(sys.argv[1]) as infile:
            
            if sys.argv[2] == "1":
                print("Running task 1.")
                for line in infile:
                    line = line.split(" ")
                    gears = line[0]
                    sequences = line[1].split(",")
                    potentialSequences = findPossibleSequences(gears)
                    for potential in potentialSequences:
                        for actual in sequences:
                            actual = int(actual)
                            count = mapCountSingle(potential, actual)
                            print(f"Found {count} ways to map {actual} onto {potential}.")


            elif sys.argv[2] == "2":
                print("Running task 2.")
