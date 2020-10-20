import pandas as pd
import glassdoor_scraper as gs

path =  "C:/Users/RussellP/Documents/Data Engineering Projects/salary_estimator_project/chromedriver"

# Parameters are Job Title, Number of Jobs,
df = s2.get_jobs('data engineer', 1000, False, path, 3)

# Convert from DataFrame to CSV
df.to_csv('glassdoor_jobs.csv', index=False)


