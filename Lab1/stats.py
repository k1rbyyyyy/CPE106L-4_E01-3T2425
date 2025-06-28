def mean(numbers):
    """Return the average of a list of numbers."""
    if not numbers:
        raise ValueError("The list is empty.")
    return sum(numbers) / len(numbers)

def median(numbers):
    """Return the median of a list of numbers."""
    if not numbers:
        raise ValueError("The list is empty.")
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
    else:
        return sorted_nums[mid]

def mode(numbers):
    """Return the mode of a list of numbers."""
    if not numbers:
        raise ValueError("The list is empty.")
    counts = {}
    for num in numbers:
        counts[num] = counts.get(num, 0) + 1
    max_count = max(counts.values())
    modes = [num for num, count in counts.items() if count == max_count]
    # If multiple modes, return the smallest one
    return min(modes)