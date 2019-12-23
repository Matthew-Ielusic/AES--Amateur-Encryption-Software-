from Galois import Polynomial

x = Polynomial([1,1,1,0,1,0,1,0])
y = Polynomial([1,1,0,0,0,0,0,1])
print("x:", x, sep=' ')
print("y:", y, sep=' ')
print("x+y:", x+y, sep=' ')
print("(Expected value: x^7 + x^6 + x^4 + x^2)")
print("x*y:", x*y, sep=' ')
print("(Expected value: x^7 + x^6 + 1)")