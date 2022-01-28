def parse(lines):
    return ([[int(o) for o in v.strip().split(',')] for v in lines if not v.startswith('fold along') and v.strip() != ''],
            [v.strip()[11:].split('=') for v in lines if v.startswith('fold along')])

def foldUp(fold, point):
    if (point[1] > fold):
        point[1] = fold - (point[1] - fold)
    return point

def foldLeft(fold, point):
    if (point[0] > fold):
        point[0] = fold - (point[0] - fold)
    return point

def coord(p):
    return str(p[0])+":"+str(p[1])

def display(paper):
    w = max([p[0] for p in paper])
    h = max([p[1] for p in paper])
    dots = 0
    print("---------------------")
    for y in range(0,h+1):
        for x in range(0,w+1):
            if (len([p for p in paper if p[1] == y and p[0] == x]) > 0):
                dots += 1
                print('#', end='')
            else:
                print('-', end='')
        print('')
    return dots

def solve(data):
    paper = data[0]
    folds = data[1]
    ops = {
     'x': foldLeft,
     'y': foldUp
    }

    fold = folds[0]
    folded = {}
    for d in paper:
        e = ops[fold[0]](int(fold[1]), d)
        if (coord(e) not in folded):
            folded[coord(e)] = e
    result = len(folded)
    return result
