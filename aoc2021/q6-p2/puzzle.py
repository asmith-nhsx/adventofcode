def parse(lines):
    data = [int(v) for v in lines[0].strip().split(',')]
    result = []
    for i in range(0,9):
        result.append(len([v for v in data if v == i]))
    return result

def tick(data):
    newfish = data[0]
    sixers = newfish
    for i in range(1,9):
        if (i == 8):
            data[7] = data[8]
            data[8] = newfish
        else:
            data[i-1] = data[i]
    data[6] += sixers
    print(data)
    return data

def solve(data):
    print(data)
    for day in range(0, 256):
        data = tick(data)
    print(data)
    print(sum(data))
    return sum(data)
