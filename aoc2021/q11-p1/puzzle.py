def parse(lines):
    return [[int(o) for o in list(v.strip())] for v in lines]

def addPower(row, col, lines, flashes):
    if (row > -1 and col > -1 and row < len(lines) and col < len(lines[0])):
        lines[row][col] += 1
        if (lines[row][col] == 10):
            flash(row, col, lines, flashes)

def flash(row, col, lines, flashes):
    if ((row, col) not in flashes or not flashes[(row,col)]):
        flashes[(row,col)] = True
        for r in range(row-1,row+2):
            for c in range(col-1,col+2):
                if (not (r == row and c == col)):
                    addPower(r, c, lines, flashes)

def power(data):
    for row in range(0, len(data)):
        for col in range(0, len(data[row])):
            data[row][col] += 1

def checkFlash(data, flashes):
    for row in range(0, len(data)):
        for col in range(0, len(data[row])):
            if (data[row][col] > 9):
                flash(row, col, data, flashes)

def unflash(data, flashes):
    for row in range(0, len(data)):
        for col in range(0, len(data[row])):
            if (data[row][col] > 9):
                data[row][col] = 0
    return len(flashes)

def printGrid(step, lines):
    print("Step ", step)
    for line in lines:
        print(line)
    print("-------------------------------")

def solve(data):
    result = 0
    for step in range(0,100):
        flashes = {}
        power(data)
        checkFlash(data, flashes)
        result += unflash(data, flashes)
    printGrid(step, data)
    print(result)
    return result
