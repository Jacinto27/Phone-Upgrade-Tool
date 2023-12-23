import pandas as pd

data = pd.read_csv('../Data/Raw/cleaned_all_phones.csv')

#print(data.columns)

data1 = data.drop(['inches', 'battery_type', 'weight(g)'], axis=1)
print(data1.columns)

print(data1['os'].unique())