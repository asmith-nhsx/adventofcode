def parse(lines):
    return [(v.strip().split('|')[0], v.strip().split('|')[1]) for v in lines]

def fiver(code, basis):
    #print (code, basis, basis[6])
    ones, fours, sevens, eights = tobase(code, basis)
    fives = len(code) == len([a for a in basis[6] if a in code])
    #print(ones, fours, sevens, eights, fives)
    if (ones + sevens > 0):
        return 3
    elif (fives > 0):
        return 5
    return 2

def sixer(code, basis):
    #print (code, basis)
    ones, fours, sevens, eights = tobase(code, basis)
    #print(ones, fours, sevens, eights)
    if (ones + fours + sevens + eights == 0):
        return 6
    elif (fours + eights == 0):
        return 0
    return 9

def tobase(code, basis):
    return (
        includes(code, basis[1]),
        includes(code, basis[4]),
        includes(code, basis[7]),
        includes(code, basis[8])
    )

def includes(code, base):
    return len(base) == len([a for a in code if a in base])

def uncode(code, codes, keys):
    for c in keys:
        if (includes(code, c)):
            return codes[c]
    print("Not found!", code)
    return -1

map = {
    2 : 1,
    3 : 7,
    4 : 4,
    7 : 8
}

def decode(input):
    uniq = [2,3,4,7]
    global map
    codes = {}
    basis = {}
    signals = [c for c in input[0].strip().split(' ')]
    for code in [c for c in signals if len(c) in uniq]:
        codes[code] = map[len(code)]
        basis[codes[code]] = code
    #print(basis)
    for code in [c for c in signals if len(c) == 6]:
        codes[code] = sixer(code, basis)
        basis[codes[code]] = code

    for code in [c for c in signals if len(c) == 5]:
        codes[code] = fiver(code, basis)
        basis[codes[code]] = code

    mult = 1000
    result = 0
    keys = sorted(codes, key=len, reverse=True)
    for out in [c for c in input[1].strip().split(' ')]:
        result += uncode(out, codes, keys) * mult
        mult /= 10
    #print(result)
    return int(result)

def solve(data):
    result = 0
    for line in data:
        result += decode(line)
    print(result)
    return result
