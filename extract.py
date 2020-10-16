import glassdoor_scraper as gs
import pandas as pd

path =  "C:/Users/RussellP/Documents/Data Engineering Projects/salary_estimator_project/chromedriver"

# Parameters are Job Title, Number of Jobs,
df = gs.get_jobs('data engineer', 5, False, path, 1)

print(df.head)

