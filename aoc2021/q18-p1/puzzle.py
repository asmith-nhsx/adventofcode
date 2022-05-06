def parse(lines):
    return [num.strip() for num in lines]

def parseNum(lines):
    return [toNum(num.strip()) for num in lines]

def toNum(num):
    return eval(num)

def magnitude(x):
    if (type(x) is int):
        return x
    m = 3 * magnitude(x[0])
    m += 2 * magnitude(x[1])
    return m

def reduce(x):
    while (True):
        l = str(x)
        while (True):
            if (not explode(x)[0]):
                break
            #print(f"after explode:{x}")
        splits(x)
        #print(f"after split  :{x}")
        if (l == str(x)):
            break
    return x

def add(x, y):
    s = [y, x]
    #print(f"after add    :{s}")
    return reduce(s)

def addNum(num, path, val):
    l = len(path)
    if (l == 1):
        num[path[0]] += val
    elif (l == 2):
        num[path[0]][path[1]] +=  val
    elif (l == 3):
        num[path[0]][path[1]][path[2]] +=  val
    elif (l == 4):
        num[path[0]][path[1]][path[2]][path[3]] +=  val
    else:
        num[path[0]][path[1]][path[2]][path[3]][path[4]] += val

def editNum(num, path, val):
    l = len(path)
    if (l == 1):
        num[path[0]] = val
    elif (l == 2):
        num[path[0]][path[1]] = val
    elif (l == 3):
        num[path[0]][path[1]][path[2]] = val
    elif (l == 4):
        num[path[0]][path[1]][path[2]][path[3]] = val
    else:
        num[path[0]][path[1]][path[2]][path[3]][path[4]] = val

def explode(num, x=None, path=None, carry=None, add=0, exp=False):

    if (path is None):
        path = []
    if (carry is None):
        carry = []
    if (x is None):
        x = num

    if (type(x) is int):
        #print(f'Primitve:{x},path:{path},carry={carry},exp={exp}')
        if (add > 0):
            # add the right hand number to the nearest number on the right
            addNum(num, path, add)
            # once added signal the end of the recursive call
            add = -1
        return exp, path, add

    if (type(x[0]) is int and type(x[1]) is int):
        #print(f'Base:{x},path:{path},carry:{carry},exp={exp}')
        if (not exp and len(path) >= 4):
            if (len(carry) > 0):
                # add the left hand number to the nearest number on the left
                addNum(num, carry, x[0])
            # replace this number with a 0
            editNum(num, path, 0)
            return True, carry, x[1]

    for i in range(0,2):
        exp, carry, add  = explode(num, x[i], path + [i], carry, add, exp)
        if (add == -1):
            break

    return exp, carry, add

def split(x):
    l = x // 2
    r = (x + 1) // 2
    return [l,r]

def splits(num, x=None, path=None):
    if (path is None):
        path = []
    if (x is None):
        x = num

    if (type(x) is int):
        #print(f'Primitve:{x}, path:{path}')
        if (x > 9):
            val = split(x)
            editNum(num, path, val)
            return True
        return False

    for i in range(0,2):
        b = splits(num, x[i], path + [i])
        if (b):
            return True
    return False

def sum(nums):
    result = nums[0]
    #print(f'start  :{result}')
    for x in nums[1:]:
        #print(f'Adding :{x}')
        result = add(x, result)
        #print(f'Sum    :{result}')
    return result

def solve(data):
    s = sum(data)
    return magnitude(s)
