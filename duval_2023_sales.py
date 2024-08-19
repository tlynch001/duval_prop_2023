import pandas as pd
import os

# Get the user's home directory using the USERPROFILE environment variable
user_home_dir = os.environ['USERPROFILE']

# Construct the file path using the user's home directory
file_path = os.path.join(user_home_dir, 'Downloads', 'Duval 26 Preliminary NAL 2024', 'NAL26P202401.csv')

# Load the CSV file
data = pd.read_csv(file_path)

# Clean the ZIP code column: Convert to string and remove any '.0' suffix from ZIP codes
data['OWN_ZIPCD'] = data['OWN_ZIPCD'].fillna('').astype(str).str.replace(r'\.0$', '', regex=True)

# List of Duval zip codes to exclude
duval_zip_codes = [
    '32218', '32210', '32244', '32246', '32256', '32225', '32224', '32257',
    '32216', '32211', '32207', '32209', '32208', '32258', '32277', '32221',
    '32205', '32250', '32223', '32233', '32217', '32226', '32206', '32222',
    '32254', '32219', '32220', '32234', '32204', '32266', '32202', '32276',
    '32290', '32212', '32227', '32267', '32099', '32215', '32230', '32237',
    '32201', '32203', '32214', '32228', '32229', '32232', '32231', '32236',
    '32235', '32238', '32240', '32239', '32241', '32245', '32247', '32255'
]

# Filter records with SALE_YR1 as 2023
sales_2023_data = data[data['SALE_YR1'] == 2023]

# Filter the records for those outside the Duval ZIP codes
sales_outside_duval = sales_2023_data[~sales_2023_data['OWN_ZIPCD'].isin(duval_zip_codes)]

# Calculate the total number of records
total_sales_2023 = sales_2023_data.shape[0]
total_sales_outside_duval = sales_outside_duval.shape[0]

# Get the top 15 owners by count outside Duval ZIP codes
top_owners_outside_duval = sales_outside_duval.groupby(['OWN_NAME', 'OWN_CITY', 'OWN_STATE']).size().reset_index(name='Count')
top_owners_outside_duval = top_owners_outside_duval.sort_values(by='Count', ascending=False).head(15)

# Output the results
print(f"Total sales in 2023: {total_sales_2023}")
print(f"Total sales to people outside Duval ZIP code: {total_sales_outside_duval}")
print("\nTop 15 people by count (outside Duval ZIP codes):")
print(top_owners_outside_duval)
