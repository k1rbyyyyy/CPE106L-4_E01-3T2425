"""
File: mode.py
Prints the mode of a set of numbers in a file.
"""

def mode(words):
    if not words:
        return 0
    theDictionary = {}
    for word in words:
        word = word.upper()
        theDictionary[word] = theDictionary.get(word, 0) + 1
    theMaximum = max(theDictionary.values())
    modes = [key for key, value in theDictionary.items() if value == theMaximum]
    return modes[0] if len(modes) == 1 else modes
