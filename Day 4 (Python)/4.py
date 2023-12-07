import sys

def getLineScore(line, mode):
    #args:
    #line: the line to score
    #mode: 1 for task 1 scoring, 2 for task 2 winner counting
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
                    if mode == 1:
                        if score == 0:
                            score = 1
                        else:
                            score *= 2
                    else:
                        score += 1
                i = result_tuple[1]
            
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
    if len(sys.argv) < 2:
        print("Please provide a filepath and a task number.")
    else:
        with open(sys.argv[1]) as infile:
            if sys.argv[2] == "1":
                print("Running task 1.")
                score = 0
                for line in infile:
                    score += getLineScore(line, 1)
                print(score)

            elif sys.argv[2] == "2":
                print("Running task 2.")
                cardCount = 0
                lines = infile.readlines()
                timesToProcess = [1 for i in range(len(lines))]
                scoreTable = {}
                print(len(lines))
                
                for i in range(len(lines)):
                    scoreTable[i] = getLineScore(lines[i],2)
                    for p in range(timesToProcess[i]):
                        cardCount += 1
                        for q in range(i, i + scoreTable[i] + 1):
                            timesToProcess[q] += 1
                        
                                                                 
                print(f"Result: {cardCount}")
                
                
            else:
                print("Please provide a valid task number.")

    print("Completed.")
        
