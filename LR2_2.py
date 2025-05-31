def navigate_file_lines():
    # Prompt for filename
    filename = input("Enter the filename: ")
    
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Error: File not found.")
        return

    total_lines = len(lines)
    print(f"The file has {total_lines} lines.")
    print("Enter a line number between 1 and", total_lines, "(or 0 to quit):")

    while True:
        try:
            line_number = int(input("Line number: "))
            if line_number == 0:
                print("Goodbye!")
                break
            elif 1 <= line_number <= total_lines:
                print(f"Line {line_number}: {lines[line_number - 1].rstrip()}")
            else:
                print(f"Invalid line number. Please enter a number between 1 and {total_lines}.")
        except ValueError:
            print("Please enter a valid number.")

navigate_file_lines()
