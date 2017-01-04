import random
from vectors import distance
import matplotlib.pyplot as plt
import numpy as np

def sum_of_squares(v):
    """computes the sum of squared elements in v"""
    return sum(v_i ** 2 for v_i in v)
    
def sum_of_squares_gradient(v):
    """computes the gradient (derivate) of sum of squared elements"""
    return [2 * v_i for v_i in v]

def step(v, direction, step_size):
     """move step_size in the direction from v"""
     return [v_i + step_size * direction_i
     for v_i, direction_i in zip(v, direction)]

# pick a random starting point
v = [random.randint(-3,3) for i in range(2)]

# how close two points have to be to consider convergence     
tolerance = 0.0000001

# prepare 3d plot
fig = plt.figure(figsize=(12,10))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
x = y = np.arange(-3.0, 3.0, 0.05)
X, Y = np.meshgrid(x, y)
zs = np.array([sum_of_squares([x,y]) for x,y in zip(np.ravel(X), np.ravel(Y))])
Z = zs.reshape(X.shape)
ax.plot_surface(X, Y, Z)

while True:
     gradient = sum_of_squares_gradient(v) # compute the gradient at v
     next_v = step(v, gradient, -0.01) # take a negative gradient step
     if distance(next_v, v) < tolerance: # stop if we're converging
         break
     v = next_v # continue if we're not
     ax.plot([v[0]],[v[1]],[sum_of_squares(v)], markerfacecolor='w', markeredgecolor='w', marker='x', markersize=5, alpha=0.6)
     
print v

plt.show()