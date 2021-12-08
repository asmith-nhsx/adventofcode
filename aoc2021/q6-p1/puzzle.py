def parse(lines):
    return [int(v) for v in lines[0].strip().split(',')]

def tick(data):
    result = []
    for i in range(0, len(data)):
        data[i] -= 1
        if (data[i] == -1):
            result.append(8)
            data[i]=6
    return data + result

def solve(data):
    #print(data)
    for day in range(0, 18):
        data = tick(data)
    print(data)
    print(len(data))
    return len(data)
