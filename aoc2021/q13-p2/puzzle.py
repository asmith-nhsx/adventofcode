def parse(lines):
    return ([[int(o) for o in v.strip().split(',')] for v in lines if not v.startswith('fold along') and v.strip() != ''],
            [v.strip()[11:].split('=') for v in lines if v.startswith('fold along')])

def foldUp(fold, point):
    return foldLeft(fold, point, 1)

def foldLeft(fold, point, dir=0):
    if (point[dir] > fold):
        point[dir] = fold - (point[dir] - fold)
    return point

def coord(p):
    return str(p[0])+":"+str(p[1])

def display(paper):
    w = max([p[0] for p in paper])
    h = max([p[1] for p in paper])
    code = ''
    for y in range(0,h+1):
        for x in range(0,w+1):
            if (len([p for p in paper if p[1] == y and p[0] == x]) > 0):
                code += '#'
            else:
                code += '.'
        code += '\n'
    print("---------------------")
    print(code)
    return code

def solve(data):
    paper = data[0]
    folds = data[1]
    ops = {
     'x': foldLeft,
     'y': foldUp
    }

    for fold in folds:
        folded = {}
        for d in paper:
            e = ops[fold[0]](int(fold[1]), d)
            if (coord(e) not in folded):
                folded[coord(e)] = e
        paper = folded.values()
    return display(paper)
