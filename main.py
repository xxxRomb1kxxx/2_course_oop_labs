import math
WIDTH = 1920
HEIGHT = 1080
class Pointer2d:
    def __init__(self,x: int,y:int):
        self.x = x
        self.y = y

    def __check_paramerts__(self) ->bool:
        return (0 <= self.x <= WIDTH) and (0 <= self.y <= HEIGHT)

    def __equal__(self,other)->bool:
         return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Pointer({self.x},{self.y})"

class Vector2d:
    def __init__(self,x: int = None,y:int = None,start:Pointer2d = None,end: Pointer2d = None):
        if start is not None and end is not None:
            self.x = end.x - start.x
            self.y = end.y - start.y
        elif x is not None and y is not None:
            self.x = x
            self.y = y
        else:
            raise ValueError("Invalid input data for Vector __init__")
    def __get_item__(self,index: int)-> int:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError(" wrong index (get_item)")
    def __set_item__(self,index:int,value:int)-> int:
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError(" wrong index (set_item)")
    def __iter__(self):
        self._index = 0;
        return self
    def __next__(self):
        if self._index < 2:
            result = self.__get_item__(self._index)
            self._index += 1
            return result
        else:
            raise StopIteration
    def __len__(self):
        return int(math.sqrt(self.x * self.x + self.y * self.y))
    def __abs__(self):
        return abs(int(math.sqrt(self.x * self.x + self.y * self.y)))
    def __equal__(self,other)->bool:
         return self.x == other.x and self.y == other.y
    def __repr__(self):
        return f"Vector({self.x},{self.y})"
    def __add__(self, other: 'Vector2d') -> 'Vector2d':
        if not isinstance(other, Vector2d):
            raise TypeError("Unsupported operand type Vector2d")
        return Vector2d(x=self.x + other.x, y=self.y + other.y)
    def __sub__(self, other: 'Vector2d') -> 'Vector2d':
        if not isinstance(other, Vector2d):
            raise TypeError("Unsupported operand type expected Vector2d")
        return Vector2d(x=self.x - other.x, y=self.y - other.y)
    def __mul__(self, scalar: int) -> 'Vector2d':
        if not isinstance(scalar, int):
            raise TypeError("Unsupported operand type expected int or float")
        return Vector2d(x=self.x * scalar, y=self.y * scalar)
    def __truediv__(self, scalar: int) -> 'Vector2d':
        if not isinstance(scalar, int):
            raise TypeError("Unsupported operand type expected int or float")
        if scalar == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        return Vector2d(x=self.x / scalar, y=self.y / scalar)

    def dot(self, other: 'Vector2d') -> int:
        return self.x * other.x + self.y * other.y

    @staticmethod
    def dot_static(v1: 'Vector2d', v2: 'Vector2d') -> int:
        return v1.x * v2.x + v1.y * v2.y
    def cross(self, other: 'Vector2d') -> int:
        return self.x * other.y - self.y * other.x

    @staticmethod
    def cross_static(v1: 'Vector2d', v2: 'Vector2d') -> int:
        return v1.x * v2.y - v1.y * v2.x

    @staticmethod
    def mixed_product(v1: 'Vector2d', v2: 'Vector2d', v3: 'Vector2d') -> int:
        cross_product = v1.x * v2.y - v1.y * v2.x
        return cross_product * v3.x + cross_product * v3.y



'''
print("/////////////_POINTER_DEBUG_//////////////////")
#Pointer debug
pointer1 = Pointer2d(10,10)
pointer2 = Pointer2d(10,10)
print(pointer1.__check_paramerts__())
print(pointer2.__check_paramerts__())
print(pointer1.__equal__(pointer2))
print(pointer1)
print(pointer2)
'''
print("/////////////_POSITIONS_//////////////////")
position_1 = Pointer2d(5,5)
position_2 = Pointer2d(15,25)
position_3 = Pointer2d(5,5)
position_4 = Pointer2d(15,25)
position_5 = Pointer2d(25,35)
position_6 = Pointer2d(45,60)
vector_1 = Vector2d(start = position_1,end = position_2)
vector_2 = Vector2d(start = position_3,end = position_4)
vector_3 = Vector2d(start = position_5,end = position_6)
'''
vector_1.__get_item__(0)
vector_1.__set_item__(0,100)
vector_1.__set_item__(1,120)
'''
print(vector_1.__repr__())
print(len(vector_1))
for value in vector_1:
    print(value)
print(vector_2.__abs__())
print(vector_2.__abs__())
print(vector_1.__equal__(vector_2))
print("///////////////////////////////")
print(vector_1.__repr__())
print(vector_2.__repr__())
print(vector_3.__repr__())
'''
print("////////////_MATH_OPERATION_///////////////////")
vector_sum = vector_1 + vector_2
print(vector_sum)
vector_diff = vector_1 - vector_2
print(vector_diff)
vector_mul = vector_1 * 2
print(vector_mul)
vector_div = vector_1 / 2
print(vector_div)
'''
print("//////////////_VECTORS_PRODUCTS_/////////////////")
dot_result = vector_1.dot(vector_2)
print(f"Скалярное произведение (метод инстанса): {dot_result}")
dot_static_result = Vector2d.dot_static(vector_1, vector_2)
print(f"Скалярное произведение (статический метод): {dot_static_result}")
cross_result = vector_1.cross(vector_2)
print(f"Векторное произведение (метод инстанса): {cross_result}")
cross_static_result = Vector2d.cross_static(vector_1, vector_2)
print(f"Векторное произведение (статический метод): {cross_static_result}")
mixed_result = Vector2d.mixed_product(vector_1, vector_2, vector_3)
print(f"Смешанное произведение: {mixed_result}")