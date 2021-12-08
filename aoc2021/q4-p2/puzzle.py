def parse(lines):
    data = {
        "draw": [int(v) for v in lines[0].split(',')]
    }
    rows = [o.strip().replace('  ',' ').split(' ') for o in lines[1:] if o.strip() != '']
    cols = []
    for r in range(0, len(rows), 5):
        cols.append([rows[r][0], rows[r+1][0], rows[r+2][0], rows[r+3][0], rows[r+4][0]])
        cols.append([rows[r][1], rows[r+1][1], rows[r+2][1], rows[r+3][1], rows[r+4][1]])
        cols.append([rows[r][2], rows[r+1][2], rows[r+2][2], rows[r+3][2], rows[r+4][2]])
        cols.append([rows[r][3], rows[r+1][3], rows[r+2][3], rows[r+3][3], rows[r+4][3]])
        cols.append([rows[r][4], rows[r+1][4], rows[r+2][4], rows[r+3][4], rows[r+4][4]])
    data["lines"] = rows + cols
    data["boards"] = len(rows) // 5
    return data

def score(board, lines):
    result = 0
    for i in range((board - 1) * 5, board * 5):
        print(lines[i])
        result += sum([int(d) for d in lines[i] if int(d) > 0])
    return result

def solve(data):
    #print(data)
    wins = {}
    winners = {}
    for pick in data["draw"]:
        ind = -1
        for row in data["lines"]:
            ind += 1
            for col in range(0, 5):
                if pick == int(data["lines"][ind][col]):
                    try:
                        data["lines"][ind][col] = "-1"
                        wins[ind] += 1
                    except KeyError:
                        wins[ind] = 1
                    if wins[ind] == 5:
                        #print ("Winning line!", ind)
                        b = ((ind % (data["boards"] * 5)) // 5) + 1
                        winners[b] = pick
                        if (len(winners) == data["boards"]):
                            print("final board won!")
                            b = list(winners)[-1]
                            print ("in board", b)
                            s = score(b, data["lines"])
                            print ("board score =", s, " x ", winners[b], " = ", s * winners[b])
                            return s * winners[b]
    print("No win!")
    return 0
