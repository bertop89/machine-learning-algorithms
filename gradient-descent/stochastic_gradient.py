import random
import numpy as np
from vectors import vector_subtract, scalar_multiply

def sum_of_squares(v):
    """computes the sum of squared elements in v"""
    return sum(v_i ** 2 for v_i in v)
    
def sum_of_squares_gradient(v):
    return [2 * v_i for v_i in v]

def in_random_order(data):
     """generator that returns the elements of data in random order"""
     indexes = [i for i, _ in enumerate(data)] # create a list of indexes
     random.shuffle(indexes) # shuffle them
     for i in indexes: # return the data in that order
        yield data[i]

def my_fun(x, y, theta): 
    return (y - theta[0] - theta[1]*x - theta[2]*(x**2)) ** 2

def my_grad_fun(x, y, theta): 
    return ((y - theta[1] - theta[2]*(x*2)) ** 2)

def minimize_stochastic(target_fn, gradient_fn, x, y, theta_0, alpha_0=0.01):
     data = zip(x, y)
     theta = theta_0 # initial guess
     alpha = alpha_0 # initial step size
     min_theta, min_value = None, float("inf") # the minimum so far
     iterations_with_no_improvement = 0
     # if we ever go 100 iterations with no improvement, stop
     while iterations_with_no_improvement < 100:
         value = sum( target_fn(x_i, y_i, theta) for x_i, y_i in data )
     
         if value < min_value:
             # if we've found a new minimum, remember it
             # and go back to the original step size
             min_theta, min_value = theta, value
             iterations_with_no_improvement = 0
             alpha = alpha_0
         else:
             # otherwise we're not improving, so try shrinking the step size
             iterations_with_no_improvement += 1
             alpha *= 0.9
         # and take a gradient step for each of the data points
         for x_i, y_i in in_random_order(data):
             gradient_i = gradient_fn(x_i, y_i, theta)
             theta = vector_subtract(theta, scalar_multiply(alpha, gradient_i))
     return min_theta
     
def maximize_stochastic(target_fn, gradient_fn, x, y, theta_0, alpha_0=0.01):
    return minimize_stochastic(negate(target_fn),
                               negate_all(gradient_fn),
                               x, y, theta_0, alpha_0)

def step(v, direction, step_size):
    """move step_size in the direction from v"""
    return [v_i + step_size * direction_i
            for v_i, direction_i in zip(v, direction)]

def negate(f):
    """return a function that for any input x returns -f(x)"""
    return lambda *args, **kwargs: -f(*args, **kwargs)
    
def negate_all(f):
    """the same when f returns a list of numbers"""
    return lambda *args, **kwargs: [-y for y in f(*args, **kwargs)]

def safe(f):
    """define a new function that wraps f and return it"""
    def safe_f(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            return float('inf')         # this means "infinity" in Python
    return safe_f

def minimize_batch(target_fn, gradient_fn, theta_0, tolerance=0.000001):
    """use gradient descent to find theta that minimizes target function"""
    
    step_sizes = [100, 10, 1, 0.1, 0.01, 0.001, 0.0001, 0.00001]
    
    theta = theta_0                           # set theta to initial value
    target_fn = safe(target_fn)               # safe version of target_fn
    value = target_fn(theta)                  # value we're minimizing
    
    while True:
        gradient = gradient_fn(theta)  
        next_thetas = [step(theta, gradient, -step_size)
                       for step_size in step_sizes]
                   
        # choose the one that minimizes the error function        
        next_theta = min(next_thetas, key=target_fn)
        next_value = target_fn(next_theta)
        
        # stop if we're "converging"
        if abs(value - next_value) < tolerance:
            return theta
        else:
            theta, value = next_theta, next_value
            
def maximize_batch(target_fn, gradient_fn, theta_0, tolerance=0.000001):
    return minimize_batch(negate(target_fn),
                          negate_all(gradient_fn),
                          theta_0, 
                          tolerance)
     
if __name__ == "__main__":
    
    x = [random.randint(-3,3) for i in range(10)]
    y = [random.randint(-3,3) for i in range(10)]
    
    minimize_stochastic(my_fun, my_grad_fun, x, y, [0,1,0])