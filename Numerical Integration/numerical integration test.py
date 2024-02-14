import numpy as np
from scipy.integrate import quad

# function we want to integrate
def f(x):
    return np.exp(np.cos(-2 * x * np.pi)) + 3.2

# call quad to integrate f from -2 to 2. Returns value of integration and the error
res, err = quad(f, -2, 2)

print("The numerical result is {:f} (+-{:g})"
    .format(res, err))

