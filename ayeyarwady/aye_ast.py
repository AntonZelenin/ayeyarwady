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


class Double(Type):
    def eval(self):
        return ir.Constant(aye_types.DOUBLE, float(self.value))


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
        if isinstance(left.type, Integer) and isinstance(right.type, Integer):
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
    _functions_cache = {}

    def __init__(self, builder, module, value):
        self.builder = builder
        self.module = module
        self.value = value

    def eval(self):
        value = self.value.eval()

        # Declare argument list
        fmt = f'{_get_c_format(value.type)} \n\0'
        c_fmt = ir.Constant(
            ir.ArrayType(aye_types.INT8, len(fmt)),
            bytearray(fmt.encode('utf8'))
        )
        global_fmt = ir.GlobalVariable(self.module, c_fmt.type, name='fstr')
        global_fmt.linkage = 'internal'
        global_fmt.global_constant = True
        global_fmt.initializer = c_fmt
        fmt_arg = self.builder.bitcast(global_fmt, value.type.as_pointer())

        self.builder.call(self.get_print_function(value.type), [fmt_arg, value])

    def get_print_function(self, type_):
        NAME = "printf"
        if NAME not in self._functions_cache:
            self._functions_cache[NAME] = {}
        if type_ not in self._functions_cache[NAME]:
            self._declare_print_function(NAME, type_)
        return self._functions_cache[NAME][type_]

    def _declare_print_function(self, name, type_):
        voidptr_ty = type_.as_pointer()
        printf_ty = ir.FunctionType(aye_types.DOUBLE, [voidptr_ty], var_arg=True)
        printf = ir.Function(self.module, printf_ty, name=name)
        self._functions_cache[name][type_] = printf


def _get_c_format(type_):
    if isinstance(type_, ir.IntType):
        return '%i'
    elif isinstance(type_, ir.DoubleType):
        return '%f'
    raise ValueError(f'Unsupported type: {type}')
