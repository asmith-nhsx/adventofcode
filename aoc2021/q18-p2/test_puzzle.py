import unittest
import puzzle

class TestBasic(unittest.TestCase):

    def test_solve_pass(self):
        with open('test.txt') as file:
            data = puzzle.parse(file.readlines())
            answer = puzzle.solve(data)
            self.assertEqual(3993, answer)

    def test_real_pass(self):
        with open('input.txt') as file:
            data = puzzle.parse(file.readlines())
            answer = puzzle.solve(data)
            self.assertEqual(4812, answer)

if __name__ == '__main__':
    unittest.main()
