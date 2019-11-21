# sleep_graph

Scrapes sleep data (sleep time and wake time) from Garmin website and graphs them as seen below:
![sleep graph example](https://github.com/Dopamineral/sleep_graph/blob/master/example.png)


Updated it to color weekends and weekdays and also added weekdays to the y-axis
![sleep graph example with colour and weekdays](https://github.com/Dopamineral/sleep_graph/blob/master/example_colour_days.png)

## Step 0: This works best in the anaconda - spyder setup but good luck to however you want to use it
anaconda python datascience package thing can be found here: https://www.anaconda.com/

## Step 1: Run: "SIGN IN" portion of the code and then log into your garmin account manually.
Automatic login is not implemented yet and might actually be preferable, user-safety wise. Once the selenium web driver is active the rest of the code will execute fine. When you're logged in it will be able to scrape the dates based on the urls that fit each day.

## Step 2: Resize the chromium driver window until the width is as small as possible. 
The XPATH to the data will change if the sidemenu is showing and you will scrape a whole bunch of NaNs. So resize it so it has the width of a mobile website.

## Step 3: Run: rest of the script
#### SCRAPE WEBSITE
Gets the data from the garmin website
#### DATA CONVERSION
Converts the "strings" from the site to datetime objects and then some further juggling to fix the horrible before midnight after midnight plotting isses
#### PLOT DATA 
Makes a fancy plot of the data, plot scales in the Y direction based on the amount of datapoints given

## Possible use
Sport watches and smart watches are starting to come down quite a bit in price. It's reaching the level where the average joe can afford one without having to sell any kidneys (mine was 200 euro). I'm super impressed by the sleep tracking abilities of the current garmin watch that I have. Simply by wearing the watch it will predict what kind of activity you're doing and also when you're awake and when you're asleep. With some fancy heart rate variability measures they also claim to be able to quantify different sleep stages but I haven't used any of that data here.

Quantifying bed-time and wake time with very very very minimal effort on the "patient side" is amazing for individual follow up of sleep. I remember having to write down sleep and wake times by memory and it was just a drudgy slob, and even more so when you didn't do your homework for a couple of days. Follow up of problems with sleep onset was one of my interests in writing this program. 

At the moment the source of the data is really just the sleep time and wake time, due to constraints of what's easily accessible on the garmin website. So for conditions where theres a lot of wake time during the night this might not give an accurate representation of someone's sleep. In the future a different source of data, possibly .FIT files could solve this. 

Ideas for further applications would be to test how well one can predict delay of sleep onset based on wake time, average wake time, average sleep time, etc... Where there's data there's room for magic! 


