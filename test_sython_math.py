from sython_extended import SythonExtended
import unittest
import math

class TestSythonMathMixin(unittest.TestCase):
    def setUp(self):
        """Initial setup for tests - creates an Sython environment and adds math functions."""
        
        self.interpreter = SythonExtended()  # Assuming you have an interpreter class

    def evaluate(self, expr):
        """Helper method to evaluate an expression in the Sython environment."""
        return self.interpreter.run(expr)

    def test_pi(self):
        """Test that pi is correctly available."""
        self.assertAlmostEqual(self.evaluate('pi'), math.pi, places=9)

    def test_e(self):
        """Test that e is correctly available."""
        self.assertAlmostEqual(self.evaluate('e'), math.e, places=9)

    def test_sin(self):
        """Test the sine function."""
        self.assertAlmostEqual(self.evaluate('(sin (/ pi 2))'), 1, places=9)

    def test_cos(self):
        """Test the cosine function."""
        self.assertAlmostEqual(self.evaluate('(cos pi)'), -1, places=9)

    def test_sqrt(self):
        """Test the square root function."""
        self.assertAlmostEqual(self.evaluate('(sqrt 4)'), 2, places=9)

    def test_log(self):
        """Test the logarithmic function."""
        self.assertAlmostEqual(self.evaluate('(log e)'), 1, places=9)  # Natural log
        self.assertAlmostEqual(self.evaluate('(log 100 10)'), 2, places=9)  # Log base 10

    def test_pow(self):
        """Test the power function."""
        self.assertAlmostEqual(self.evaluate('(pow 2 3)'), 8, places=9)
        self.assertAlmostEqual(self.evaluate('(pow 5 0)'), 1, places=9)

    def test_tan(self):
        """Test the tangent function."""
        self.assertAlmostEqual(self.evaluate('(tan (/ pi 4))'), 1, places=9)

    def test_abs(self):
        """Test the absolute value function."""
        self.assertEqual(self.evaluate('(abs -5)'), 5)

    def test_round(self):
        """Test the rounding function."""
        self.assertEqual(self.evaluate('(round 3.5)'), 4)
        self.assertEqual(self.evaluate('(round 3.49)'), 3)

    def test_floor(self):
        """Test the floor function."""
        self.assertEqual(self.evaluate('(floor 3.7)'), 3)
        self.assertEqual(self.evaluate('(floor 5.1)'), 5)

    def test_ceil(self):
        """Test the ceiling function."""
        self.assertEqual(self.evaluate('(ceil 3.1)'), 4)
        self.assertEqual(self.evaluate('(ceil 5.9)'), 6)

if __name__ == '__main__':
    unittest.main(verbosity=2)
