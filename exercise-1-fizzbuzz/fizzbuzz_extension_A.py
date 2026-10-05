
import numpy as np

numbers = np.arange(1, 101)

for number in numbers:
    output = ""

    if number % 3 == 0:
        output += "Fizz"
    if number % 5 == 0:
        output += "Buzz"
    if number % 7 == 0:
        output += "Fang"
    if number % 11 == 0:
        output += "Bang"

    if output == "":
        output = number

    print(f"{number}:{output}")
