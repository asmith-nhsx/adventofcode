def parse(lines):
    return [s.strip() for s in lines]

def bin2dec(bin):
    bit = 0
    result = 0
    while bit < len(bin):
        result += (2 ** (len(bin) - bit - 1)) * int(bin[bit])
        bit += 1
    return result

def search(isox, data):
    length = len(data[0])
    n = len(data)
    bit = 0
    sigbit = lambda i, d : sum([int(s[i]) for s in d]) >=  len(d) / 2

    while bit < length:
        sig = sigbit(bit, data) == isox
        #print(isox, sigbit(bit, data), len(data) / 2, sig)
        data = [s for s in data if int(s[bit]) == sig]
        bit += 1
        if (len(data) == 1):
            result = bin2dec(data[0])
            #print ('Found', result, data[0])
            return result

    print ('Failed')
    return 0

def solve(data):
    oxy = search(1, data)
    print(len(data))
    scrub = search(0, data)

    print (oxy, scrub, oxy * scrub, len(data))
    return oxy * scrub
