# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 20:23:17 2023

@author: Giancarlo
"""

# Importing libraries
from bs4 import BeautifulSoup
import requests
from time import sleep
import csv
import json

# Retrieving an parsing first page
url = "https://www.myhome.ie/estate-agents/page-1"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Finding the maximum page number
maxpage = soup.find('ul', class_ = 'ngx-pagination ng-star-inserted').find_all('a')[-2].text.split()[-1]
maxpage = int(maxpage) 

# Getting the data for the agents
agents_list = list()
for page in range(maxpage+1):
    
    url = "https://www.myhome.ie/estate-agents/page-{}".format(page)
    response = requests.get(url)
    if response.status_code != 200:
        print('Error, response status',response.status_code)
        break
    soup = BeautifulSoup(response.content, "html.parser")
    
    agent_data = soup.find_all("div", class_ = "agents-search__details")
    
    print('Scraping page',page)
    for item in agent_data:
        try:
            name = item.find("div", class_= "agents-search__name").text
        except:
            print('Could not retrieve name')
            name = None
            continue
        try:
            address = item.find("div", class_= "agents-search__address").text
        except:
            print('Address not found for',name)
            address = None
        try:
            phone = item.find_all("div", class_= "agents-search__text d-flex align-items-center ng-star-inserted")[0].text.replace(' ','').replace('-','')
        except:
            phone = None
            print('Phone number not found for',name)
        try:
            license = item.find_all("div", class_= "agents-search__text d-flex align-items-center ng-star-inserted")[1].text
            license = license.strip().split(' ')[-1]
            license.replace('.','')
        except:
            license = None
            print('License number not found for',name)
    
        agents_list.append({'Name' : name, 'Address' : address, 'Phone' : phone, 'License' : license})
        print('Retrieved',len(agents_list),'agents...')
    sleep(3)
print('Done')

# Saving Data
# As csv
field_names = ['Name', 'Address', 'Phone', 'License']
with open('Agents.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(agents_list)
# As JSON
json_object = json.dumps(agents_list, indent=4)
with open("Agents.json", "w") as outfile:
    outfile.write(json_object)