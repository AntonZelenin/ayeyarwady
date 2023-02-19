import ayeyarwady.types as aye_types

from abc import abstractmethod, ABC
from llvmlite import ir


class Type(ABC):
    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value


class Integer(Type):
    @abstractmethod
    def eval(self):
        pass


class I32(Integer):
    def eval(self):
        return ir.Constant(aye_types.INT32, int(self.value))


class Float(Type):
    def eval(self):
        return ir.Constant(aye_types.FLOAT, float(self.value))


class BinaryOp:
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right


class Sum(BinaryOp):
    def eval(self):
        if isinstance(self.left, Integer) and isinstance(self.right, Integer):
            return self.builder.add(self.left.eval(), self.right.eval())
        elif isinstance(self.left, Float) and isinstance(self.right, Float):
            return self.builder.fadd(self.left.eval(), self.right.eval())
        raise ValueError(f'Unsupported operator types: {type(self.left)} {type(self.right)}')


class Sub(BinaryOp):
    def eval(self):
        if isinstance(self.left, Integer) and isinstance(self.right, Integer):
            return self.builder.sub(self.left.eval(), self.right.eval())
        elif isinstance(self.left, Float) and isinstance(self.right, Float):
            return self.builder.fsub(self.left.eval(), self.right.eval())
        raise ValueError(f'Unsupported operator types: {type(self.left)} {type(self.right)}')


class Mul(BinaryOp):
    def eval(self):
        return self.builder.mul(self.left.eval(), self.right.eval())


class Div(BinaryOp):
    def eval(self):
        return self.builder.div(self.left.eval(), self.right.eval())


class Print:
    def __init__(self, builder, module, printf, value):
        self.builder = builder
        self.module = module
        self.printf = printf
        self.value = value

    def eval(self):
        value = self.value.eval()

        # Declare argument list
        voidptr_ty = aye_types.FLOAT.as_pointer()
        fmt = "%f \n\0"
        c_fmt = ir.Constant(
            ir.ArrayType(aye_types.INT8, len(fmt)),
            bytearray(fmt.encode("utf8"))
        )
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name="fstr")
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = self.builder.bitcast(global_fmt, voidptr_ty)

        self.builder.call(self.printf, [fmt_arg, value])
