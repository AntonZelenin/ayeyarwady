# Types
INTEGER = 'INTEGER'
FLOAT = 'FLOAT'

# Keywords
PRINT = 'PRINT'

# Parenthesis
OPEN_PAREN = 'OPEN_PAREN'
CLOSE_PAREN = 'CLOSE_PAREN'
OPEN_CURLY_BRACKET = 'OPEN_CURLY_BRACKET'
CLOSE_CURLY_BRACKET = 'CLOSE_CURLY_BRACKET'

# Arithmetic operators
SUM = 'SUM'
SUB = 'SUB'
MUL = 'MUL'
DIV = 'DIV'

ALL_TOKENS = [v for v in locals() if not v.startswith('_')]
