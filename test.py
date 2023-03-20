import unittest
from main import csp_coloring

class TestCase(unittest.TestCase):
    def runTest1(self):
        
        a = csp_coloring({1: [3], 3: [1, 19], 2: [18, 19], 18: [2], 19: [3, 2]}, 3)
        self.assertEqual(a, {1: 0, 18: 0, 19: 0, 2: 1, 3: 1}, "{1: 0, 18: 0, 19: 0, 2: 1, 3: 1}")
        def TestCases():
            TestCases = unittest.TestSuite() 
            TestCases.addTest(TestCase('runTest1'))
if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(TestCases())
