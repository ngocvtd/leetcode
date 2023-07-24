import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Given data points
x_data = np.array([0.0, 0.5, 1.0, 1.5, 1.9, 2.5, 3.0, 3.5, 4.0, 4.5,
                   5.0, 5.5, 6.0, 6.6, 7.0, 7.6, 8.5, 9.0, 10.0])
y_data = np.array([1.0, 0.9, 0.7, 1.5, 2.0, 2.4, 3.2, 2.0, 2.7, 3.5,
                   1.0, 4.0, 3.6, 2.7, 5.7, 4.6, 6.0, 6.8, 7.3])

# Linear function: y = bx + a
def linear_func(params, x):
    a, b = params
    return b * x + a

# Quadratic function: y = cx^2 + bx + a
def quadratic_func(params, x):
    a, b, c = params
    return c * x**2 + b * x + a

# Objective function for linear model: Sum of squared residuals
def linear_objective(params):
    return np.sum((linear_func(params, x_data) - y_data)**2)

# Objective function for quadratic model: Sum of squared residuals
def quadratic_objective(params):
    return np.sum((quadratic_func(params, x_data) - y_data)**2)

# Initial guesses for parameters
initial_guess_linear = [0, 1]  # [a, b]
initial_guess_quadratic = [0, 1, 1]  # [a, b, c]

# Perform optimization to find the best linear model parameters
result_linear = minimize(linear_objective, initial_guess_linear)
params_linear = result_linear.x

# Perform optimization to find the best quadratic model parameters
result_quadratic = minimize(quadratic_objective, initial_guess_quadratic)
params_quadratic = result_quadratic.x

# Plot the original data and the fitted curves
plt.scatter(x_data, y_data, label='Data Points')
plt.plot(x_data, linear_func(params_linear, x_data), label='Linear Fit')
plt.plot(x_data, quadratic_func(params_quadratic, x_data), label='Quadratic Fit')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Data and Fitted Curves')
plt.grid(True)
plt.show()

