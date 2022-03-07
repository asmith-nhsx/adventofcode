def parse(lines):
    return [[int(o) for o in v.strip()] for v in lines]

def minPath(p, e):
    return (e[0] - p[0]) + (e[1] - p[1])

def popOpen(open, score):
    minimal = -1
    for p in open:
        if score[p] < minimal or minimal == -1:
            found = p
            minimal = score[p]
    open.remove(found)
    return found

def getPath(came, current, data):
    path = [current]
    total = 0
    while current in came.keys():
        total += data[current[0]][current[1]]
        current = came[current]
        path.append(current)
    path.reverse()
    print(path)
    return total

def getNeighbours(p, sz):
    neighbours = []
    if (0 <= p[0]-1 < sz):
        neighbours.append((p[0]-1, p[1]))
    if (0 <= p[0]+1 < sz):
        neighbours.append((p[0]+1, p[1]))
    if (0 <= p[1]-1 < sz):
        neighbours.append((p[0], p[1]-1))
    if (0 <= p[1]+1 < sz):
        neighbours.append((p[0], p[1]+1))
    return neighbours

def solve(data):
    # A* search algorithm - something I had never come across before
    # credit https://github.com/bruntonspall/adventofcode/blob/master/2021/Day%2015.ipynb
    # and https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode

    #print(data)
    sz = len(data)
    start = (0,0)
    end = (sz-1,sz-1)

    open = [start]
    came = {}
    score = {start: 0}
    guess = {start: minPath(start,end)}

    while len(open) > 0:
        current = popOpen(open ,guess)
        if (current == end):
            total = getPath(came, current, data)
            print(total)
            return total

        for n in getNeighbours(current, sz):
            tentative = guess[current] + data[n[0]][n[1]]
            if n not in guess or tentative < guess[n]:
                came[n] = current
                guess[n] = tentative
                score[n] = tentative + minPath(n, end)
                if n not in open:
                    open.append(n)
    return -1
