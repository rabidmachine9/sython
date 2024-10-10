import math


class SythonMathMixin:
    def add_math_library(self, env):
            env['pi'] = math.pi
            env['e'] = math.e

            # Add basic functions
            env['sin'] = lambda x: math.sin(x)
            env['cos'] = lambda x: math.cos(x)
            env['sqrt'] = lambda x: math.sqrt(x)
            env['log'] = lambda x, base=math.e: math.log(x, base)  # Default to natural log
            env['pow'] = lambda x, y: math.pow(x, y)

            # Add more as needed, e.g. factorial, tan, etc.
            env['tan'] = lambda x: math.tan(x)
            env['abs'] = lambda x: abs(x)
            env['round'] = lambda x: round(x)
            env['floor'] = lambda x: math.floor(x)
            env['ceil'] = lambda x: math.ceil(x)