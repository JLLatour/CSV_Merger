import csv
import os
from datetime import datetime

def choose_file(prompt):
    # List CSV files in the current directory
    csv_files = [f for f in os.listdir() if f.endswith('.csv')]
    if not csv_files:
        print("No CSV files found in the current directory.")
        return None

    print(f"{prompt} (Select a file by number):")
    for i, file in enumerate(csv_files, 1):
        print(f"{i}: {file}")

    choice = int(input(f"Enter the number corresponding to the file you want to use: ")) - 1
    if 0 <= choice < len(csv_files):
        return csv_files[choice]
    else:
        print("Invalid choice.")
        return None

def choose_column(headers, prompt):
    # List columns in the current CSV file
    print(f"\n{prompt}")
    for i, header in enumerate(headers, 1):
        print(f"{i}: {header}")
    column_choice = int(input(f"Enter the number corresponding to the column you want to use (1-indexed): ")) - 1
    if 0 <= column_choice < len(headers):
        return column_choice
    else:
        print("Invalid choice.")
        return None


def normalize_key(key):
    return key.strip().lower()


def merge_csv():
    # Choose file1 and file2 from the current directory
    file1 = choose_file("Choose the first CSV file")
    if not file1:
        return

    file2 = choose_file("Choose the second CSV file")
    if not file2:
        return

    # Read the headers from both files
    with open(file1, mode='r', newline='', encoding='utf-8') as f1:
        reader = csv.reader(f1)
        headers1 = next(reader)  # Read header row of the first file

    with open(file2, mode='r', newline='', encoding='utf-8') as f2:
        reader = csv.reader(f2)
        headers2 = next(reader)  # Read header row of the second file

    # Display headers and ask user for the primary key columns
    primary_key_column1 = choose_column(headers1, f"Choose the primary key column in {file1} based on these headers:")
    if primary_key_column1 is None:
        return

    primary_key_column2 = choose_column(headers2, f"Choose the primary key column in {file2} based on these headers:")
    if primary_key_column2 is None:
        return

    # Read the second file into a dictionary where the primary key column is the key
    second_file_data = {}

    with open(file2, mode='r', newline='', encoding='utf-8') as f2:
        reader = csv.reader(f2)
        next(reader)  # Skip header row
        for row in reader:
            key = row[primary_key_column2]
            if key not in second_file_data:
                second_file_data[key] = [row]
            else:
                second_file_data[key].append(row)  # Store multiple matches for the same key

    # Read the first file and merge data based on the primary key
    merged_rows = []
    with open(file1, mode='r', newline='', encoding='utf-8') as f1:
        reader = csv.reader(f1)
        next(reader)  # Skip header row of the first file

        for row in reader:
            try:
                key = row[primary_key_column1]
                normalized_key = normalize_key(key)
                if normalized_key in [normalize_key(k) for k in second_file_data.keys()]:
                    # If there are multiple matches, ask the user to choose which one is correct
                    if len(second_file_data[key]) > 1:
                        if key != '':
                            selected_match = []
                        else:
                            print(f"\nMultiple matches found for key '{key}' in {file2}:")
                            for i, option in enumerate(second_file_data[key]):
                                print(f"{i + 1}: {option}")
                            choice = int(input("Enter the number corresponding to the correct match: ")) - 1
                            if choice == "":
                                selected_match = []
                            else:
                                selected_match = second_file_data[key][choice]
                    else:
                        # If only one match, use that match
                        selected_match = second_file_data[key][0]

                    # Merge the selected match with the row from the first file
                    merged_row = row + selected_match
                else:
                    # If no match, keep the row from the first file as is
                    merged_row = row

                merged_rows.append(merged_row)
            except Exception as e:
                print(e)


    # Write the merged data to the primary output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"output_{timestamp}.csv"
    with open(output_file, mode='w', newline='', encoding='utf-8') as output:
        writer = csv.writer(output)
        writer.writerow(headers1 + headers2)  # Write the header
        writer.writerows(merged_rows)  # Write the merged rows

    print(f"Data merged successfully into {output_file}.")

    # Write the unmatched rows to a secondary output file
    unmatched_file = f"unmatched_{timestamp}.csv"
    with open(unmatched_file, mode='w', newline='', encoding='utf-8') as output_unmatched:
        writer = csv.writer(output_unmatched)
        writer.writerow(headers2)  # Write the header of the second file
        for key, rows in second_file_data.items():
            for row in rows:
                if key not in [r[primary_key_column1] for r in merged_rows]:
                    writer.writerow(row)

    print(f"Unmatched rows saved to {unmatched_file}.")




if __name__ == '__main__':
    merge_csv()

