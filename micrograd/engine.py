
class Value:
    def __init__(self, data, _children=(), _op=''):
        self.data = float(data)
        self._prev = set(_children)
        self._op = _op

    def __repr__(self):
        out = f"Value => data = {self.data}"
        return out
    # __repr__ is a dunder method which provides a readable string reprsention.

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

   # Addition and multiplication are commutative, so we can alias __radd__ = __add__ and __rmul__ = __mul__.
    # Subtraction and division are not commutative, so __rsub__ and __rtruediv__ need their own implementations.

    def __neg__(self):
        out = Value(-self.data, (self,), 'neg')
        return out

    def __sub__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data - other.data, (self, other), '-')
        return out

    def __rsub__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(other.data - self.data, (other, self), '-')
        return out

    def __truediv__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data / other.data, (self, other), '/')
        return out

    def __rtruediv__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(other.data / self.data, (other, self), '/')
        return out

    def __pow__(self, other):
        if isinstance(other, Value):
            out = Value(self.data ** other.data, (self, other), '**')
        else:
            out = Value(self.data ** float(other),
                        (self,), f'**{float(other)}')
        return out
