#!/usr/bin/env python3

import json
import locale
import os
from os import name
import sys


def load_data(filename):
  """Loads the contents of filename as a JSON file."""
  with open(filename) as json_file:
    data = json.load(json_file)
  return data


def format_car(car):
  """Given a car dictionary, returns a nicely formatted name."""
  return "{} {} ({})".format(
      car["car_make"], car["car_model"], car["car_year"])


def process_data(data):
  """Analyzes the data, looking for maximums.

  Returns a list of lines that summarize the information.
  """
  max_revenue = {"revenue": 0}
  max_sales = {"total_sales":0}
  years ={}
  for item in data:
    # Calculate the revenue generated by this model (price * total_sales)
    # We need to convert the price from "$1234.56" to 1234.56
    item_price = locale.atof(item["price"].strip("$"))
    item_revenue = item["total_sales"] * item_price
    if item_revenue > max_revenue["revenue"]:
      item["revenue"] = item_revenue
      max_revenue = item
    
    # also handle max sales
    item_sales = item["total_sales"]
    if item_sales > max_sales["total_sales"]:
      max_sales= item
    
    # also handle most popular car_year
    year=item["car"]["car_year"]
    if year not in years:
      years[year]= item["total_sales"]
    else:
      years[year]+= item["total_sales"]
  
  # Assemble the calculated data into a summary  
  popular_year=(sorted(years.items(), key = lambda kv:(kv[1], kv[0])))
  popular_year=popular_year[0]
  line1= "The {} generated the most revenue: {}".format(format_car(max_revenue["car"]),max_revenue["revenue"]) 
  line2= "The {} had the most sales: {}".format(format_car(max_sales["car"]),max_sales["total_sales"]) 
  line3= "The most popular year was {} with {} sales.".format(popular_year[0],popular_year[1]) 
  pdf_lines=[line1,line2,line3]
  pdf_lines="<br/>".join(pdf_lines)
  return pdf_lines

# Create PDF
  import reports
  reports.generate("/tmp/cars.pdf", "Sales summary for last month", pdf_lines, data)
  

# Send email
  import emails
  receiver = "{}@example.com".format(os.environ.get('USER'))
  message = emails.generate("automation@example.com", receiver, "Sales summary for last month", pdf_lines, "/tmp/cars.pdf")
  emails.send(message)
  




data=load_data("car_sales.json")
process_data(data)


            
