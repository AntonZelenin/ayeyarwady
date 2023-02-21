import ayeyarwady.types as aye_types

from abc import abstractmethod, ABC
from llvmlite import ir


class Program:
    def __init__(self, statements: list):
        self.statements = statements

    def eval(self):
        for statement in self.statements:
            statement.eval()


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


class Double(Type):
    def eval(self):
        return ir.Constant(aye_types.DOUBLE, float(self.value))


class String(Type):
    def eval(self):
        return ir.Constant(aye_types.STRING(len(self.value)), str(self.value))


class BinaryOp:
    def __init__(self, builder, module, left, right):
        self.builder = builder
        self.module = module
        self.left = left
        self.right = right


class Sum(BinaryOp):
    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if isinstance(left.type, ir.IntType) and isinstance(right.type, ir.IntType):
            return self.builder.add(left, right)
        elif isinstance(left.type, ir.DoubleType) and isinstance(right.type, ir.DoubleType):
            return self.builder.fadd(left, right)
        raise ValueError(f'Sum unsupported operator types: {type(self.left)} {type(self.right)}')


class Sub(BinaryOp):
    def eval(self):
        left = self.left.eval()
        right = self.right.eval()
        if isinstance(left.type, ir.IntType) and isinstance(right.type, ir.IntType):
            return self.builder.sub(left, right)
        elif isinstance(left.type, ir.DoubleType) and isinstance(right.type, ir.DoubleType):
            return self.builder.fsub(left, right)
        raise ValueError(f'Subtraction unsupported operator types: {type(self.left)} {type(self.right)}')


class Mul(BinaryOp):
    def eval(self):
        return self.builder.mul(self.left.eval(), self.right.eval())


class Div(BinaryOp):
    def eval(self):
        return self.builder.div(self.left.eval(), self.right.eval())


class Print:
    _global_fmt_cache = {}

    def __init__(self, builder, module, value, printf):
        self.builder = builder
        self.module = module
        self.value = value
        self.printf = printf

    def eval(self):
        value = self.value.eval()
        fmt_arg = self.builder.bitcast(
            self._get_global_fmt(value.type),
            value.type.as_pointer(),
        )
        self.builder.call(self.printf, [fmt_arg, value])

    def _get_global_fmt(self, type_):
        if type_ not in self._global_fmt_cache:
            self._declare_global_fmt(type_)
        return self._global_fmt_cache[type_]

    def _declare_global_fmt(self, type_):
        fmt = f'{_get_c_format(type_)} \n\0'
        c_fmt = ir.Constant(
            ir.ArrayType(aye_types.INT8, len(fmt)),
            bytearray(fmt.encode('utf8'))
        )
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name=f'fstr_{type_}')
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt

        self._global_fmt_cache[type_] = global_fmt


def _get_c_format(type_):
    if isinstance(type_, ir.IntType):
        return '%i'
    elif isinstance(type_, ir.DoubleType):
        return '%lf'
    raise ValueError(f'Unsupported type: {type}')
