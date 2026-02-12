import xml.etree.ElementTree as ET
from datetime import datetime
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (project root)
project_root = os.path.dirname(script_dir)

# Construct paths relative to project root
file_path = os.path.join(project_root, 'exported_data', 'export.xml')
sleep_output_path = os.path.join(project_root, 'imported_data', 'filtered_sleep_records.xml')
heart_rate_output_path = os.path.join(project_root, 'imported_data', 'filtered_heart_rate_records.xml')

tree = ET.parse(file_path)
root = tree.getroot()

# Define date range
start_filter = datetime(2026, 1, 19)
end_filter = datetime(2026, 2, 9)

# Find all sleep analysis records
sleep_records = root.findall('.//Record[@type=\'HKCategoryTypeIdentifierSleepAnalysis\']')

# Filter by date range
filtered_sleep_records = []
for record in sleep_records:
    if record.get('value', '').startswith("HKCategoryValueSleepAnalysisAsleep"):
        start_date_str = record.get('startDate')
        if start_date_str:
            record_date = datetime.strptime(start_date_str.split(' ')[0], '%Y-%m-%d')
            if start_filter <= record_date <= end_filter:
                filtered_sleep_records.append(record)
 
# Find all heart rate records
heart_rate_records = root.findall('.//Record[@type=\'HKQuantityTypeIdentifierHeartRate\']')

# Filter by date range and time (11 pm to 10 am)
filtered_heart_rate_records = []
for record in heart_rate_records:
    start_date_str = record.get('startDate')
    if start_date_str:
        record_datetime = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S %z")
        record_date = record_datetime.date()
        record_time = record_datetime.time()

        if start_filter.date() <= record_date <= end_filter.date():
            if record_time.hour >= 23 or record_time.hour < 10:
                filtered_heart_rate_records.append(record)


with open(sleep_output_path, 'w') as f:
    for record in filtered_sleep_records:
            start_date = record.get('startDate')
            end_date = record.get('endDate')
            value = record.get('value')
            f.write(f'Start: {start_date}, End: {end_date}, Value: {value}\n')

with open(heart_rate_output_path, 'w') as f:
    for record in filtered_heart_rate_records:
        start_date = record.get('startDate')
        value = record.get('value')
        f.write(f'Start: {start_date}, Value: {value}\n')

print(f'Saved {len(filtered_sleep_records)} sleep records and {len(filtered_heart_rate_records)} heart rate records')

