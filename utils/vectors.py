import math

def dot(v, w):
     """v_1 * w_1 + ... + v_n * w_n"""
     return sum(v_i * w_i
     for v_i, w_i in zip(v, w))

def sum_of_squares(v):
     """v_1 * v_1 + ... + v_n * v_n"""
     return dot(v, v)

def vector_subtract(v, w):
     """subtracts corresponding elements"""
     return [v_i - w_i
     for v_i, w_i in zip(v, w)]

def squared_distance(v, w):
     """(v_1 - w_1) ** 2 + ... + (v_n - w_n) ** 2"""
     return sum_of_squares(vector_subtract(v, w))

def distance(v, w):
    """distance between two vectors"""
    return math.sqrt(squared_distance(v, w))
    
def scalar_multiply(c, v):
     """c is a number, v is a vector"""
     return [c * v_i for v_i in v]