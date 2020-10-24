# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 14:06:07 2020

@author: RussellP
"""
import pandas as pd
 
df = pd.read_csv('glassdoor_jobs.csv')

# Salary Parsing

# Remove rating from Comapny Name Field

# Parse state and city into 2 different columns (variables)

# Change the founded variable to age of company

# Parsing of Job Description (Python, Years Exp)


# SALARY PARSING
# Remove any values that do not have a valid salary (They are currently set -1)
df = df[df['Salary Estimate'] != '-1']

# Removing 'Glassdor Est.' text from Salary Estimate fields
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])

# Removing the 'k' and '$' from the Salary Estimate range
removed_k = salary.apply(lambda x: x.replace('k', '').replace('$', ''))

# Create Column for Per Hour and Employer Provided Salary in the case there is per hour or employer provided salaries
df['Hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)  # use this type of method to parse out per hour also)

# Get the min salary for the salary estimate range and convert to int
df['min_salary'] = removed_k.apply(lambda x: int(x.split('-')[0]))

# Get the max salary for the salary estimate range and convert to int
df['max_salary'] = removed_k.apply(lambda x: int(x.split('-')[1]))

# Get the average of the min and max salary
df['avg_salary'] = (df.min_salary + df.max_salary)/2

# COMPANY NAME PARSING
# Remove the rating
df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis = 1)

# LOCATION PARSING
# Creating state field
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])

# Check if the job is in the same place as the HQ (NOTE: The scraper currently doesn't pull in the headquarters values, will fix soon)
df['same_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis = 1)


# Check how many jobs are in each state (Note: our data is currently only from San Francisco)
# df.job_state.value_counts()

# FOUNDED PARSING
# Changing it to age of company
df['age'] = df['Founded'].apply(lambda x: x if x < 1 else 2020 - x)

# JOB DESCRIPTION PARSING
# Python
df['python'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)

# SQL
df['sql'] = df['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)

# Excel
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)

# Apache Spark
df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)

# AWS
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)

# 2 Years of experience (This parsing will be improved next iteration)
df['experience_2years'] = df['Job Description'].apply(lambda x: 1 if '2 years' in x.lower() else 0)

df.to_csv('salary_data_cleaned.csv', index = False)

pd.read_csv('salary_data_cleaned.csv')















