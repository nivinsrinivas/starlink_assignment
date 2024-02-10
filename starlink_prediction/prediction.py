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
starlink_data_csv = 'starlink_prediction.csv'


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
with open(starlink_data_csv, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([desc[0] for desc in cursor.description])  # Write column headers
    csv_writer.writerows(rows)  # Write rows of data

print(f"\nData from table '{table_name}' exported to '{starlink_data_csv}'\n")


# Silence pandas warnings
pd.options.mode.chained_assignment = None


def get_starlink_data():
    """Process CSV data, filter NULLs"""
    # Load the data to a dataframe
    starlink_data_df = pd.read_csv(starlink_data_csv)

    # Convert launch_date to datetime
    starlink_data_df['launch_date'] = pd.to_datetime(starlink_data_df['launch_date'])
    
    starlink_data_df['satellite_name'] = starlink_data_df['satellite_name'].fillna('0')
    starlink_data_df['satellite_number'] = starlink_data_df['satellite_name'].str.extract(r'(\d+)').astype(float).astype(pd.Int64Dtype())


    # Filter null data
    starlink_data_filtered_df = starlink_data_df[starlink_data_df['satellite_name'].str.contains('STARLINK', na=False)]

    # Drop rows with NaN values in the satellite_number column
    starlink_data_filtered_df.dropna(subset=['satellite_number'], inplace=True)

    # Sort DataFrame by launch_date
    starlink_data_filtered_df.loc[:, 'launch_date'] = pd.to_datetime(starlink_data_filtered_df['launch_date'])    

    return [starlink_data_df, starlink_data_filtered_df]

def predict_target_date():
    """Function to predict date by when 42000 satellites will be launched"""

    starlink_data_filtered_df = get_starlink_data()[1]

    # Predicting when will Spacex Launch 42000 Starlink satellites ?!
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

    print(f"\nThe date by when Spacex will launch 42000 Starlink satellites is predicted to be approximately: {date}!!\n")



def predict_number_of_launches():
    """Get the number of launches it will take to reach 42000 satellites"""
    # Fetch distinct count of launch_dates
    starlink_data_unfiltered_df = get_starlink_data()[0]
    distinct_launch_count = starlink_data_unfiltered_df['launch_date'].nunique()
    
    print("Number of SpaceX launches of starlink satellites, so far:", distinct_launch_count)
    
    starlink_data_filtered_df = get_starlink_data()[1]

    # Find number of satellites launched so far
    latest_satellite_count = int(starlink_data_filtered_df['satellite_number'].max())

    print("\nNumber of satellites launched so far:", latest_satellite_count)

    # Calculate the average number of satellites launched per launch
    average_satellites_per_launch = latest_satellite_count / distinct_launch_count

    # Estimate the number of launches needed to reach 42,000 satellites
    estimated_launches_needed = (42000 - latest_satellite_count) / average_satellites_per_launch

    # Round up to the nearest integer
    estimated_launches_needed = int(estimated_launches_needed + 0.5)

    print("\nEstimated number of launches needed to reach 42,000 Starlink satellites:", estimated_launches_needed)



predict_number_of_launches()
predict_target_date()