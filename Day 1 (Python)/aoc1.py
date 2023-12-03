def getFirst(line):
    for char in line:
        if char.isdigit():
            return int(char)

def getLast(line):
    for i in range(-1, (len(line) * -1 - 1), -1):
        #iterate backwards through the line without reversing it
        char = line[i]
        if char.isdigit():
            return int(char)


with open("input.txt") as infile:
    nums = []
    for line in infile:
        first = getFirst(line)
        last = getLast(line)
        
        nums.append((first * 10) + last)

print(sum(nums))
