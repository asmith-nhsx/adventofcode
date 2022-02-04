def parse(lines):
    return (lines[0].strip(),
            [v.strip().split(' -> ') for v in lines[2:]])

def getRules(data):
    tmp = {}
    for map in data:
        tmp[map[0]] = map[0][0]+map[1]
    return tmp

def polymerise(poly, rules):
    poly2 = ''
    for i in range(0,len(poly)):
        pair = poly[i:i+2]
        if pair in rules:
            poly2 += rules[pair]
        else:
            poly2 += pair
    return poly2

def freq(poly):
    f = {}
    for b in poly:
        if b in f:
            f[b] += 1
        else:
            f[b] = 1
    return f

def solve(data):
    poly = data[0]
    rules = getRules(data[1])
    for i in range(0,10):
        poly = polymerise(poly, rules)
    f = freq(poly)
    mx = max(f.values())
    mn = min(f.values())
    print(mx, mn, mx - mn)
    return mx - mn
