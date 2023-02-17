import aye.types
from llvmlite import ir


class Number:
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value

    def eval(self):
        return ir.Constant(aye.types.INT, int(self.value))


class BinaryOp:
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right


class Sum(BinaryOp):
    def eval(self):
        return self.builder.add(self.left.eval(), self.right.eval())


class Sub(BinaryOp):
    def eval(self):
        return self.builder.sub(self.left.eval(), self.right.eval())


class Print:
    def __init__(self, builder, module, printf, value):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.value = value

    def eval(self):
        value = self.value.eval()

        # Declare argument list
        voidptr_ty = aye.types.INT.as_pointer()
        fmt = "%i \n\0"
        c_fmt = ir.Constant(
            ir.ArrayType(ir.IntType(8), len(fmt)),
            bytearray(fmt.encode("utf8"))
        )
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="fstr")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)

        self.builder.call(self.printf, [fmt_arg, value])
