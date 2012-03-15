def combinations(items, n):
    if n==0: yield []
    else:
        for i in range(len(items)):
            for cc in combinations(items[:i]+items[i+1:],n-1):
                yield [items[i]]+cc

def uniqueCombinations(items, n):
    if n==0: yield []
    else:
        for i in range(len(items)):
            for cc in uniqueCombinations(items[i+1:],n-1):
                yield [items[i]]+cc

def uniqueCombinations2(items, n):
    """Returns all combinations not containing the next item first."""
    if n==0: yield []
    else:
        for i in range(len(items)):
            for cc in uniqueCombinations(items[:i],n-1):
                yield cc+[items[i]]
       
def selections(items, n):
    if n==0: yield []
    else:
        for i in range(len(items)):
            for ss in selections(items, n-1):
                yield [items[i]]+ss

def permutations(items):
    return combinations(items, len(items))
