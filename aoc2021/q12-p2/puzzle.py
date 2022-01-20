def parse(lines):
    return [v.strip().split("-") for v in lines]

def countSmall(path):
    small = []
    small2 = ''
    for s in [p for p in path.split(',') if p == p.lower() and p != 'start']:
        if s not in small:
            small.append(s)
        elif small2 == '':
            small2 = s
        else:
            return False
    return True

def walk(cave, paths, tree, path, call):
    call += 1
    if (countSmall(path)):
        paths.append(path)
        if cave != 'end':
            for turn in tree[cave]:
                if turn != 'start':
                    walk(turn, paths, tree, path + ',' + turn, call)

def solve(data):
    tree = {}
    for c in data:
        if c[0] in tree:
            tree[c[0]].append(c[1])
        else:
            tree[c[0]] = [c[1]]
        if c[1] in tree:
            tree[c[1]].append(c[0])
        else:
            tree[c[1]] = [c[0]]
    print(tree)

    path = ''
    paths = []
    cave = 'start'
    walk(cave, paths, tree, path, 0)

    final = [p for p in paths if p.find('end') > -1]
    #print(final)
    result = len(final)
    print(result)
    return result
