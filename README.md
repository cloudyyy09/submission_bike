You can run the file by following these steps:
1. clone this repository:
   
   git clone https://github.com/cloudyyy09/submission_bike
   


## Run Streamlit App
To run the dashboard:
1. Download the dashboard folder (do not move files within it).
2. Install Streamlit:
   
   pip install streamlit
   
3. Install required libraries (pandas, numpy, scipy, matplotlib, seaborn, plotly).
4. Open dashboard.py in VSCode.
5. Run the dashboard:
   
   streamlit run dashboard/dashboard.py
   


## Questions Explored
The analysis answers the following questions:
1. What is the trend of bike-sharing usage each year?  
2. How does weather condition affect the percentage of bike-sharing users?  
3. How does the season affect the percentage of bike-sharing users?  
4. At what time is the number of bike rentals the highest?

## Data Analysis Pipeline
1. *Data Collection*: Used bike-sharing dataset from 2011 to 2012.
2. *Data Cleaning*: Fixed data type mismatches and renamed columns.
3. *Exploratory Data Analysis (EDA)*: Explored days_df and hours_df.
4. *Visualization*: Created line, bar, and pie charts to show trends by year, user type, season, weather, and hourly usage.
