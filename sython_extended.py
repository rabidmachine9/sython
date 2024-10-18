from sython_interpreter import SythonInterpreter
from sython_math import SythonMathMixin
from sython_midi import SythonMidiMixin

# Create a composite interpreter that includes the mixin
class SythonExtended(SythonInterpreter, SythonMathMixin, SythonMidiMixin):
    def __init__(self):
        super().__init__()

        # Explicitly initialize the mixin if it has an __init__ method
        SythonMidiMixin.__init__(self)

        self.add_math_library(self.env)
        self.add_midi_library(self.env) 