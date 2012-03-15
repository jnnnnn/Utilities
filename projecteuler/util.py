import math,time

class memoize(object):
    """Tag a function with @memoize above the 'def' to only compute each result once."""
    def __init__(self,func):
        self.func = func
        self.memory = {}
    def __call__(self,*args):
        if not args in self.memory:
            self.memory[args] = self.func(*args)
        return self.memory[args]

def digits(n):
    return len(str(n))

def duration(f, *args):
    t = time.time()
    result = f(*args)
    print (f.__name__, " execution time: ", time.time()-t)
    return result

def timeMultipleRuns(n, f, *args):
    t = time.time()
    for i in range(n):
        x = f(*args)
    print (f.__name__, "execution time for {} runs:".format(n), time.time()-t)


def continuedFrac(N = 23):
    def rem(f):
        return f - int(f)
    def step(x,y):
        Ai = int(y*(math.sqrt(N)+x)/(N-x*x))
        x2 = Ai*(N-x*x)/y - x
        y2 = (N-x*x)/y
        if rem(x) > 0.000001 or rem(y) > 0.000001:
            raise Exception("{} {} {}".format(N,x,y))
        return Ai, round(x2), round(y2)
    A0 = int(math.sqrt(N))
    x,y=A0, 1
    axys = []
    for i in range(100000):
        Ai, x, y = step(x,y)        
        if (Ai,x,y) in axys:
            return axys[axys.index((Ai,x,y)):]
        axys.append((Ai,x,y))
    else:
        raise "Sequence too long, aborting"
