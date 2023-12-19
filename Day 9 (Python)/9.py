import sys

def extrapolate(nums):
    diffs = []
    for i in range(len(nums)):
        if i > 0:
            diffs.append(nums[i] - nums[i-1])
    return diffs

def extrapolateDown(table):
    diffs = extrapolate(table[-1])

    table.append(diffs)
    down = False #value determining whether to go up or down
    for num in diffs:
        if num != 0:
            down = True
    if down:
        return extrapolateDown(table)
    else:
        return extrapolateUp(table)[0][-1]

def extrapolateUp(table):
    lastExtr = 0
    for i in range(len(table)-1, -1, -1):
        appendage = table[i][-1] + lastExtr
        lastExtr = appendage
        table[i].append(appendage)
    return table


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a filepath and a task number.")
    else:
        with open(sys.argv[1]) as infile:
            if sys.argv[2] == "1":
                print("Running task 1.")
                ret = 0
                for line in infile.readlines():
                    intLine = []
                    for num in line.split():
                        intLine.append(int(num))
                    extrapolation = extrapolateDown([intLine])
                    ret += extrapolation
                print(ret)



            elif sys.argv[2] == "2":
                print("Running task 2.")


                
                
            else:
                print("Please provide a valid task number.")

    print("Completed.")
