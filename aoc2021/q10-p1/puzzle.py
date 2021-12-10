def parse(lines):
    return [v.strip() for v in lines]

def solve(data):
    open = ['(', '[', '{', '<']
    close = [')', ']', '}', '>']
    score = 0
    scores = [3, 57, 1197, 25137]
    for line in data:
        stack = []
        for s in line:
            if s in open:
                stack.append(s)
            elif s in close:
                expected = open.index(stack.pop())
                if expected != close.index(s):
                    print("{} - Expected {}, but found {} instead".format(line, close[expected], s))
                    score += scores[close.index(s)]
    print(score)                
    return score
