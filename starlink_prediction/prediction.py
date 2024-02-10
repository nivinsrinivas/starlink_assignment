import psycopg2
import csv
import pandas as pd
import sys
from datetime import datetime

from sklearn.linear_model import LinearRegression

# Database connection parameters
dbname = 'postgres'
user = 'meltano'
password = 'password'
host = 'localhost'
port = '5432'

# Name of the table to fetch data from
schema = 'analytics'
table_name = 'starlink_prediction'

# Name of the output CSV file
output_csv_file = 'starlink_prediction.csv'


try:
    # Establish a connection to the database
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    # Create a cursor object using the connection
    cursor = conn.cursor()

except psycopg2.Error as e:
    # Print error message
    print("Error connecting to the PostgreSQL database:", e)
    sys.exit(1)

# Fetch all data from the starlink_prediction table
cursor.execute(f"SELECT * FROM {schema}.{table_name}")
rows = cursor.fetchall()

# Close DB connection
cursor.close()
conn.close()


# Write the data to a CSV file
with open(output_csv_file, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([desc[0] for desc in cursor.description])  # Write column headers
    csv_writer.writerows(rows)  # Write rows of data

print(f"\nData from table '{table_name}' exported to '{output_csv_file}'")


# Silence pandas warnings
pd.options.mode.chained_assignment = None

# Load the data to a dataframe
starlink_data_df = pd.read_csv('starlink_prediction.csv')


starlink_data_df['satellite_name'] = starlink_data_df['satellite_name'].fillna('0')
starlink_data_df['satellite_number'] = starlink_data_df['satellite_name'].str.extract(r'(\d+)').astype(float).astype(pd.Int64Dtype())

# Filter null data
starlink_data_filtered_df = starlink_data_df[starlink_data_df['satellite_name'].str.contains('STARLINK', na=False)]


# Find number of satellites launched so far
latest_satellite_count = int(starlink_data_filtered_df['satellite_number'].max())

print("\nNumber of satellites launched so far:", latest_satellite_count)


# Predicting when will Spacex Launch 42000 Starlink satellites ?!

# Convert launch_date to datetime
starlink_data_filtered_df['launch_date'] = pd.to_datetime(starlink_data_filtered_df['launch_date'])

# Drop rows with NaN values in the satellite_number column
starlink_data_filtered_df.dropna(subset=['satellite_number'], inplace=True)


# Sort DataFrame by launch_date
starlink_data_filtered_df.loc[:, 'launch_date'] = pd.to_datetime(starlink_data_filtered_df['launch_date'])

# Create a new DataFrame with only launch_date and satellite_number
df_filtered = starlink_data_filtered_df[['launch_date', 'satellite_number']]

# Create features (X) and target variable (y)
X = df_filtered['launch_date'].astype(int).values.reshape(-1, 1)  # Convert launch_date to integer for regression
y = df_filtered['satellite_number'].values

# Fit linear regression model
model = LinearRegression()
model.fit(X, y)

# Predict satellite_number for the date when it reaches 42000
date_42000 = (42000 - model.intercept_) / model.coef_[0]
# Convert to seconds
date = str(datetime.utcfromtimestamp(date_42000 / 1e9).date())

print(f"\nThe date by when Spacex will launch 42000 Starlink satellites is predicted to be approximately: {date} !!!\n")



