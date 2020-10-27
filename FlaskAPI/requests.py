# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 12:20:47 2020

@author: RussellP
"""

import requests
from data_input import data_in

# Endpoint URL
URL = 'http://127.0.0.1:5000/predict'

# Structuring our request
headers ={"Content-Type": "application/json"}
data = {"input": data_in}

r = requests.get(URL, headers = headers, json = data)



# Run this line separate to the above request code
r.json()
