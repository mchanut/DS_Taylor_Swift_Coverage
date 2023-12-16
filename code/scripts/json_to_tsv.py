import json
import argparse
import os
import shutil
import csv
import re

"""
Wanted usage:

python3 json_to_tsv.py -i <json_file> -o <out_file>
"""

def write_output_file(input, output):
    if not os.path.exists("data/tsv_data"):
        os.makedirs("data/tsv_data")

    output_path = os.path.join("data/tsv_data", os.path.basename(output))

    csv.register_dialect('tsv_dialect', delimiter='\t', quoting=csv.QUOTE_ALL, lineterminator='\n')

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='tsv_dialect')

        writer.writerow(["Title", "Description", "Coding"])

        for article in input:
            title = re.sub(r'[\r\n]+', ' ', article["title"])
            description = re.sub(r'[\r\n]+', ' ', article["description"])
            writer.writerow([title, description, ''])

def main():

    parser = argparse.ArgumentParser(description="Convert a json file into a tsv file.")

    parser.add_argument("-i", "--input", required=True, metavar="<json_file>", help="Json file to convert.")
    parser.add_argument("-o", "--output", required=True, metavar="<tsv_file>", help="Name of output tsv file.")
    
    args = parser.parse_args()
    
    input = args.input
    output = args.output

    if not os.path.exists("data/raw_data"):
        os.makedirs("data/raw_data")

    input_path = os.path.join("data/raw_data", os.path.basename(input))
    
    if not os.path.exists(input_path):
        shutil.move(input, "data/raw_data")

    with open(input_path, 'r') as f:
        data = json.load(f)

    write_output_file(data, output)


if __name__ == "__main__":
    main()