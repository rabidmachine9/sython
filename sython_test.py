import unittest
from sython_interpreter import SythonInterpreter

class TestSchemeInterpreter(unittest.TestCase):
    def setUp(self):
        self.sy = SythonInterpreter()


    def test_tokenize(self):
        self.assertEqual(self.sy.tokenize("(+ 1 2)"), ['(', '+', '1', '2', ')'])
        self.assertEqual(self.sy.tokenize("(define (square x) (* x x))"), ['(', 'define', '(', 'square', 'x', ')', '(', '*', 'x', 'x', ')', ')'])

    def test_parse(self):
        self.assertEqual(self.sy.parse(['(', '+', '1', '2', ')']), ['+', 1, 2])
        self.assertEqual(self.sy.parse(['(', 'define', '(', 'square', 'x', ')', '(', '*', 'x', 'x', ')', ')']), ['define', ['square', 'x'], ['*', 'x', 'x']])

    def test_atom(self):
        self.assertEqual(self.sy.atom("42"), 42)
        self.assertEqual(self.sy.atom("3.14"), 3.14)
        self.assertEqual(self.sy.atom("x"), "x")

    def test_extend_env(self):
        base_env = {'x': 10}
        self.sy.env.update(base_env)  # Set up the base environment

        # Call extend_env and pass the keys and values to extend the environment
        new_env = self.sy.extend_env(['y'], [5])

        # Check if the new environment has the extended variables
        self.assertEqual(new_env['y'], 5)

        # Check that the original environment is intact
        self.assertEqual(self.sy.env['x'], 10)
        self.assertNotIn('y', self.sy.env)  # 'y' should only be in the extended env, not the base env


    def test_evaluate(self):
        self.sy.env.update({'+': (lambda x, y: x + y), '-': (lambda x, y: x - y)})
        self.assertEqual(self.sy.evaluate(['+', 1, 2]), 3)
        self.assertEqual(self.sy.evaluate(['-', 5, 3]), 2)

        self.sy.env['x'] = 10
        self.assertEqual(self.sy.evaluate('x'), 10)

        self.sy.env['square'] = lambda x: x * x
        self.assertEqual(self.sy.evaluate(['square', 4]), 16)

    def test_basic_arithmetic(self):
        self.assertEqual(self.sy.run("(+ 1 2)"), 3)

    def test_boolean_operations(self):
        self.assertEqual(self.sy.run("(and #t #f)"), False)

    def test_conditionals(self):
        self.assertEqual(self.sy.run("(if #t 1 0)"), 1)
        self.assertEqual(self.sy.run("(if #f 1 0)"), 0)

    def test_function_definition_and_calling(self):
        self.sy.run("(define (square x) (* x x))")
        self.assertEqual(self.sy.run("(square 4)"), 16)

    def test_higher_order_functions(self):
        self.sy.run("(define (apply proc arg) (proc arg))")
        self.sy.run("(define (add1 x) (+ x 1))")
        self.assertEqual(self.sy.run("(apply add1 5)"), 6)

    def test_list_operations(self):
        self.assertEqual(self.sy.run("(car (cons 1 2))"), 1)
        self.assertEqual(self.sy.run("(cdr (cons 1 2))"), [2])

    def test_recursion(self):
        self.sy.run("(define (factorial n) (if (= n 0) 1 (* n (factorial (- n 1)))))")
        self.assertEqual(self.sy.run("(factorial 5)"), 120)

    def test_variable_definition(self):
        self.sy.run("(define x 10)")
        self.assertEqual(self.sy.run("x"), 10)

if __name__ == '__main__':
    unittest.main(verbosity=2)
