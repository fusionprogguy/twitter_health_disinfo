# README

## Table of contents


## General info
This project collects tweets about health and medicine from the users in a twitter list that you own. The way this tool is intended to be used is to help identify health influencers who are spreading health misinformation on twitter. 

You need to have a twitter account and apply for a developer account. 


## Technologies
Project is created with Python 3.8

To download Python go to
https://www.python.org/downloads/

	
## Setup

### Signup for Developer Account

You can sign up for a developer account here to use the Twitter API to retrieve tweets.
https://developer.twitter.com/en/apply-for-access

Check your email for from 'developer-accounts@twitter.com' or similar email and follow their instructions. They will send you an application form and may also ask for further clarification on the purpose of your request. Expect a few follow up emails back and forth before they give you an account. I believe they want to prevent people misusing twitter for bots or denial of service attacks so they want to know exactly who will be using the information and what format your information will be in, and who it will be shared with. 

### Authentication Keys

To set up your authentication keys with Python, check the following articles
https://python-twitter.readthedocs.io/en/latest/getting_started.html
https://www.digitalocean.com/community/tutorials/how-to-authenticate-a-python-application-with-twitter-using-tweepy-on-ubuntu-14-04

If you are using the code for private use, in the python code you can put in your keys where it says "xxxx". You may want to use more advanced methods
of keyword storage if you want other people to use your code or to create a Twitter app or bot. 

```
# Obtain your twitter developer account and enter your secret keys to access the API
consumer_key = "xxxx"
consumer_secret = "xxxx"
access_token = "xxxx"
access_token_secret = "xxxx"
```

### Installation of Libraries

Assuming you have Python up and running, you may need to install a few libraries, if you have not installed them already for other projects. 

```
import tweepy
import TextBlob
import pandas
import csv
import gender_guesser
import Counter
import datetime
import re
import traceback
import warnings
import statistics
import matplotlib.pyplot
```

If you are not sure which ones you need to install, just run the program and the error messages will tell you which libraries you are missing. 

### Run TwitterUserName.py

To run this project, open up TwitterUserName.py in your favourite Python interepreter and run it.

If you are using the command prompt in windows press the windows key + R and type cmd and then press enter.

Navigate to your folder with the file eg "cd C:\folder"


Then type in "python TwitterUserName.py"

```
python TwitterUserName.py
```


### Keyword Lists

The program requires three csv files with keywords:

1. claim_keywords.csv

2. medical_keywords.csv

3. nutrition_keywords.csv


Popular keywords in the files are:

1. Claims: research, healthy, support, better, data, review, because, evidence, must, never ...

2. Medical: covid19, healthy, coronavirus, patients, pandemic, cancer, disease, vaccine, heart, medical, diabetes, medicine, clinical ...

3. Nutritional: health, food, nutrition, diet, eating, exercise, weight, eat, foods, obesity, protein, fat, sugar, diets, dietary, plantbased, meat ...


You can use your own keyword lists if you wish. The files simply have one column with keywords in them. 


## Output

The program produces multiple csv file as well as some png files. 

### Csv files and headers

1. 'health_tweets-Health-<Date_time>.csv' contains all the tweets that could be retrieved.
2. 'health_user_info-Health-<Date_time>.csv' contains a summary of each of the users in the list.
3. 'word_freq-Health-<Date_time>.csv' contains the counts of the words which match the keywords.


The health_tweets file has the headings:
claim,medical, nutrition, polarity, subjectivity, name, qualification, date, tweet


The health_user file has the headings:
name, clean_name, screen_name	gender, qualification, bio, polarity, sentiment, followers_count, following_count, Status:Followers, Follower:Following	acct_created, location, status_count, user_url, count_retrieved, count_RT, count_claim, count_medical, count_nutrition


The word_freq file has the headings:
Word, freq, list1, list2, list3


### Filters 

The two main filters I use are to reduce the number of rows produced and to select the most useful tweets which always have a claim and a medical or nutrition keyword.

The first filter is to select the most prominent health influencers who have more than 1000 followers and status updates (tweets). The current project is focused on examining the claims by the biggest influencers so it may be better to increase these figures if you want to reduce the data produced. 

```
    # Set limits on health influencer to filter the most popular and most active
    if followers_count > 1000 and status_count > 1000:
```

The second filter is for statistical purposes, so that we have enough tweets per person to have meaningful calculations such as ratios, sentiment or polarity. 

An example of who might be filtered out is someone like @MictheVegan who only has 8 total tweets. With such few tweets, the calculations may present a rather negative picture of him in terms of sentiment, since a few of his tweets from 2016 appear quite negative. The tone in his youtube videos are much more upbeat and positive, so it may give a false impression of him. 


```
    # Set the minimum number of tweets you'll allow for each person. Make sure there is always a claim, and then a medical or nutrition keyword.
    
    if count_retrieved > 9 and count_claim > 0 and (count_medical + count_nutrition) > 0:
```

Currently for testing I am saving all the tweets, but once you are happy with the keywords you can uncomment the if-clause. 

```
# if bool_claim and (bool_medical or bool_nutrition):
if True:
  ...
  c_tweets.writerow(row)
```

### PNG files

The images are based on the data collected and plotted as a scatterplot in 2D with a x-axis and a y-axis. These images are produced in pairs, with the x data coming from the columns in x_axis and the y data coming from the columns in y_axis.

x_axis = ['status_count', 'count_nutrition', 'count_claim', 'count_claim', 'count_retrieved', 'count_retrieved', 'sentiment', 'followers_count']
y_axis = ['followers_count', 'count_medical', 'count_nutrition', 'count_medical', 'count_claim', 'count_RT', 'polarity', 'following_count']

The plot file names are produced automatically from the column names

```
    plot_name = (str(x) + ' ' + str(y)).replace(':', '_')
    plt.savefig(plot_name + '.png')
```

## Licensing

GNU General Public License v3.0
“GPL version 3 or any later version”

https://www.gnu.org/licenses/gpl-3.0.html
https://www.gnu.org/licenses/gpl-3.0.md
 


## Donations

Donations are welcome. [Please use this paypal account.](https://www.paypal.com/paypalme/StevenMorello)
