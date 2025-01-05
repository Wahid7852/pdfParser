import os
import csv

csv_directory = "csvs"
output_csv = "merged_dataset.csv"

csv_files = [file for file in os.listdir(csv_directory) if file.endswith(".csv")]

if not csv_files:
    print("No CSV files found in the directory!")
else:
    header_written = False

    with open(output_csv, 'w', newline='') as outfile:
        writer = None

        for idx, csv_file in enumerate(csv_files):
            csv_path = os.path.join(csv_directory, csv_file)

            with open(csv_path, 'r') as infile:
                reader = csv.reader(infile)
                rows = list(reader)

                if idx == 0:
                    header = rows[0] if rows else []
                    writer = csv.writer(outfile)
                    writer.writerow(header)
                    header_written = True

                if len(rows) > 1:
                    content_row = rows[1]
                    writer.writerow(content_row)

    print(f"Merged CSV file created: {output_csv}")
