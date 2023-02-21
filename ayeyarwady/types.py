from llvmlite import ir

INT8 = ir.IntType(8)
INT16 = ir.IntType(16)
INT32 = ir.IntType(32)

DOUBLE = ir.DoubleType()


def STRING(length):
    return ir.ArrayType(INT8, length)
