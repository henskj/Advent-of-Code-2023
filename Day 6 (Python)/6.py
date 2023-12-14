import sys

def getWins(time, dist):
    #Get the amount of possible wins for a time-dist pair.
    count = 0
    for i in range(time, -1, -1):
        #the distance you get by spending i time accelerating
        velocity = i
        remainingTime = time - velocity
        if velocity * remainingTime > dist:
            count += 1
    return count

def getLists(timeLine, distLine):
    times = []
    dists = []
    timeDigit = ""
    distDigit = ""
    for timeChar, distChar in zip(timeLine,distLine):
        if timeChar.isdigit():
            timeDigit += timeChar
        else:
            if timeDigit != "":
                times.append(int(timeDigit))
                timeDigit = ""
        if distChar.isdigit():
            distDigit += distChar
        else:
            if distDigit != "":
                dists.append(int(distDigit))
                distDigit = ""
    return times, dists

def joinLists(times, dists):
    time = ""
    dist = ""
    for i in range(len(times)):
        time += str(times[i])
        dist += str(dists[i])
    time = int(time)
    dist = int(dist)
    return time, dist

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a filepath and a task number.")
    else:
        with open(sys.argv[1]) as infile:
            if sys.argv[2] == "1":
                print("Running task 1.")
                possibleWinsByRace = []
                timeLine = infile.readline()
                distLine = infile.readline()
                times, dists = getLists(timeLine, distLine)
                


                wins = []
                for i in range(len(times)):
                    winCount = getWins(times[i],dists[i])
                    wins.append(winCount)
                print(wins)
                ret = 1
                for i in range(len(wins)):
                    ret = ret * wins[i]
                print(ret)

            elif sys.argv[2] == "2":
                print("Running task 2.")
                timeLine = infile.readline()
                distLine = infile.readline()
                time, dist = getLists(timeLine, distLine)
                time, dist = joinLists(time, dist)

                print(time)
                print(dist)
                print(getWins(time, dist))

                
                
            else:
                print("Please provide a valid task number.")

    print("Completed.")
