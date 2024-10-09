class Symbol(str):
    """A symbol is a unique string that is used as an identifier."""
    def __repr__(self):
        return f"'{self}'"  # Return the symbol in quoted form for clarity