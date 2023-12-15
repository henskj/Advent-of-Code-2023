import sys
from enum import Enum
from functools import total_ordering

"""
('symbolValue', ['2', '3', '4', '5', '6', '7',
                                       '8', '9', 'T', 'J', 'Q', 'K', 'A'])

"""


class SymbolValue(Enum):
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    T = 9
    J = 10
    Q = 11
    K = 12
    A = 13

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
    
def handType(handSymbols):
    
    keys = list(symbolMap.keys())
    counts = [0 for i in range(len(keys))]
    for symbol in handSymbols:
        for i in range(len(keys)):
            if symbol == keys[i]:
                counts[i] += 1
                break
            
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
        bucketbucket[handType(symbols)].append(hand)
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
    if len(sys.argv) < 2:
        print("Please provide a filepath and a task number.")
    else:
        with open(sys.argv[1]) as infile:
            if sys.argv[2] == "1":
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
                

            elif sys.argv[2] == "2":
                print("Running task 2.")


                
                
            else:
                print("Please provide a valid task number.")

    print("Completed.")
