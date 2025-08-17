
class Value:
    def __init__(self, data, _inputs=(), _op=''):
        self.data = float(data)
        self._inputs = set(_inputs)
        self._op = _op

    def __repr__(self):
        out = f"Value => data = {self.data}"
        return out
    # __repr__ provides a readable string representation.

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')
        return out
    __radd__ = __add__

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')
        return out
    __rmul__ = __mul__

    def __pow__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data ** other.data, (self, other), '**')
        return out

    # Subtraction and division defined via addition and multiplication:
    # a - b == a + (-b)
    # a / b == a * (b ** -1)

    def __neg__(self):
        # unary minus via multiply by -1; preserves graph through __mul__
        return self * -1

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __truediv__(self, other):
        return self * (other ** -1)

    def __rtruediv__(self, other):
        return other * (self ** -1)
