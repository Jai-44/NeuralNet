
class Value:

    def __init__(self, data):
        self.data = float(data)

    def __repr__(self):
        return f"Value => data = {self.data}"

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data + other.data)
    __radd__ = __add__

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data * other.data)
    __rmul__ = __mul__

    def __neg__(self):
        return Value(-self.data)

    def __sub__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data - other.data)

    def __rsub__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(other.data - self.data)

    def __truediv__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data / other.data)

    def __rtruediv__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(other.data / self.data)

    def __pow__(self, other):
        if isinstance(other, Value):
            return Value(self.data ** other.data)
        return Value(self.data ** float(other))


a = Value(2)
b = Value(3)
c = a + b
d = Value(-7)
e = c - d

print(e)
