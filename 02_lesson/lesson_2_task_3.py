import math

def square(side):
    area = side * side
    if not isinstance(side, int):
        area = math.ceil(area)
    return area

print(square(5))     
print(square(3.2))   
print(square(4.7))   
print(square(2))     
print(square(6.1))