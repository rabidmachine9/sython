import operator

class Symbol(str):
    """A symbol is a unique string that is used as an identifier."""
    def __repr__(self):
        return f"'{self}'"  # Return the symbol in quoted form for clarity



class SythonInterpreter:
    def __init__(self, debug=False):
        self.env = self.standard_env()
        self.debug = debug  # Add a debug flag
        self.line_number = 1  # Initialize line number

    # Tokenizer: Convert source code into a list of tokens
    def tokenize(self, source_code):
        # Reset line number for each tokenization
        self.line_number = 1
        lines = source_code.split('\n')
        tokens = []

        for line in lines:
            line = line.split(';')[0]  # Ignore comments
            line = line.replace("'", " ' ")  # Ensure quote is treated as a separate token
            tokens_line = line.replace('(', ' ( ').replace(')', ' ) ').split()
            tokens.extend(tokens_line)
            self.line_number += 1  # Increment line number for each line

        if self.debug:
            print(f"[DEBUG] Tokens: {tokens}")
        return tokens

    # Parser: Convert tokens into a nested list (abstract syntax tree)
    def parse(self, tokens):
        if len(tokens) == 0:
            raise SyntaxError("unexpected EOF while reading at line {self.line_number}")
        token = tokens.pop(0)
        if token == '(':
            L = []
            while tokens[0] != ')':
                L.append(self.parse(tokens))
            tokens.pop(0)  # pop off ')'
            if self.debug:
                print(f"[DEBUG] Parsed expression: {L}")
            return L
        elif token == ')':
            raise SyntaxError("unexpected ')' at line {self.line_number}")
        elif token == "'":  # Handle quoted expressions
            return ['quote', self.parse(tokens)]
        else:
            return self.atom(token)

    # Convert token to a number if possible, otherwise keep as a symbol
    def atom(self, token):
        try:
            return int(token)  # Check if it's an integer
        except ValueError:
            try:
                return float(token)  # Check if it's a float
            except ValueError:
                # Check if it's a string (starts and ends with quotes)
                if token.startswith('"') and token.endswith('"'):
                    return token  # Keep the quotes for now, evaluate will handle them later
                else:
                    return Symbol(token)  # Anything else is treated as a symbol


    # Standard environment with basic operations
    def standard_env(self):
        env = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            'mod': operator.mod,        # Modulo operation
            '=': operator.eq,           # Equal to
            '<': operator.lt,           # Less than
            '>': operator.gt,           # Greater than
            'and': lambda x, y: x and y,  # Logical AND
            'or': lambda x, y: x or y,    # Logical OR
            'not': operator.not_,       # Logical NOT
            'car': lambda lst: lst[0],  # First element of a list
            'cdr': lambda lst: lst[1:], # Rest of the list after the first element
            'cons': lambda x, y: [x] + (y if isinstance(y, list) else [y]),  # Create a new list with x as head and y as tail
            'length': self._length,
            '#t': True,                 # True value
            '#f': False,                # False value
            'display': self._display_fn,
        }
        return env

    def _length(self, x):
        if isinstance(x, (list, str)):
            return len(x)
        else:
            raise TypeError(f"Argument must be a list or string at line {self.line_number}")

    def _display_fn(self, *args):
        """Custom display function for the interpreter."""
        output = ' '.join(map(str, args))  # Convert all arguments to strings
        print(output, end='')  # Print without a newline
        return None  # Typically, display does not return a value

    # Create a new environment with parameters bound to argument values
    def extend_env(self, params, args):
        new_env = self.env.copy()  # Copy the current environment
        new_env.update(zip(params, args))
        return new_env

    # Evaluator: Evaluate the parsed expression in an environment
    def evaluate(self, expr, env=None, is_tail=False):
        if env is None:
            env = self.env
        while True:  # Use a loop to simulate TCO instead of recursive calls
            
            if isinstance(expr, str):  # variable reference or string
                if expr.startswith('"') and expr.endswith('"'):
                    if self.debug:
                        print(f"[DEBUG] Evaluating string literal: {expr}")
                    return expr[1:-1]  # Return the string literal without the quotes
                elif self.debug:
                    print(f"[DEBUG] Evaluating variable: {expr}")
                return env[expr]
            elif not isinstance(expr, list):  # constant literal
                if self.debug:
                    print(f"[DEBUG] Evaluating constant: {expr}")
                return expr
            op = expr[0]

            if self.debug:
                print(f"[DEBUG] Evaluating expression: {expr}")

            # Handle variable or function definitions
            if op == 'quote':
                return expr[1]
            elif op == 'define':
                if isinstance(expr[1], list):  # function definition: (define (name params) body)
                    _, (name, *params), body = expr
                    env[name] = lambda *args: self.evaluate(body, self.extend_env(params, args))
                    if self.debug:
                        print(f"[DEBUG] Defined function {name} with params {params}")
                    return None
                else:  # variable definition: (define var expr)
                    _, var, exp = expr
                    env[var] = self.evaluate(exp, env)
                    if self.debug:
                        print(f"[DEBUG] Defined variable {var} with value {env[var]}")
                    return None

            # Handle conditionals: (if condition then-expr else-expr)
            elif op == 'if':
                _, condition, then_expr, else_expr = expr
                expr = then_expr if self.evaluate(condition, env) else else_expr
                continue  # Tail call optimization: continue with new expression

            # Handle boolean operations
            elif op == 'and':
                return all(self.evaluate(arg, env) for arg in expr[1:])
            elif op == 'or':
                return any(self.evaluate(arg, env) for arg in expr[1:])
            elif op == 'not':
                return not self.evaluate(expr[1], env)

            # Handle list operations
            elif op == 'car':
                return self.evaluate(expr[1], env)[0]
            elif op == 'cdr':
                return self.evaluate(expr[1], env)[1:]
            elif op == 'cons':
                return env[op](self.evaluate(expr[1], env), self.evaluate(expr[2], env))

            elif op == 'display':
                 # Evaluate each argument and pass them to _display_fn
                args = [self.evaluate(arg, env) for arg in expr[1:]]
                self._display_fn(*args)  # Call _display_fn with evaluated arguments
                return None  # Display typically does not return a value

            # Handle arithmetic operations
            elif op in {'+', '-', '*', '/'}:
                args = [self.evaluate(arg, env) for arg in expr[1:]]
                # Check if all arguments are numbers
                if not all(isinstance(arg, (int, float)) for arg in args):
                    raise TypeError(f"Operator '{op}' requires all arguments to be numbers, got: {args} at line {self.line_number}")
                
                if op == '+':
                    return sum(args)
                elif op == '-':
                    return args[0] - sum(args[1:])
                elif op == '*':
                    result = 1
                    for num in args:
                        result *= num
                    return result
                elif op == '/':
                    if args[1] == 0:
                        raise ZeroDivisionError("Division by zero is undefined at line {self.line_number}")  # Raise an error for division by zero
                    return args[0] / args[1]

            # Function call
            proc = self.evaluate(expr[0], env)
            args = [self.evaluate(arg, env) for arg in expr[1:]]
            if is_tail:
                expr = proc(*args)
                continue  # Tail call optimization: continue with new expression
            else:
                return proc(*args)

    # Process each expression separately in the program
    def run(self, program):
        """Run the given Scheme program in the provided environment."""
        if self.debug:
            print(f"Running program: {program}")
        tokens = self.tokenize(program)
        expressions = []
        while tokens:
            expressions.append(self.parse(tokens))
        for expr in expressions:
            result = self.evaluate(expr)
            if result is not None:  # Skip None results
                print(result)
        if self.debug:
            print(f"Results: {result}")
        return result