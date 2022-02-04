def parse(lines):
    return (lines[0].strip(),
            [v.strip().split(' -> ') for v in lines[2:]])

def getRules(data):
    tmp = {}
    for map in data:
        tmp[map[0]] = (map[0][0]+map[1],map[1]+map[0][1])
    return tmp

def addCount(counts, pair, num=1):
    if (pair in counts):
        counts[pair] += num
    else:
        counts[pair] = num
    return counts

def pairCounts(template):
    counts = {}
    for i in range(0,len(template)):
        pair = template[i:i+2]
        counts = addCount(counts, pair)
    return counts

# Credit: Idea to keep hold of pair counts not the full string
# courtesy of https://beny23.github.io/posts/advent_of_code_2021_day_14/
# via: https://github.com/bruntonspall/adventofcode/blob/master/2021/Day%2014.ipynb
def polymerise(counts, rules):
    newcounts = {}
    for pair, num in counts.items():
        if (pair in rules):
            newcounts = addCount(newcounts, rules[pair][0], num)
            newcounts = addCount(newcounts, rules[pair][1], num)
    return newcounts

def freq(counts, last):
    f = {last:1}
    for pair, num in counts.items():
        f = addCount(f, pair[0], num)
    return f

def solve(data):
    poly = data[0]
    rules = getRules(data[1])

    counts = pairCounts(poly)
    print(counts)

    for i in range(0,40):
        counts = polymerise(counts, rules)

    f = freq(counts,poly[-1])
    print(f)
    mx = max(f.values())
    mn = min(f.values())

    print(mx, mn, mx - mn)
    return mx - mn
