import unittest
import puzzle

class TestBasic(unittest.TestCase):
    def test_example_pass(self):
        with open('test.txt') as file:
            data = puzzle.parse(file.readlines())
            answer = puzzle.solve(data)
            self.assertEqual(10, answer)

    def test_example_pass1(self):
        with open('test1.txt') as file:
            data = puzzle.parse(file.readlines())
            answer = puzzle.solve(data)
            self.assertEqual(19, answer)

    def test_example_pass2(self):
        with open('test2.txt') as file:
            data = puzzle.parse(file.readlines())
            answer = puzzle.solve(data)
            self.assertEqual(226, answer)

    def test_real_pass(self):
        with open('input.txt') as file:
            data = puzzle.parse(file.readlines())
            answer = puzzle.solve(data)
            self.assertEqual(3369, answer)
if __name__ == '__main__':
    unittest.main()
