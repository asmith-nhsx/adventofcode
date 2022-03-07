def parse(lines):
    return [v.strip() for v in lines]

def findBasin(basins, row, col, length, line):
    error = False
    if (row != 0):
        for basin in basins:
            error = False
            try:
                prevrow = basin[row-1]
            except KeyError:
                error = True
                # catch if the operation is not in the dictionary
                # this basin has no presence on the previous row!
                #print("basin {} not on row {}".format(basin["id"],row-1))

            #print("Searching for ", basin[row-1][0], col, basin[row-1][1])
            found = False
            if (not error):
                pos = col
                while (pos < length):
                    if (line[pos] == '9'):
                        break
                    if (prevrow[0] <= pos and pos <= prevrow[1]):
                        found = True
                        break
                    pos += 1

                if (found):
                    basin[row] = [col, length]
                    return basin

    return { "id": str(len(basins) + 1), row: [col, length] }

def addBasin(basins, basin):
    if (len([b for b in basins if b["id"] == basin["id"]]) == 0):
        #print("Adding basin {}".format(basin["id"]))
        basins.append(basin)

def sizeBasin(basin, data):
    size = 0
    for key in basin:
        if (key != "id"):
            print(basin["id"],key,basin[key][1],basin[key][0])
            print(data[key][basin[key][0]:basin[key][1]+1])         
            size += basin[key][1]-basin[key][0]+1
    return size

def solve(data):
    result = []
    for row in data:
        print(row)

    print("-------")

    basins = []
    row = 0
    for line in data:
        row2 = ''
        found = False
        col = 0
        for s in line:
            if s != '9':
                if not found:
                    found = True
                    basin = findBasin(basins, row, col, len(line), line)
                    #print("Returned basin ", basin["id"])
                row2 += basin["id"]
            else:
                if found:
                    found = False
                    # end col
                    basin[row][1] = col-1
                    addBasin(basins, basin)
                row2 += s
            col += 1
        if found:
            found = False
            # end col
            basin[row][1] = col
            addBasin(basins, basin)
        row += 1
        result.append(row2)
        print(row2)

    sizes = []
    for b in basins:
        sizes.append(sizeBasin(b, data))

    sizes = sorted(sizes, reverse=True)
    result = 1
    for s in sizes[:3]:
        print(s)
        result *= s

    print(result)
    return result
