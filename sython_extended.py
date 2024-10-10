from sython_interpreter import SythonInterpreter
from sython_math import SythonMathMixin

# Create a composite interpreter that includes the mixin
class SythonExtended(SythonInterpreter, SythonMathMixin):
    def __init__(self):
        super().__init__()
        self.add_math_library(self.env)