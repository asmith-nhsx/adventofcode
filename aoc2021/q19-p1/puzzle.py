import itertools as it

def parse(lines):
    results, scanner = [], []
    for line in lines:
        if (line.startswith('---')):
            if len(scanner) > 0:
                results.append(scanner)
            scanner = []
        elif (len(line)) > 2:
            scanner.append([int(num) for num in line.strip().split(',')])

    return results

def scan(s1, s2):
    result = (0,[0,0,0])
    for a in range(2000, -2000, -1):
        for b in range(2000, -2000, -1):
            for c in range(2000, -2000, -1):
                m = compare(s1, s2, [a,b,c])
                result = m, [a,b,c] if result[0] < m else result
    return result

def rotate(d, s):
    r = []
    #print(f":{d}")
    for index in d:
        sign = -1 if index < 0 else 1
        #print(f":::{index},{sign}")
        r.append(sign * s[abs(index)-1])
    return r

def compare(s1, s2, t0):
    rotations = [
        [1, 2, 3],
        [1, 3,-2],
        [1,-2,-3],
        [1,-3, 2],

        [2,-1, 3],
        [2, 3, 1],
        [2, 1,-3],
        [2,-3,-1],

        [-1,-2, 3],
        [-1,-3,-2],
        [-1, 2,-3],
        [-1, 3, 2],

        [-2, 1, 3],
        [-2,-3, 1],
        [-2,-1,-3],
        [-2, 3,-1],

        [3, 2, 1],
        [3, 1, 2],
        [3,-2, 1],
        [3,-1,-2],

        [-3,-2,-1],
        [-3,-1, 2],
        [-3, 2, 1],
        [-3, 1,-2]
    ]
    add = lambda x, y : [x[i] + y[i] for i in range(3)]
    matched = 0
    for r in rotations:
        m = 0
        for b1 in s1:
            for b2 in s2:
                b3 = rotate(r, b2)
                a = add(t0, b3)
                #print(f"{b1}, {a}, {b2}, {r}")
                if b1 == a:
                    m += 1
        matched = m if m > matched else matched
    return matched

def solve(data):
    #print(data)
    #t0 = [68,-1246,-43]

    #pairs = {}
    #for i in range(len(data)):
    #    for j in range(len(data)):
    #        if (i != j):
    #            x = j if i < j else i
    #            y = i if i < j else j
    #            key = (x, y)
    #            if key not in pairs:
    #                pairs[key] = 1
    #                print(f"Matching {i} and {j}")
                    #m = scan(data[i], data[j])
                    #print(f"Matched {m[0]} beacons at {m[1]}")


    d0 = [[-618,-824,-621]]
    d1 = [[686,422,578]]
    t = []
    for b1 in data[0]:
        for b2 in data[1]:
            for b11 in b1:
                for b22 in b2:
                    t.append(abs(b11) + abs(b22))
                    t.append(abs(b11) - abs(b22))
                    t.append(abs(b22) - abs(b11))
                    t.append(-abs(b11) - abs(b22))
    print(t)
    #result = (0,[0,0,0])
    #for p in it.permutations(t,3):
        #if p[0] == 68 and p[1] == -1246:
        #    print(p)
    #    m = compare(data[0], data[1], p)
        #result = m, p if result[0] < m else result
    #    if m > 11:
    #        print(f"Matched {m} for position {p}")
    #print(result)
    return 0
