import unittest
from sython_interpreter import SythonInterpreter
from io import StringIO
from unittest.mock import patch


class TestSythonInterpreter(unittest.TestCase):
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
        self.assertEqual(self.sy.atom("some_string"), "some_string")

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
        self.assertEqual(self.sy.run("(- 2 1)"), 1)
        self.assertEqual(self.sy.run("(/ 1 2)"), 0.5)

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

    def test_division_by_zero_error(self):
        with self.assertRaises(ZeroDivisionError) as context:
            self.sy.run("( / 1 0 )")  # Attempting to divide by zero
        self.assertIn("Division by zero is undefined", str(context.exception))

    def test_display_string(self):
        code = '(display "hello")'
        expected_output = "hello"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.sy.run(code)  # Run the code that uses the display function
            output = fake_out.getvalue().strip()  # Capture the printed output

        self.assertEqual(output, expected_output, f"Expected '{expected_output}', got '{output}'")

    def test_operator_type_error(self):
        code = '(+ 1 "two" 3)'
        try:
            self.sy.run(code)
        except TypeError as e:
            assert "Operator '+' requires all arguments to be numbers, got: [1, 'two', 3]" in str(e)
        else:
            assert False, "TypeError was not raised"

    def test_length(self):
        code_list = '(length (quote (1 2 3 4 5)))'  # Testing length of a list
        result_list = self.sy.run(code_list)
        assert result_list == 5, f"Expected 5, got {result_list}"

        code_string = '(length "hello")'  # Testing length of a string
        result_string = self.sy.run(code_string)
        assert result_string == 5, f"Expected 5, got {result_string}"

        #Optionally, test an invalid input (like a number) to ensure error handling works
        code_invalid = '(length 123)'
        try:
            self.sy.run(code_invalid)
        except TypeError as e:
            assert "Argument must be a list or string" in str(e)
        else:
            assert False, "TypeError was not raised"

    def test_lambda(self):
        self.sy.run("(define (my-lambda x) (if (> x 2) 'yes 'no))")
        self.assertEqual(self.sy.run("(my-lambda 3)"), 'yes')
        self.assertEqual(self.sy.run("(my-lambda 1)"), 'no')

    
    

if __name__ == '__main__':
    unittest.main(verbosity=2)