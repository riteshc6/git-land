import os

A = os.path.join(os.path.realpath(__file__), '..')

B = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

C = os.path.basename(__file__)

d = os.listdir(path='.')

print(A)
print(B)
print(C)
print(d)
