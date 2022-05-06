import unittest
import puzzle

class TestBasic(unittest.TestCase):
    def test_sum_pass(self):
        for i in range(0,6):
            with open(f'test{i}.txt') as file:
                data = puzzle.parseNum(file.readlines())
                expected = data[0]
                answer = puzzle.sum(data[1:])
                self.assertEqual(expected, answer)

    def test_explode_pass(self):
        with open('test_5.txt') as file:
            data = puzzle.parse(file.readlines())
            for line in data:
                cols = line.strip().split(" becomes ")
                expected = puzzle.toNum(cols[1])
                answer = puzzle.toNum(cols[0])
                print(expected)
                print(answer)
                puzzle.explode(answer)
                self.assertEqual(expected, answer)

    def test_split_pass(self):
        with open('test_6.txt') as file:
            data = puzzle.parse(file.readlines())
            for line in data:
                cols = line.strip().split(" becomes ")
                expected = puzzle.toNum(cols[1])
                answer = puzzle.split(int(cols[0]))
                self.assertEqual(expected, answer)

    def test_splits_pass(self):
        with open('test_7.txt') as file:
            data = puzzle.parse(file.readlines())
            for line in data:
                cols = line.strip().split(" becomes ")
                expected = puzzle.toNum(cols[1])
                answer = puzzle.toNum(cols[0])
                puzzle.splits(answer)
                self.assertEqual(expected, answer)

    def test_magnitude_pass(self):
        with open('test_8.txt') as file:
            data = puzzle.parse(file.readlines())
            for line in data:
                cols = line.strip().split(" becomes ")
                expected = int(cols[1])
                input = puzzle.toNum(cols[0])
                answer = puzzle.magnitude(input)
                self.assertEqual(expected, answer)

    def test_solve_pass(self):
        with open('test.txt') as file:
            data = puzzle.parseNum(file.readlines())
            answer = puzzle.solve(data)
            self.assertEqual(4140, answer)

    def test_real_pass(self):
        with open('input.txt') as file:
            data = puzzle.parseNum(file.readlines())
            answer = puzzle.solve(data)
            self.assertEqual(3051, answer)

if __name__ == '__main__':
    unittest.main()
