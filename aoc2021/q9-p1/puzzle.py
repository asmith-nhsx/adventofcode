def parse(lines):
    line = len(lines[0].strip()) * '9'
    lines = [line] + lines + [line]
    return [v.strip() for v in lines]
    
def rowLowest(row, line, points):
    last, cur, next = 0, 0, 0
    limit = len(line)
    line = '9'+line+'9'
    for col in range(0,limit):
        last, cur, next = int(line[col]),int(line[col+1]),int(line[col+2])
        if (last > cur and cur < next):
            #print(row, col, cur)
            points.append((row, col, cur))
    return

def solve(data):
    row = 0
    points = []
    for line in data[1:-1]:
        row += 1
        rowLowest(row, line, points)

    lows = []
    risk = 0
    for point in points:
        top = int(data[point[0]-1][point[1]])
        cur = point[2]
        bot = int(data[point[0]+1][point[1]])
        if (top > cur and cur < bot):
            lows.append((point[0], point[1], cur))
            risk += cur + 1

    print(lows)
    print(risk)
    return risk
