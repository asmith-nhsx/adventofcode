# Initially trying to do this using string indexing
# gets pretty spicy - so switched to using nested lists
def parse(lines):
    return [num.strip() for num in lines]

def component(x, i = 0):
    pos = x.index(',')
    if (i != 0):
        return x[pos+1:].rstrip(']')
    return x[:pos].lstrip('[')

def isNum(x):
    if (x is not None and len(x) > 4):
        return x.find(',') and x[0] == '[' and x[-1] == ']'
    return False

def leftish(x):
    return int(component(x))

def rightish(x):
    return int(component(x, 1))

def magnitude(x):
    return

def split(x):
    l = x // 2
    r = (x + 1) // 2
    return f'[{l},{r}]'

def splits(x):
    pos = 0
    result = ''
    while (pos < len(x) - 1):
        if (x[pos] in '1234567890' and x[pos+1] in '1234567890'):
            s = split(int(x[pos:pos+2]))
            result += s
            print(f'result: {result}, splitting: {x[pos:pos+2]}, split:{s}')
            pos +=2

        else:
            result += x[pos]
            pos += 1
    result += x[:-1]
    print(f'returning {result} from splits')
    return result

def explode(x):
    pos, nest, leftp, extra, start, end, rightp = 0, 0, 0, 0, 0, 0, 0
    num, left, right, result = '', '', '', ''
    while (pos < len(x)):
        if (x[pos] in '1234567890'):
            if (num != ''):
                rightp = pos
                r = rightish(num) + int(x[rightp])
                if (r > 9):
                    right = split(r)
                else:
                    right = str(r)
                break
            else:
                leftp = pos
        if (num == ''):
            if (x[pos] == '['):
                nest += 1
            elif (x[pos] == ']'):
                nest -= 1
        if (nest > 4):
            start = pos
            end = x[start:].find(']') + start
            extra = x[start+1:end].rfind('[')
            if (extra > -1 and extra + start < end):
                start += extra + 1
            num = x[start:end+1]
            print(f'start={start},end={end},extra={extra},num={num}')
            if (leftp > 0):
                l = leftish(num) + int(x[leftp])
                if (l > 9):
                    left = split(l)
                else:
                    left = str(l)
            pos = end
            nest = 0
        else:
            pos += 1

    if (num != ''):
        result = x[0:leftp]+left+x[leftp+1:start] if leftp > 0 else x[0:start]
        result += '0'
        result += x[end+1:rightp]+right+x[rightp+1:] if rightp > 0 else x[end+1:]
        #print (f"x={x}")
        #print (f"num={num}, leftp={leftp}, x[leftp]={x[leftp]}, start={start}, end={end}, rightp={rightp}, x[rightp]={x[rightp]}")
        return result, True
    return x, False

def reduce(x):
    result = x
    found = True
    while (found):
        print(f'before explode {result}')
        result, found = explode(result)
        print(f'after explode {result}')
    print(f'returning {result} from reduce')
    return result

def add(x, y):
    result = f'[{y},{x}]'
    return reduce(result)

def sum(nums):
    result = nums[0]
    print(f'start:{result}')
    for x in nums[1:]:
        print(f'Adding:{x}')
        result = add(x, result)
        print(f'Sum:{result}')
    return result

def solve(data):
    result = sum(data)
    return result
