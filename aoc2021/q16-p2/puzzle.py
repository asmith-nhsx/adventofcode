def parse(lines):
    return [o.strip() for o in lines]

def hex2Bin(input):
    map = {
        '0' : '0000',
        '1' : '0001',
        '2' : '0010',
        '3' : '0011',
        '4' : '0100',
        '5' : '0101',
        '6' : '0110',
        '7' : '0111',
        '8' : '1000',
        '9' : '1001',
        'A' : '1010',
        'B' : '1011',
        'C' : '1100',
        'D' : '1101',
        'E' : '1110',
        'F' : '1111'
    }
    word = ''
    for h in input:
        word += map[h]
    return word

def bin2Dec(input):
    result = 0
    for p in range(0,len(input)):
        result += int(input[p]) * (2 ** (len(input) - p - 1))
    return result

def readLiteral(input, pos):
    i = 6
    litbin = ''
    while (True):
        litbin += input[i+1:i+5]
        i += 5
        if (input[i - 5] == '0'):
            break
    literal = bin2Dec(litbin)
    if (pos == 0):
        while (i % 4 != 0):
            i += 1
        next = i - 1
    else:
        next = i
    return (literal, next)

def readFixedLen(input):
    pkts = []
    total_len = bin2Dec(input[7:22])
    next = 22
    while (next - 22 < total_len - 1):
        pkt = readPacket(input, next)
        next += pkt[1]
        pkts.append(pkt)
    return pkts, next

def readSubpackets(input):
    pkts = []
    total_pkt = bin2Dec(input[7:18])
    next = 18
    for n in range(0,total_pkt):
        pkt = readPacket(input, next)
        next += pkt[1]
        pkts.append(pkt)
    return pkts, next

def readPacket(chunk, pos):
    input = chunk[pos:]
    version = bin2Dec(input[0:3])
    type = bin2Dec(input[3:6])
    next = -1
    if (type == 4):
        return readLiteral(input, pos)
    else:
        subPkts = []
        len_id = input[6:7]
        if (len_id == '0'):
            subPkts, next = readFixedLen(input)
        else:
            subPkts, next = readSubpackets(input)

        values = [v[0] for v in subPkts]
        if (type == 0):
            value = sum(values)
        elif (type == 1):
            value = 1
            for i in values:
                value *= i
        elif (type == 2):
            value = min(values)
        elif (type == 3):
            value = max(values)
        elif (type == 5):
            value = 1 if values[0] > values[1] else 0
        elif (type == 6):
            value = 1 if values[0] < values[1] else 0
        elif (type == 7):
            value = 1 if values[0] == values[1] else 0
        else:
            raise ValueError("type not known")
    return (value, next)

def solve(data):
    result = []
    for hex in data:
        word = hex2Bin(hex)
        result.append(readPacket(word, 0)[0])
    return result
