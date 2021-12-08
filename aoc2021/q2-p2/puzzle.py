def parse(lines):
    return [(s.split(' ')[0], int(s.split(' ')[1])) for s in lines]

def solve(data):
    x, y, z = 0, 0, 0
    fwd = lambda a, x, y, z : (x + a, y + (z * a), z)
    down = lambda a, x, y, z : (x, y, z + a)
    up = lambda a, x, y, z : (x, y, z - a)
    cmds = {
      'forward': fwd,
      'down': down,
      'up': up
    }
    for cmd, mv in data:
        x, y, z = cmds[cmd](mv, x, y, z)
    print (x, y, z, x * y)
    return x * y
