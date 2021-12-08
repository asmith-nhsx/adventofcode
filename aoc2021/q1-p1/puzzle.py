def parse(lines):
    return [int(d) for d in lines]  

def solve(data):
    prev = -1
    increases = 0
    for depth in data:
        if (prev > -1 and depth > prev):
            increases += 1
        prev = depth
    return increases
