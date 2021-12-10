def parse(lines):
    return [v.strip() for v in lines]

def solve(data):
    open = ['(', '[', '{', '<']
    close = [')', ']', '}', '>']
    scores = []
    for line in data:
        stack = []
        score = 0
        error = False
        for s in line:
            if s in open:
                stack.append(s)
            elif s in close:
                expected = open.index(stack.pop())
                if expected != close.index(s):
                    error = True
                    break
        if (not error):
            for c in stack[::-1]:
                score *= 5
                score += open.index(c) + 1
            scores.append(score)
    scores = sorted(scores)
    result = scores[len(scores) // 2]
    print(scores)
    print(result)
    return result
