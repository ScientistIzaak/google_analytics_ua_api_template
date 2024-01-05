# Import necessary modules
import pandas as pd
import time
from datetime import datetime, timedelta
from collections import defaultdict
from google.oauth2 import service_account
from googleapiclient.discovery import build


# Set the path to your service account key file
keyfile_path = 'path/to/your/credentials.json'

# Authenticate & Build Service
try:
    credentials = service_account.Credentials.from_service_account_file(
        keyfile_path, scopes=['https://www.googleapis.com/auth/analytics.readonly']
    )
    analytics = build('analyticsreporting', 'v4', credentials=credentials)
except Exception as e:
    print(f"Authentication error: {e}")
    # Handle authentication error gracefully, e.g., by exiting the script or logging the error.

# Set Request Parameters
start_date_str = 'YYYY-MM-DD'  # Replace with your start date
end_date_str = 'YYYY-MM-DD'    # Replace with your end date

start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

duration = (end_date - start_date).days

views = {'Your View Name': 'Your View ID'}  # Replace with your view names and IDs
dimensions = [
              # Dimensions go here
             ]

metrics = [
            # Metrics go here
          ]

# List to store DataFrames
dfs = []

# Loop through each day
for day in range(duration + 1):
    current_date = start_date + timedelta(days=day)
    current_date_str = current_date.strftime("%Y-%m-%d")

    # Build request body for each day
    body = {
        "reportRequests": [
            {
                "viewId": views['Your View Name'],
                "dateRanges": [
                    {
                        "startDate": current_date_str,
                        "endDate": current_date_str
                    }
                ],
                "dimensions": [{'name': dimension} for dimension in dimensions],
                "metrics": [{'expression': metric} for metric in metrics],
                "pageSize": 100000,
                "samplingLevel": "LARGE"
            }
        ]
    }

    # Make Request for each day
    try:
        response = analytics.reports().batchGet(body=body).execute()
    except Exception as e:
        print(f"API request error for {current_date_str}: {e}")
        continue  # Skip to the next iteration if there is an error

    # Parse Request for each day
    report_data = defaultdict(list)

    for report in response.get('reports', []):
        rows = report.get('data', {}).get('rows', [])
        for row in rows:
            for i, key in enumerate(dimensions):
                report_data[key].append(row.get('dimensions', [])[i])  # Get dimensions

            for values in row.get('metrics', []):
                all_values = values.get('values', [])  # Get metric values
                for i, key in enumerate(metrics):
                    report_data[key].append(all_values[i])

    # Create DataFrame for each day
    df = pd.DataFrame(report_data)

    # Append DataFrame to the list
    dfs.append(df)
    
    # 1-second delay between API calls
    time.sleep(1)

# Concatenate all DataFrames in the list
final_df = pd.concat(dfs, ignore_index=True)

# Transform Date column to Datetime format
final_df['ga:Date'] = pd.to_datetime(final_df['ga:Date'])

# Group by year and create separate DataFrames
yearly_dfs = {year: group for year, group in final_df.groupby(final_df['ga:Date'].dt.year)}

# Specify the base file path for the CSV files
base_csv_file_path = "ga_analytics_data_{}.csv"

# Loop through the years and save each DataFrame to a separate CSV file
for year, df in yearly_dfs.items():
    # Specify the file path for the CSV file
    csv_file_path = base_csv_file_path.format(year)
    
    # Save the DataFrame to the CSV file
    df.to_csv(csv_file_path, index=False)
    
    print(f"DataFrame for {year} saved to {csv_file_path}
