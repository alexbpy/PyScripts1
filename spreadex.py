import csv

def convert_text_to_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = infile.readlines()
        writer = csv.writer(outfile)

        # # Write header to CSV file (optional)
        # writer.writerow(["Column1", "Column2", "Column3", "Column4", "Column5"])

        # Process lines in groups of 5
        for i in range(0, len(reader), 5):
            # Ensure we have at least 5 lines to form a row
            row_data = [line.strip() for line in reader[i:i+5] if line.strip()]
            
            # Pad with empty strings if there are less than 5 lines in the group
            row_data += [''] * (5 - len(row_data))
            
            writer.writerow(row_data)

if __name__ == "__main__":
    input_file = "spreadex.txt"  # Replace with your input file name
    output_file = "spreadex.csv"  # Replace with your desired output CSV file name
    convert_text_to_csv(input_file, output_file)


convert_text_to_csv('spreadex.txt', 'spreadex.csv')