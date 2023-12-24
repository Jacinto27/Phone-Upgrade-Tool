import os
import re

from pandas import Series, read_csv, to_datetime, DataFrame

# Path configuration
script_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.dirname(os.path.dirname(script_dir))


# Functions
def split_os(string: str):
    regex = r'(\d+(\.\d+){0,2})'
    parts = re.split(regex, string, maxsplit=1)
    if len(parts) >= 2:
        return parts[0].strip(), parts[1].strip()
    else:
        return string.strip(), ''


# Read Data
datafile = os.path.join(project_root, 'Data', 'Raw', 'cleaned_all_phones.csv')  # File Location

data = read_csv(datafile)
data = DataFrame(data)

data = data.drop(['inches', 'battery_type', 'weight(g)'], axis=1)  # Remove unnecessary columns

# OS name cleaning

data[['system', 'version']] = data['os'].apply(lambda x: Series(split_os(x)))  # Split columns

# brief cleaning
filtered_phone_names = data[data['version'] == '']['phone_name'].astype(str).tolist()
data = data[~data['phone_name'].isin(filtered_phone_names)]  # Remove phone with no version number

data = data.drop(['os'], axis=1)  # Drop os column

# Extract p value from Screen resolution

data['resolution'] = data['resolution'].str.extract(r'x(\d+)')  # All values after the 'x' in the middle

# Convert release date column to to datetime
data['announcement_date'] = to_datetime(data['announcement_date'])

datafile_save = os.path.join(project_root, 'Data', 'Processed', 'cleaned_all_phones_processed.csv')  # File Location

data.to_csv(datafile_save, index=False)
