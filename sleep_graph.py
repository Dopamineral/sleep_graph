# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 13:14:24 2019

@author: Robert
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
import datetime
import matplotlib.pyplot as plt
import numpy as np

def goto_page(url):
	"""Navigates to given url, url must be string""" 
	driver.get(url)
    
def sign_in(url):
    """Prompts user to sign in, waits 30s"""
    driver.get(url)
    sleep(30)

#calculate rolling 7 day time average.
def rolling_average(n,data_list):
    """Calculates rolling average over n days in a sleep-wake time list"""
    output_list = []
    for i in range(len(timedt_sleep_list_h)):
        if i < n:
            average = np.nanmean(data_list[0:n-1])
        else:
            average = np.nanmean(data_list[i-n:i])
        output_list.append(average)
    return output_list
    

    
if __name__ == "__main__":
#-----------------------SIGN IN -----------------------------------------------    
    #use this to sign in into the garmin site, automatic sign in doesn't work yet
    driver = webdriver.Chrome("D:/programming/chromedriver.exe")
    url_sign_in = "https://connect.garmin.com/signin/"
    sign_in(url_sign_in)
    
    #before you continue, resize the window of the browser so its width is small 
    #enough for the side banner to disappear
#---------------------SCRAPE WEBSITE-------------------------------------------
    time_sleep_list = []
    time_wake_list = []
    
    #input date range that you want to graph (Year - Month - Day)
    date_start = ("2019-10-23")
    date_end = ("2019-11-16")
    
    #convert start and end to datetime to calculate days in between
    datetime_start = datetime.datetime.strptime(date_start,"%Y-%m-%d")
    datetime_end = datetime.datetime.strptime(date_end,"%Y-%m-%d")
    delta = (datetime_end - datetime_start).days

    url_list = []
    date_list = [] # Will use this later for the plot

    for i in range(delta+1):
        #Create list urls to scrape over to get the sleep and wake times
        new_date = datetime_start + datetime.timedelta(days=i)
        url_date = datetime.datetime.strftime(new_date,"%Y-%m-%d")
        url = "https://connect.garmin.com/modern/sleep/{}".format(url_date)
        url_list.append(url)
        date_list.append(url_date)
        
    
    for url in url_list:
        #scrape over urls
        goto_page(url)
        timeout_delay = 5 # delay (s) until timeout error is raised
        try:
            #waits until it can find the sleep time element on the page
            myElem = WebDriverWait(driver, timeout_delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/div/div[3]/div/div[2]/div/div/div[3]/div[1]/div/div/div/div[1]')))
        except TimeoutException:
            print("Loading took too much time! Possibly no data on this day")
        
        try:
            time_sleep = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div[3]/div/div[2]/div/div/div[3]/div[1]/div/div/div/div[1]').text
            time_wake =  driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div[3]/div/div[2]/div/div/div[3]/div[2]/div/div/div/div[1]').text
            time_sleep_list.append(time_sleep)
            time_wake_list.append(time_wake)
        
        except:
            time_sleep = ""
            time_wake = ""
            time_sleep_list.append(time_sleep)
            time_wake_list.append(time_wake)
            
#-----------------------DATA CONVERSION ---------------------------------------
    #changing time to datetime format
    timedt_sleep_list = []
    timedt_wake_list = []
    for i in range(len(time_sleep_list)): 
        try:
            timedt_sleep = datetime.datetime.strptime(time_sleep_list[i], "%I:%M %p").time()
            print(timedt_sleep)
            timedt_wake = datetime.datetime.strptime(time_wake_list[i], "%I:%M %p").time()
            print(timedt_wake)
            timedt_sleep_list.append(timedt_sleep)
            timedt_wake_list.append(timedt_wake)
        except:
            #In case of missing data
            timedt_sleep_list.append(np.nan)
            timedt_wake_list.append(np.nan)
    #Convert data to positive and negative seconds to fix the midnight horror
    timedt_sleep_list_s = []
    for time in timedt_sleep_list:
        try:
            time_delta = datetime.timedelta(hours= time.hour, minutes = time.minute, seconds = time.second)
            time_delta_s = time_delta.seconds
            #Assumption, I'll never go to bed before 18:00, else change the below
            if time > datetime.time(18,0,0):
                time_delta_s = time_delta_s - (24*60*60)
            timedt_sleep_list_s.append(time_delta_s)
        except:
            #In case of NaNs
            timedt_sleep_list_s.append(time)
            
       
    timedt_wake_list_s = []
    for time in timedt_wake_list:
        try:
            time_delta = datetime.timedelta(hours= time.hour, minutes = time.minute, seconds = time.second)
            time_delta_s = time_delta.seconds
            timedt_wake_list_s.append(time_delta_s)
        except:
            #In case of NaNs
            timedt_wake_list_s.append(time)
            
        
    #convert seconds to hours (float value)
    timedt_sleep_list_h = [x / (60*60) for x in timedt_sleep_list_s]
    timedt_wake_list_h = [x / (60*60) for x in timedt_wake_list_s]
        
    #calculating general means for data
    mean_wake = np.nanmean(timedt_wake_list_h) 
    mean_sleep = np.nanmean(timedt_sleep_list_h)
    
    
#--------------------PLOT DATA ------------------------------------------------
    fig = plt.figure(figsize = (10,0.4*len(timedt_sleep_list_h))) #Will chang ethe Y size of the graph based on the amount of data
    sleep_lines= plt.hlines(xmin = timedt_sleep_list_h, # Plots bar during sleep
               xmax = timedt_wake_list_h, 
               y = [x for x in range(len(timedt_sleep_list_h))],
               color="dodgerblue", linewidth=18)
    sleep_average, = plt.plot(rolling_average(5,timedt_sleep_list_h), # Plots rolling average of sleep time over n days, n = 5
             [x for x in range(len(timedt_sleep_list_h))],
             color="navy")
    wake_average, = plt.plot(rolling_average(5,timedt_wake_list_h), # Plots rolling average of wake time over n days, n = 5
             [x for x in range(len(timedt_sleep_list_h))],
             color="navy")
    plt.grid(axis='x') # Plots grid corresponding to hours

    plt.locator_params(axis = 'x', # Shows tick for every hour
                       nbins =24)
    sleep_ideal = plt.vlines(x=0, #Plot ideal sleep hour = midnight
               ymin = 0,
               ymax = len(timedt_sleep_list_h)-1,
               color="red")
    wake_ideal = plt.vlines(x=7, # Plot ideal wake hour = 7:00
               ymin = 0,
               ymax = len(timedt_sleep_list_h)-1,
               color="red")
    plt.yticks(ticks = np.arange(len(timedt_sleep_list_h)), # Sets dates as Y_ticks
               labels = date_list)
    plt.ylim(len(timedt_sleep_list_h),-1)
    hour_labels = ["22:00",
                   "23:00",
                   "0:00",
                   "1:00",
                   "2:00",
                   "3:00",
                   "4:00",
                   "5:00",
                   "6:00",
                   "7:00",
                   "8:00",
                   "9:00",
                   "10:00",
                   "11:00",
                   "12:00"]
    plt.xticks(ticks = [-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12],
               labels = hour_labels,
               rotation=0 )
    plt.legend((sleep_lines,sleep_ideal, sleep_average, wake_ideal,wake_average),
               ('sleep','ideal sleep: 00:00','average sleep (5 days)','ideal wake: 7:00','average wake (5 days)'))
    plt.title("SLEEP GRAPH - Based on Garmin tracking")
