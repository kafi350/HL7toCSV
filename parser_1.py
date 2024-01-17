# Description: This file contains a function that parses an HL7 file and writes the data to a CSV file.
# Author: Abdullahil Kafi
import sys
from hl7apy.parser import parse_segment
import csv

def parse_hl7_to_csv(hl7_file_path, csv_file_path):
    data = {
            'Patient Info': [],
            'Encounters': [],
            'Lab Reports': [],
    }
    with open(hl7_file_path, 'r') as file:
        for line in file:
            hl7_content = line.replace('\n', '\r')
            try:
                segment = parse_segment(hl7_content)
                if segment.name == 'PID':
                    patient_info = {field.name: field.value for field in segment.children if field.value is not None}
                    data['Patient Info'].append(patient_info)
                elif segment.name == 'PV1':
                    encounter_info = {field.name: field.value for field in segment.children if field.value is not None}
                    data['Encounters'].append(encounter_info)
                elif segment.name == 'OBX':
                    lab_info = {field.name: field.value for field in segment.children if field.value is not None}
                    data['Lab Reports'].append(lab_info)
            except Exception as e:
                print("Error parsing HL7 segment:", e)

    # Write data to CSV
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for segment_type, segments in data.items():
            writer.writerow([segment_type]) 
            for segment in segments:
                writer.writerow(segment.values()) 
                writer.writerow([]) 

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python parser_1.py <input.hl7> <output.csv>")
        sys.exit(1)

    hl7_file_path = sys.argv[1]
    csv_file_path = sys.argv[2]

    parse_hl7_to_csv(hl7_file_path, csv_file_path)
            