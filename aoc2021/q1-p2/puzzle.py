
def parse(lines):
    return [int(d) for d in lines]

def solve(data):
    return 0

def sumChunk(data, start, size):
    sum = 0
    for v in data[start:start+size:]:
        sum += v
    return sum
