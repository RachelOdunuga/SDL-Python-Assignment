import argparse
import numpy as np

def fizzbuzz(limit, rules):
    numbers = np.arange(1, limit + 1)

    for number in numbers:
        output = ""

        for factor in rules:
            if number % factor == 0:
                output += rules[factor]

        if output == "":
            output = number

        print(f"{number}:{output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    rules = {3: "Fizz", 5: "Buzz", 7: "Fang", 11: "Bang"}
    fizzbuzz(args.limit, rules)
