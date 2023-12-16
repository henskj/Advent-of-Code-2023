import sys
from enum import Enum
from functools import total_ordering

if len(sys.argv) < 2:
    print("Please provide a filepath and a task number.")
else:
    mode = sys.argv[2]


class SymbolValue(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    T = 10
    if mode == "1":
        J = 11
    elif mode == "2":
        J = 1
    else:
        print("Something's gone wrong with the mode in SymbolValue.")
    Q = 12
    K = 13
    A = 14

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

symbolMap = {
    '2': SymbolValue.TWO,
    '3': SymbolValue.THREE,
    '4': SymbolValue.FOUR,
    '5': SymbolValue.FIVE,
    '6': SymbolValue.SIX,
    '7': SymbolValue.SEVEN,
    '8': SymbolValue.EIGHT,
    '9': SymbolValue.NINE,
    'T': SymbolValue.T,
    'J': SymbolValue.J,
    'Q': SymbolValue.Q,
    'K': SymbolValue.K,
    'A': SymbolValue.A
}
    
def handType(handSymbols, mode):
    
    keys = list(symbolMap.keys())
    counts = [0 for i in range(len(keys))]
    jokers = 0
    for symbol in handSymbols:
        for i in range(len(keys)):
            if symbol == keys[i]:
                if symbol == "J":
                    jokers += 1
                counts[i] += 1
                break

    if mode == "1" or jokers == 0: 
        if 5 in counts:
            return "fioak"
        elif 4 in counts:
            return "fooak"
        elif 3 in counts:
            if 2 in counts:
                return "fh"
            else:
                return "thoak"
        elif 2 in counts:
            if counts.count(2) == 2:
                return "twopa"
            else:
                return "onepa"
        else:
            return "highc"
    elif mode == "2":
        """
        Checks for jokers go in here. We only go here at all if there are
        actually jokers; this means we can strip away any results that would
        require no jokers to reach, simplifying away a lot of what would
        otherwise be very logically complex and error-prone.
        """
        otherMaxCount = max(counts[:9] + counts[10:])
        maxCount = jokers + otherMaxCount

        if maxCount == 5:
            return "fioak"
        elif maxCount == 4:
            return "fooak"
        #3 in counts with jokers becomes fooak or fioak, so we skip here
        elif 2 in counts:
            if maxCount == 4:
                return "fooak"
            elif jokers == 1 and counts.count(2) == 2:
                return "fh"
            elif jokers == 2:
                return "thoak"
            elif jokers == 1:
                return "thoak"
        else:
            if jokers == 1:
                return "onepa"
    
    
    
def bucketSortHands(hands):
    #Bucket sorts the hands. Takes entire lines, ignores the point score
    #Does include the point score in the dict though.
    bucketbucket = {}
    bucketbucket["highc"] = []  # high card
    bucketbucket["onepa"] = []  # one pair
    bucketbucket["twopa"] = []  # two pair
    bucketbucket["thoak"] = []  # three of a kind
    bucketbucket["fh"]    = []  # full house
    bucketbucket["fooak"] = []  # four of a kind
    bucketbucket["fioak"] = []  # five of a kind
    
    for hand in hands:
        symbols = hand.split()[0]
        hand = hand[:-1]
        typ = handType(symbols, mode)
        bucketbucket[typ].append(hand)
    return bucketbucket

def sortBucketsAscending(bucketbucket):
    sortedBuckets = []
    for key in bucketbucket.keys():
        bucket = bucketbucket[key]
        if len(bucket) > 1:
            sortBucket(bucket)
            for ele in bucket:
                sortedBuckets.append(ele)
        elif len(bucket) == 1:
            sortedBuckets.append(bucket[0])
    return sortedBuckets
        
        
def sortBucket(bucket):
    #merge sort the bucket
    if len(bucket) > 1:
        midIndex = len(bucket)//2
        left = bucket[:midIndex]
        right = bucket[midIndex:]

        sortBucket(left)
        sortBucket(right)

        i = j = k = 0

        while i < len(left) and j < len(right):
            if handGreaterThanOrEqual(right[j],left[i]):
                bucket[k] = left[i]
                i += 1
            else:
                bucket[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            bucket[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            bucket[k] = right[j]
            j += 1
            k += 1

def handGreaterThanOrEqual(hand1, hand2):
    for i in range(5):
        left = hand1[i]
        right = hand2[i]
        if symbolMap[left] > symbolMap[right]:
            return True
        elif symbolMap[left] < symbolMap[right]:
            return False
    return True
    
            
        
    
if __name__ == "__main__":
    with open(sys.argv[1]) as infile:
        if mode == "1":
            print("Running task 1.")
            lines = infile.readlines()
            bucketbucket = bucketSortHands(lines)
            sortedBuckets = sortBucketsAscending(bucketbucket)
            print(sortedBuckets)
            i = 1
            score = 0
            for hand in sortedBuckets:
                score += int(hand.split()[1]) * i
                i += 1
            print(score)
                

        elif mode == "2":
            print("Running task 2.")
            lines = infile.readlines()
            bucketbucket = bucketSortHands(lines)
            sortedBuckets = sortBucketsAscending(bucketbucket)
            i = 1
            score = 0
            for hand in sortedBuckets:
                score += int(hand.split()[1]) * i
                i += 1
            print(score)

    print("Completed.")
