from mean import mean
from median import median
from mode import mode

def main():
    try:
        with open("numbers.txt", "r") as file:
            content = file.read()
            raw_values = content.replace(",", " ").split()
            numbers = []
            words = []
            for item in raw_values:
                try:
                    numbers.append(float(item))       # for mean & median
                    words.append(str(item))           # for mode
                except ValueError:
                    continue  # ignore non-numeric data
    except FileNotFoundError:
        print("Error: 'numbers.txt' not found.")
        return

    print(f"Data: {numbers}")
    print(f"Mean: {mean(numbers)}")
    print(f"Median: {median(numbers)}")
    print(f"Mode: {mode(words)}")

if __name__ == "__main__":
    main()
