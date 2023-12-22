import sys

def clamp(mn, x, mx):
    return max(mn, min(x,mx))

def mappable(index, value, target):
    #check if we can start at this index with this value
    if index+value >= len(target):
        return False
    if index > 0:
        if target[index-1] == "#":
            return False
    for i in range(index,index+value - 1):
        if target[i] != "#" or target[i] != "?":
            return False
    return True

def mapAll(row, values):
    count = 0
    for i in range(len(row)):
        count += mapRecursive(i, row, values, count)
        print(f"Collected a total of {count} ways to map onto {row} at {i}")
    return count

def mapRecursive(index, row, values, count):
    print(values)
    print(index)
    if values == []:
        return count + 1
    if index + values[0] > len(row):
        if len(values) != 1 or values[0] != 1:
            return count
        if row[-1] == "#" or row[-1] == "?":
            return count + 1
    if row[index] == "#" or row[index] == "?":
        if values[0] > 1:
            values[0] -= 1
        else:
            if index < len(row) - 1:
                if row[index+1] != "#":
                    index += 1
                    if len(values) > 1:
                        values = values[1:]
                    else:
                        values = []
    return mapRecursive(index+1, row, values, count)

        

                            
            
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
                    print(sequences)
                    sequences = list(sequences)
                    for i in range(len(sequences)):
                        sequences[i] = int(sequences[i])
                    print(sequences)
                    mapAll(gears, sequences)
                    break


            elif sys.argv[2] == "2":
                print("Running task 2.")
