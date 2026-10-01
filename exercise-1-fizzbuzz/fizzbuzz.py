
import numpy as np

numbers = np.arange(1,101)

for number in numbers:
    if number % 3 == 0 and number % 5 == 0:
        output = "FizzBuzz"
    elif number % 3 == 0:
        output = "Fizz"
    elif number % 5 == 0:
        output = "Buzz"
    else:
        output = number
    print(f"{number}:{output}")
