import math


class Value:
    def __init__(self, data, _inputs=(), _op=''):
        self.data = float(data)
        self.grad = 0.0
        self._backward = lambda: None
        self._inputs = set(_inputs)
        self._op = _op

    def __repr__(self):
        out = f"Value => data = {self.data}"
        return out
    # __repr__ provides a readable string representation.

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')

        def _backward():
            # local grads for addition: d(out)/d(self)=1, d(out)/d(other)=1
            self.grad += 1.0 * out.grad
            other.grad += 1.0 * out.grad
        out._backward = _backward
        return out
    __radd__ = __add__

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')

        def _backward():
            # product rule: d(out)/d(self)=other.data, d(out)/d(other)=self.data
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out
    __rmul__ = __mul__

    def __pow__(self, other):
        # other is an int/float (scalar exponent)
        exp = float(other)
        out = Value(self.data ** exp, (self,), f'**{exp}')

        def _backward():
            # d/dself (self**exp) = exp * self**(exp-1)
            self.grad += (exp * (self.data ** (exp - 1.0))) * out.grad
        out._backward = _backward
        return out

    def relu(self):
        out = Value(0 if self.data < 0 else self.data)

        def _backward(self):
            self.grad += (out.data > 0) * out.grad
        out._backward = _backward
        return out

    def tanh(self):
        out = Value(math.tanh(self.data))

        def _backward(self):
            self.grad += (1 - out.data * out.data) * out.grad
        out._backward = _backward
        return out

    # Addition and multiplication are commutative, so we can alias __radd__ = __add__ and __rmul__ = __mul__.
    # Subtraction and division are not commutative, so __rsub__ and __rtruediv__ need their own implementations.

    def __neg__(self):
        # unary minus via multiply by -1; preserves graph through __mul__
        return self * -1

    def __sub__(self, other):
        # a - b == a + (-b)
        other = other if isinstance(other, Value) else Value(other)
        return self + (-other)

    def __rsub__(self, other):
        # b - a == b + (-a)
        other = other if isinstance(other, Value) else Value(other)
        return other + (-self)

    def __truediv__(self, other):
        # a / b == a * (b ** -1)
        other = other if isinstance(other, Value) else Value(other)
        return self * (other ** -1)

    def __rtruediv__(self, other):
        # b / a == b * (a ** -1)
        other = other if isinstance(other, Value) else Value(other)
        return other * (self ** -1)

    def backward(self):
        # It gives topological order of a graph
        topo = []
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._inputs:
                    build_topo(child)
                topo.append(v)

        build_topo(self)
        self.grad = 1.0

        for node in reversed(topo):
            node._backward()
