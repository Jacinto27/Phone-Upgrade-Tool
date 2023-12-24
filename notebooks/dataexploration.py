import os
import re

import pandas as pd

scrpath = os.path.abspath(__file__)
scrdir = os.path.dirname(scrpath)
project_root = os.path.dirname(scrdir)


# Functions
def split_os(string):
    regex = r'(\d+(\.\d+){0,2})'
    parts = re.split(regex, string, maxsplit=1)
    if len(parts) >= 2:
        return parts[0].strip(), parts[1].strip()
    else:
        return string.strip(), ''


datafile = os.path.join(project_root, 'Data', 'Raw', 'cleaned_all_phones.csv')

data = pd.read_csv(datafile)
data = pd.DataFrame(data)

data1 = data.drop(['inches', 'battery_type', 'weight(g)'], axis=1)

# print(data1.columns)
#
# print(data1['os'].unique())
# OS cleaning
data1[['system', 'version']] = data1['os'].apply(lambda x: pd.Series(split_os(x)))

data1 = data1[~data1['phone_name'].isin(data1[data1['version'] == '']['phone_name'].astype(str).tolist())].drop(['os'],
                                                                                                                axis=1)

# print(data1[['system','version']].drop_duplicates())
# print(data1[data1['version']=='']['phone_name'].astype(str).tolist())

# Resolution change to p

data1['resolution'] = data1['resolution'].str.extract(r'x(\d+)')

# To datetime
data1['announcement_date'] = pd.to_datetime(data1['announcement_date'])
