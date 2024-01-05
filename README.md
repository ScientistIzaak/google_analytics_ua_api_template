# Google Analytics (Universal Analytics) Data Extraction and Processing

This script is designed for extracting data from Google Analytics (Universal Analytics) using the Google Analytics Reporting API, processing the data, and saving it into separate CSV files based on the year. The script utilizes the Python programming language and several required modules, as outlined below.

## Prerequisites

Before running the script, ensure that you have the necessary prerequisites:

  - Python installed on your machine
  - Google Analytics account with the necessary permissions
  - Service account key file for authentication

## Getting Started

1. Install the required Python modules using the following command:

    ```bash
    pip install pandas google-auth google-auth-oauthlib google-auth-httplib2
    ```

2. Set the path to your service account key file:

    ```python
    keyfile_path = 'path/to/your/credentials.json'
    ```

3. Replace the placeholder values in the script with your specific configurations:

   - `start_date_str` and `end_date_str`: Replace with your desired start and end dates in the format 'YYYY-MM-DD'.
   - `views`: Replace with your Google Analytics view names and corresponding view IDs.
   - `dimensions`: Replace with the desired dimensions for your Google Analytics report.
   - `metrics`: Replace with the desired metrics for your Google Analytics report.

## Running the Script

Execute the script in your Python environment. The script will authenticate, make API requests for each day within the specified date range, parse the responses, and create separate DataFrames for each day. Finally, it will concatenate all DataFrames, transform the 'ga:Date' column to Datetime format, group the data by year, and save each year's data into separate CSV files.
    
## Notes
  - The script includes a 1-second delay between API calls to comply with rate limits.
  - In case of authentication or API request errors, appropriate error messages will be displayed.
  - The resulting CSV files will be saved with filenames in the format ga_analytics_data_YEAR.csv.
    
Feel free to customize the script further based on your specific reporting needs. Note that this script is specifically designed for Universal Analytics. If you are using Google Analytics 4, adjustments may be required.
