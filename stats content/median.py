"""
File: median.py
Prints the median of a set of numbers in a file.
"""

def median(numbers):
    if not numbers:
        return 0
    numbers.sort()
    midpoint = len(numbers) // 2
    if len(numbers) % 2 == 1:
        return numbers[midpoint]
    else:
        return (numbers[midpoint] + numbers[midpoint - 1]) / 2

