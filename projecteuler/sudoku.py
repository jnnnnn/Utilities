singles = {1<<x:str(x) for x in range(9)}
def digits(n):
    for x in range(9):
        if 1<<x & n:
            yield x

def row(n):
    for y in range(9): yield n,y
        
def col(n):
    for x in range(9): yield x,n

def box_xys(boxnum):
    for x in range((boxnum // 3)*3, (boxnum // 3)*3+3):
        for y in range((boxnum%3) * 3, (boxnum%3)*3+3):
            yield x,y

def getbox(x,y):
    return (x//3)*3 + y%3

class InvalidGrid(Exception):
    pass

class sudoku:
    def __init__(self, starting=[]):
        self.grid = [0x1ff]*81
        self.log = False
        self.backtracks_required = 0
        for x, row in enumerate(starting):
            for y, c in enumerate(row):
                if c != '0':
                    self[x,y] = 1<<(int(c)-1)
    def __getitem__(self, key):
        return self.grid[key[0] * 9 + key[1]]
    def __setitem__(self, key, value):
        if value == 0:
            raise InvalidGrid("Unsolvable")
        x,y=key
        self.grid[x * 9 + y] = value

    def reduce(self):        
        for i in range(100):
            if self.solved():
                return True
            grid = self.grid[:]
            self.reduce_xys(row(x) for x in range(9))    
            self.reduce_xys(col(y) for y in range(9))
            self.reduce_xys(box_xys(box) for box in range(9))
            if grid == self.grid:
                return False

    def backtrack(self):
        for x in range(9):
            for y in range(9):
                if not self[x,y] in singles:
                    for d in digits(self[x,y]):
                        sub = sudoku()
                        sub.grid = self.grid[:]
                        sub[x,y] = 1<<d
                        sub.backtracks_required = 1
                        if self.log:
                            print ("Backtracking: placing {} in {},{}".format(d,x,y))
                        try:
                            if not sub.reduce():
                                sub.backtrack()
                            self.grid = sub.grid[:]
                            self.backtracks_required += sub.backtracks_required
                            
                            return
                        except InvalidGrid:
                            if self.log:
                                print("backtracking failed!")
                            pass
                    raise InvalidGrid("Unsolvable")
        if not self.solved():
            raise InvalidGrid("Unsolvable")

    def solve(self):
        if self.reduce():
            return
        self.backtrack()
    
    def singleOption_xys(self, xyss):
        xyss = list(list(xys) for xys in xyss)
        for xys in xyss:
            possiblesingles = self.possibles(xys)
            for d in range(9):
                n = 1<<d
                if possiblesingles & n and self.count(n, xys) == 1:
                    for x,y in xys:
                        if self[x,y] & n:
                            self[x,y] = n

    def count(self, n, xys):
        return sum(1 for x,y in xys if self[x,y]&n)
        
    def reduce_xys(self, xyss):
        xyss = list(list(xys) for xys in xyss)
        for xys in xyss:
            nums = self.possibles(xys)
            for x,y in xys:
                if not self[x,y] in singles:
                    self[x,y] &= nums

    def possibles(self, xys):
        nums = 0x1ff
        for x,y in xys:
            v = self[x,y]
            if v in singles:
                if v & (0x1ff^nums):
                    raise InvalidGrid("Invalid")
                nums ^= v
                
        return nums

    def solved(self):
        return set(self.grid).issubset(singles)

    def __str__(self):
        result = ""
        for x in range(9):
            for y in range(9):
                if self[x,y] in singles:
                    result += singles[self[x,y]]
                elif self[x,y] == 0:
                    result += "X"
                else:
                    result += "_"
                result += ' ' * (y%3==2)
            result += "\n" + "\n" * (x%3==2)
        return result
    
    def __repr__(self):
        return str(self)

    def print_possibles(self):
        result = ""
        for x in range(9):
            for y in range(9):
                ds = list(digits(self[x,y]))
                if len(ds) > 8:
                    result += '  __  '
                else:
                    result += "{:^8}".format("".join(str(d) for d in ds))
                result += ' ' * (2+4*(y%3==2))
            result += '\n' * (2+2*(x%3==2))
        print(result)
                
