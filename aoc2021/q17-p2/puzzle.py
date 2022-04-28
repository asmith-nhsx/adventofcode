def parse(lines):
    matrix = [o[13:].strip().split(',') for o in lines]
    target = [val.lstrip(' xy=').split('..') for sublist in matrix for val in sublist]
    return [int(val) for sublist in target for val in sublist]

def inTarget(pos, target):
    return target[0] <= pos[0] <= target[1] and target[2] <= pos[1] <= target[3]

def outOfRange(pos, target):
    return pos[1] < target[2]

def nextStep(pos, vel, top):
    newpos = (pos[0] + vel[0], pos[1] + vel[1])
    vel[0] += 1 if vel[0] < 0 else -1 if vel[0] > 0 else 0
    vel[1] -= 1
    top = newpos[1] if newpos[1] > top else top
    return newpos, vel, top

def fire(vel, data):
    pos = (0, 0)
    top = 0
    vel = list(vel)
    while (not outOfRange(pos, data)):
        pos, vel, top = nextStep(pos, vel, top)
        if (inTarget(pos, data)):
            return True
    return False

def solve(data):
    hits = []
    for x in range(0, data[1]+1):
        for y in range(data[2], -data[2]+1):
            vel = (x, y)
            if (fire(vel, data)):
                if (vel not in hits):
                    hits.append(vel)
    #print (hits)
    return len(hits)
