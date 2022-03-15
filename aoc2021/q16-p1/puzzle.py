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

def readPacket(chunk, pos, pkts, indx = 0):
    input = chunk[pos:]
    version = bin2Dec(input[0:3])
    type = bin2Dec(input[3:6])
    literal = -1
    next = -1
    len_id = -1
    total_len = -1
    total_pkt = -1
    if (type == 4):
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
    else:
        len_id = input[6:7]
        if (len_id == '0'):
            total_len = bin2Dec(input[7:22])
            next = 22
            while (next - 22 < total_len - 1):
                pkt = readPacket(input, next, pkts, indx + 1)
                next += pkt[6]
        else:
            total_pkt = bin2Dec(input[7:18])
            next = 18
            for n in range(0,total_pkt):
                pkt = readPacket(input, next, pkts, indx + 1)
                next += pkt[6]
    packet = (version, type, literal, len_id, total_len, total_pkt, next)
    pkts.append(packet)
    return packet

def printPacket(indx, input, pkt):
    if (pkt[1] == 4):
        print('  '*indx, f"version:{pkt[0]},type:Literal,value:{pkt[2]},next:{pkt[6]}")
    elif (pkt[3] == '0'):
        print('  '*indx, f"version:{pkt[0]},type:Operator,len:{pkt[4]},next:{pkt[6]}")
    else:
        print('  '*indx, f"version:{pkt[0]},type:Operator,packets:{pkt[5]},next:{pkt[6]}")

def solve(data):
    result = []
    for hex in data:
        word = hex2Bin(hex)
        pkts = []
        readPacket(word, 0, pkts)
        result.append(sum([p[0] for p in pkts]))
    return result
