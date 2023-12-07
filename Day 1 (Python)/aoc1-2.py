with open("input.txt") as infile:
    numsmap = {"one": 1, "1": 1, "two": 2, "2": 2, "three": 3, "3": 3, "four": 4,
               "4": 4, "five": 5, "5": 5, "six": 6, "6": 6, "seven": 7, "7": 7,
               "eight": 8, "8": 8, "nine": 9, "9": 9}
    backwards = {}
    for key in numsmap:
        new_key = key[::-1]
        backwards[new_key] = numsmap[key]
    nums = []
    for line in infile:
        first = -1
        second = -1
        broken = False
        for i in range(len(line)):
            if broken:
                broken = False
                break
            for key in numsmap.keys():
                if line[i:].startswith(key):
                    first = numsmap[key]
                    broken = True
                    break
        for i in range(-1, (len(line) * -1 - 1), -1):
            if broken:
                broken = False
                break
            for key in backwards.keys():
                    if line[i::-1].startswith(key):
                        second = backwards[key]
                        broken = True
                        break
        nums.append((first * 10) + second)

print(sum(nums))
    
    
    
