def parse(lines):
    return [(v.strip().split('|')[0], v.strip().split('|')[1]) for v in lines]

def solve(data):
    uniq = [2,3,4,7]
    count = len([s for l in data for s in l[1].split(' ') if len(s) in uniq])
    codes = set([s for l in data for s in l[1].split(' ') if len(s) in uniq])
    print(codes)
    print(count)
    return count
