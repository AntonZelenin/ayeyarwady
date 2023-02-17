NUMBER = 'NUMBER'
PRINT = 'PRINT'
OPEN_PAREN = 'OPEN_PAREN'
CLOSE_PAREN = 'CLOSE_PAREN'
SUM = 'SUM'
SUB = 'SUB'

ALL_TOKENS = [v for v in locals() if not v.startswith('_')]
