def parse(lines):
    return [s.strip() for s in lines]

def solve(data):
    length = len(data[0])
    n = len(data)
    print(n)
    bit = 0
    sigbit = lambda i : sum([int(s[i]) for s in data]) > n / 2

    gamma = 0
    epsilon = 0
    while bit < length:
        sig = sigbit(bit)
        print(sum([int(s[bit]) for s in data]), bit, sig,  (2 ** (length - bit - 1)), (2 ** (length - bit - 1)) * sig, (2 ** (length - bit - 1)) * (not sig))
        gamma += (2 ** (length - bit - 1)) * sig
        epsilon += (2 ** (length - bit - 1)) * (not sig)
        bit += 1

    print (gamma, epsilon, gamma * epsilon)
    return gamma * epsilon
