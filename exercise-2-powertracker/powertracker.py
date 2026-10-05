
import numpy as np 
import random

i = 1

results = []
maxima = []
minima = []

number = random.randint(1, 20)
decision = random.randint(0, 1)
if decision == 0:
    prev_result = number**2
    print(f"Loop {i}: {number}^2 = {prev_result}")
else:
    prev_result = number**3
    print(f"Loop {i}: {number}^3 = {prev_result}")

results.append(prev_result)


result = prev_result 

while True:
    i+=1
    number = random.randint(1, 20)
    decision = random.randint(0, 1)
    if decision == 0:
        result = number**2
        print(f"Loop {i}: {number}^2 = {result}")
    else:
        result = number**3
        print(f"Loop {i}: {number}^3 = {result}")

    results.append(result)
    maximum = np.max(results)
    maxima.append(maximum)
    minimum = np.min(results)
    minima.append(minimum)

    if result % prev_result == 0:
        break

    prev_result = result


print(f"The largest result is {np.max(maxima)}")
print(f"The smallest result is {np.min(minima)}")  
print(f"{result} is divisible by {prev_result}")
print(f"We completed {i} loops.")
