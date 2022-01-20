def parse(lines):
    return [v.strip().split("-") for v in lines]

def countSmall(path):

    small = []
    for s in [p for p in path.split(',') if p == p.lower() and p != 'start']:
        if s not in small:
            small.append(s)
        else:
            return False
    return True

def walk(cave, paths, tree, path, small, call):
    call += 1
    if (countSmall(path)):
        paths.append(path)
        if cave != 'end':
            for turn in tree[cave]:
                if turn != 'start':
                    walk(turn, paths, tree, path + ',' + turn, small, call)

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
    small = []
    pathnum = 0
    cave = 'start'
    #while len(paths) > 0 and pathnum < 30:
    print("In cave ", cave)
    path = cave
    walk(cave, paths, tree, path, small, 0)

    final = [p for p in paths if p.find('end') > -1]
    print(final)
    result = len(final)
    print(result)
    return result

#start,A,b,A,c,A,end
#start,A,b,A,end
#start,A,b,end
#start,A,c,A,b,A,end
#start,A,c,A,b,end
#start,A,c,A,end
#start,A,end
#start,b,A,c,A,end
#start,b,A,end
#start,b,end
