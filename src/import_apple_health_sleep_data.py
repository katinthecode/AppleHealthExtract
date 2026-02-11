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
sleep_records = root.findall(".//Record[@type='HKCategoryTypeIdentifierSleepAnalysis']")

# Filter by date range
filtered_sleep_records = []
for record in sleep_records:
    start_date_str = record.get('startDate')
    if start_date_str:
        # Parse the date (format: "2018-05-01 22:45:00 -0600")
        record_date = datetime.strptime(start_date_str.split(' ')[0], '%Y-%m-%d')
        if start_filter <= record_date <= end_filter:
            filtered_sleep_records.append(record)

# Find all heart rate records
heart_rate_records = root.findall(".//Record[@type='HKQuantityTypeIdentifierHeartRate']")

# Filter by date range and time (midnight to 10 am)
filtered_heart_rate_records = []
for record in heart_rate_records:
    start_date_str = record.get('startDate')
    if start_date_str:
        # Parse the date and time (format: "2018-05-01 22:45:00 -0600")
        date_time_part = start_date_str.split(' ')[0:2]  # Get date and time
        record_datetime = datetime.strptime(date_time_part[0] + ' ' + date_time_part[1], '%Y-%m-%d %H:%M:%S')
        record_date = record_datetime.date()
        record_time = record_datetime.time()
        
        # Check if date is in range and time is between midnight and 10 am
        if start_filter.date() <= record_date <= end_filter.date():
            if record_time.hour < 10:  # 0 to 9 (midnight to 10 am)
                filtered_heart_rate_records.append(record)

with open(sleep_output_path, 'w') as f:
    for record in filtered_sleep_records:
        xml_str = ET.tostring(record, encoding='unicode')
        f.write(xml_str + '\n')

with open(heart_rate_output_path, 'w') as f:
    for record in filtered_heart_rate_records:
        xml_str = ET.tostring(record, encoding='unicode')
        f.write(xml_str + '\n')

print(f"Saved {len(filtered_sleep_records)} sleep records and {len(filtered_heart_rate_records)} heart rate records")

