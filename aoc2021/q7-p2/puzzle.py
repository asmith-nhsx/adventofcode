def parse(lines):
    return [int(v) for v in lines[0].split(',')]

def mode(list):
    return max(set(list), key=list.count)

fuelcost = {}

def fuel(steps):
    global fuelcost
    try:
        return fuelcost[steps]
    except KeyError:
        fuelcost[steps] = sum([i for i in range(1, steps+1)])
        return fuelcost[steps]

def cost(list, pos):
    return sum([fuel(abs(pos - v)) for v in list])

def solve(data):
    lw = min(set(data))
    up = max(set(data))

    m = min([i for i in range(lw, up + 1)], key= lambda k: cost(data, k))
    c = cost(data, m)

    print(m, c)
    return c
