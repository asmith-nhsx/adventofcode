import unittest
import puzzle

class TestBasic(unittest.TestCase):
    def test_example_pass(self):
        with open('test.txt') as file:
            data = puzzle.parse(file.readlines())
            answer = puzzle.solve(data)
            self.assertEqual(5934, answer)

    def test_real_pass(self):
        with open('input.txt') as file:
            data = puzzle.parse(file.readlines())
            answer = puzzle.solve(data)
            self.assertEqual(365862, answer)
if __name__ == '__main__':
    unittest.main()
