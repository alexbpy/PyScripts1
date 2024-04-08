import os

def find_csv_file(filename):
    for file in os.listdir('.'):
        if file.endswith('.csv') and filename in file:
            return os.path.abspath(file)
    return None

if __name__ == "__main__":
    csv_file_name = "spreadex.csv"  # Replace with the file name or part of the CSV file name
    csv_file_location = find_csv_file(csv_file_name)

    if csv_file_location:
        print("CSV File Found at:", csv_file_location)
    else:
        print("CSV File Not Found.")
