def parse(lines):
    xys = [int(xy) for v in lines for coord in v.strip().split('->') for xy in coord.strip().split(',')]
    sxs = xys[::4]
    sys = xys[1::4]
    exs = xys[2::4]
    eys = xys[3::4]
    return [s for s in list(zip(zip(sxs,sys),zip(exs,eys))) if s[0][0] == s[1][0] or s[0][1] == s[1][1]]
    #return {
    #    "start": list(zip(sxs,sys)),
    #    "end": list(zip(exs,eys))
    #}

def hit(line, grid):
    x1,y1,x2,y2 = line[0][0],line[0][1],line[1][0], line[1][1]
    if (x1 == x2):
        for y in range(min(y1,y2), max(y1,y2)+1):
            grid[y][x1] += 1
    else:
        for x in range(min(x1,x2), max(x1,x2)+1):
            grid[y1][x] += 1
    #for g in grid:
    #    print(g)
    return grid

def solve(data):
    #print(data)
    mx = max([s[0][0] for s in data] + [s[1][0] for s in data])
    my = max([s[0][1] for s in data] + [s[1][1] for s in data])
    grid = [[0 for i in range(mx+1)] for j in range(my+1)]
    for line in data:
        print(line)
        grid = hit(line, grid)
    for g in grid:
        print(g)
    count = len([val for sublist in grid for val in sublist if val >= 2])
    print(count)
    return count
