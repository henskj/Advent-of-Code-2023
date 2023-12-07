def getLineScore(line):
    winners = []
    passed_useless_info = False #switch to true when past the :
    passed_winners = False #switch to true when past the |
    i = -1
    score = 0
    while i < len(line) - 1:
        i += 1
        char = line[i]
        if not passed_useless_info:
            if char == ":":
                passed_useless_info = True
        elif not passed_winners:
            if char == "|":
                passed_winners = True
            if char.isdigit():
                result_tuple = numStrToInt(line,i)
                winners.append(result_tuple[0])
                i = result_tuple[1]
                
        else:
            if char.isdigit():
                result_tuple = numStrToInt(line,i)
                owned_num = result_tuple[0]
                if owned_num in winners:
                    if score == 0:
                        score = 1
                    else:
                        score *= 2
                i = result_tuple[1]
            
            
    print(winners)
    print(score)
    print("\n")
    return score
        
def numStrToInt(line, ind):
    #given the first index of a number, returns a tuple containing:
    #(number as an int, new index)
    numStr = ""
    while line[ind].isdigit():
        numStr += line[ind]
        ind += 1
    ret = int(numStr)
    return (ret,ind)
if __name__ == "__main__":
    with open("input4.txt") as infile:
        score = 0
        for line in infile:
            score += getLineScore(line)
        print(score)
