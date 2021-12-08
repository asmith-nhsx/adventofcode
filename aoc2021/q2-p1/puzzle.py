def parse(lines):
    return [(s.split(' ')[0], int(s.split(' ')[1])) for s in lines]

def solve(data):
    x, y = 0, 0
    fwd = lambda a, x, y : (x + a, y)
    down = lambda a, x, y : (x, y + a)
    up = lambda a, x, y : (x, y - a)
    cmds = {
      'forward': fwd,
      'down': down,
      'up': up
    }
    for cmd, mv in data:
        x, y = cmds[cmd](mv, x, y)
    print (x, y, x * y)
    return x * y
