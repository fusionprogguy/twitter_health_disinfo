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

### Twitter List

The current code allows you to scrape data from your own list. You supply your username and the name of the twitter list that you own. For example if your twitter handle is @FusionProgGuy, and your list is called 'Health', then your code would be as follows:

```
# which Twitter list and who owns it
twitter_user = 'fusionprogguy'  # 'fusionprogguy'
twitter_health_list = 'Health'  # 'Education'
```

When added your own account details, in the python file, the code should run without error. 


### Keyword Lists

The program requires three csv files with keywords:

1. claim_keywords.csv

2. medical_keywords.csv

3. nutrition_keywords.csv


Popular keywords in the files are:

1. Claims: research, healthy, proves, unlikely, better, data, review, because, evidence, must, never, cause, creates ...

2. Medical: covid19, healthy, coronavirus, patients, pandemic, cancer, disease, vaccine, heart, medical, diabetes, medicine, clinical ...

3. Nutritional: health, food, nutrition, diet, eating, exercise, weight, eat, foods, obesity, protein, fat, sugar, diets, dietary, plantbased, meat ...


You can use your own keyword lists if you wish. The files simply have one column with keywords in them. 



The claims file is likely going to be the most useful for any project in which you are seeking to find people making claims about the subject matter you are interested in.

For example:

"Sugar causes cancer" should be picked up as a claim ("causes") about medicine ("cancer") and nutrition ("sugar").

Whereas the tweets:

"Chicken Sweet Potato and Butternut Squash Hash Recipe" has no claim although it contains keywords about nutrition. 

"Mitochondria and stress + <link>" has a medical keyword ("Mitochondria") and one I've assigned to nutrition ("stress"), but there is no claim. 


Of course these filters are very basic because there is no appreciation of sentence structure and there are likely to be false negatives, but in my case, with 1400 users, and up to 200 tweets being retrieved for each, the number of tweets revieved can be over 100,000 tweets without strong filters. 


This tweet is currently a false negative claim:

"The pandemic is giving people what they want - flexible working"

It has a claim "is giving people what they want", but there is no keyword for this, so it is not recognised as a claim. 


All of the keyword lists can be improved, but it takes time to find words which may be missing. The best way to improve them is to check the tweets to see if they wrongly trigger as False when you believe they should be included. 


### Polarity and Sentiment

The fields for Polarity and Sentiment are calculated using the TextBlob library. 
https://textblob.readthedocs.io/en/dev/quickstart.html

Polarity is a number between -1 and +1, where a large negative number indicates a negative feeling and a large positive number indicates a positive feeling. 
Sentiment is a number between 0 and 1, where a small number means more objective and a higher number means more subjective.

Both word lists are fairly crude and limited - for instance a negation is not recognised properly. "Not the best" might be intereted as "best", for instance. I extracted a few claim words to illustrate polarity and sentiment. 

|--------------+--------------+-------------|
|     word     |   polarity   |  sentiment  |
|--------------+--------------+-------------|
| worst        |           -1 |           1 |
| insane       |           -1 |           1 |
| shocking     |           -1 |           1 |
| outrageous   |           -1 |           1 |
| useless      |         -0.5 |         0.2 |
| fail         |         -0.5 |         0.3 |
| vulnerable   |         -0.5 |         0.5 |
| random       |         -0.5 |         0.5 |
| unlikely     |         -0.5 |         0.5 |
| flawed       |         -0.5 |         0.5 |
| skeptical    |         -0.5 |         0.5 |
| expensive    |         -0.5 |         0.7 |
| corrupt      |         -0.5 |           1 |
| complicated  |         -0.5 |           1 |
| guilty       |         -0.5 |           1 |
| questionable |         -0.5 |           1 |
| few          |         -0.2 |         0.1 |
| less         | -0.166666667 | 0.066666667 |
| remarkable   |         0.75 |        0.75 |
| successful   |         0.75 |        0.95 |
| greatly      |          0.8 |        0.75 |
| incredible   |          0.9 |         0.9 |
| the best     |            1 |         0.3 |
| perfect      |            1 |           1 |


## Output

The program produces multiple csv file as well as some png files.


### Csv files and headers

1. 'health_tweets-Health-<Date_time>.csv' contains all the tweets that could be retrieved.
2. 'health_user_info-Health-<Date_time>.csv' contains a summary of each of the users in the list.
3. 'word_freq-Health-<Date_time>.csv' contains the counts of the words which match the keywords.


The health_tweets file has the headings:
claim, medical, nutrition, polarity, subjectivity, name, qualification, date, tweet

Here is a sample of what you might see in the table. 

| claim | medical | nutrition | polarity | subjectivity | name                     | qualification | date     | tweet                                                                                                                                                                                                                                                                                                                | flu | covid | both |
|-------|---------|-----------|----------|--------------|--------------------------|---------------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----|-------|------|
| TRUE  | TRUE    | TRUE      | 0.075    | 0.645833     | Avi Bitterman, MD        | MD            | ######## | The Ornish MPI study doesnt show statistically   significant improvement in blood flow in the experimental group The results   are only statistically significant because the control group got   substantially worse Its the same problem as EVAPORATE trial This is NOT   reversal                                 | 0   | 0     | 0    |
| TRUE  | TRUE    | FALSE     | 0.068182 | 0.352273     | Julia Marcus, PhD, MPH   | MPH, PhD      | ######## | SARSCoV2 transmission risk is not equally   distributed and policies should be designed accordingly Thread on our new   paper https://t.co/dz7qhBbhlG                                                                                                                                                                | 0   | 0     | 0    |
| TRUE  | TRUE    | TRUE      | 0.055556 | 0.200397     | Dawna Mughal PhD RDN     | PhD, RDN      | ######## | Sarcopenia and physical independence in older   adults the independent and synergic role of muscle mass and muscle function   https://t.co/Hi5Rn4CyPO                                                                                                                                                                | 0   | 0     | 0    |
| TRUE  | TRUE    | TRUE      | 0.166667 | 0.308333     | Alex Leaf                |               | ######## | Yes Type 2 diabetes is the apex of insulin   resistance which is most often caused by surpassing ones personal fat   threshold Blood sugar and insulin levels would be lower but insulin   resistance would be the same https://t.co/LPSQxcyffU                                                                      | 0   | 0     | 0    |
| TRUE  | TRUE    | TRUE      | 0.170833 | 0.554167     | Alex Leaf                |               | ######## | The only logical explanation is that eliminating   spices made food less palatable and therefore caused a spontaneous reduction   of food intake https://t.co/iZAK2LBA2N                                                                                                                                             | 0   | 0     | 0    |
| TRUE  | TRUE    | TRUE      | 0        | 1            | Koushik Reddy, MD, FACLM | FACLM, MD     | ######## | Effect of icosapent ethyl on progression of   coronary atherosclerosis in patients with elevated triglycerides on statin   therapy final results of the EVAPORATE trial https://t.co/BtVghjFkHu                                                                                                                      | 0   | 0     | 0    |
| TRUE  | TRUE    | TRUE      | 0.166667 | 0.333333     | Clemens ZsÃ³fia, PhD     | PhD           | ######## | Did you know that vitamin D deficiency is more   prevalent in Southern Europe than in Nothern Europe Vitamin D deficiency is   on the rise in Africa Not enough sun https://t.co/aovrvEH2Ig                                                                                                                          | 0   | 0     | 0    |
| TRUE  | TRUE    | FALSE     | 0        | 0            | BBC Health News          |               | ######## | Coronavirus immunity Can you catch it twice   https://t.co/Z3s39vla46                                                                                                                                                                                                                                                | 0   | 0     | 0    |




The health_user file has the headings:
name, clean_name, screen_name	gender, qualification, bio, polarity, sentiment, followers_count, following_count, Status:Followers, Follower:Following	acct_created, location, status_count, user_url, count_retrieved, count_RT, count_claim, count_medical, count_nutrition

Here is a sample user details that you might see in the table. 

| name                 | clean_name        | screen_name    | gender  | qualification | bio                                                                                                                                                    | polarity   | sentiment  | followers_count | following_count | Status:Followers | Follower:Following | acct_created | location                | status_count | user_url                | count_retrieved | count_RT | count_claim | count_medical | count_nutrition |
|----------------------|-------------------|----------------|---------|---------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|------------|------------|-----------------|-----------------|------------------|--------------------|--------------|-------------------------|--------------|-------------------------|-----------------|----------|-------------|---------------|-----------------|
| Health Nerd          | Health Nerd       | GidMK          | unknown |               | Epidemiologist Blogger Writer Guardian Observer etc PhDing at   @UoW Host of @senscipod Email gidmkhealthnerd@gmailcom he/him                          | 0.10416667 | 0.42       | 21540           | 1276            | 2.41917363       | 16.8808777         | 13/11/2015   | Sydney, New South Wales | 52109        | https://t.co/onN0CN3Iw4 | 47              | 29       | 107         | 42            | 16              |
| Danielle Belardo, MD | Danielle Belardo  | DBelardoMD     | female  | MD            | Director of Cardiology at IOPBM  CoDirector of Research & Education   @learnwithiopbm preventionfirst                                                  | 0          | 0.36666667 | 34563           | 2533            | 0.23409426       | 13.6450849         | 13/05/2018   | Newport Beach, CA       | 8091         | https://t.co/qC3BWlXffQ | 95              | 83       | 116         | 77            | 39              |
| Alex Leaf            | Alex Leaf         | AlexJLeaf      | male    |               | Scholar of nutrition researcher writer INTJ                                                                                                            | 0.09166667 | 0.46       | 1326            | 74              | 1.14404223       | 17.9189189         | 26/12/2018   | Scottsdale, AZ          | 1517         | https://t.co/3g8hroYniE | 42              | 17       | 143         | 46            | 77              |
| Nick Hiebert         | Nick Hiebert      | The_Nutrivore  | male    |               | Creator of the Nutrient Density Cheat Sheet                                                                                                            | 0.025      | 0.38125    | 1888            | 175             | 11.5497881       | 10.7885714         | 13/04/2017   | Manitoba, Canada        | 21806        | https://t.co/UbrOPJENII | 21              | 7        | 64          | 15            | 26              |
| Ivor Cummins         | Ivor Cummins      | FatEmperor     | male    |               | Technical Manager / Team Leader Biochemical Engineer Complex   Problem Solving Specialist Technologist Biochemistry Nutrition LCHF CAC CVD   RootCause | 0          | 0.33863636 | 89550           | 10903           | 0.84014517       | 8.21333578         | 11/03/2014   | Ireland                 | 75235        | http://t.co/tVfArmbN3L  | 153             | 126      | 200         | 62            | 15              |
| Nina Teicholz        | Nina Teicholz     | bigfatsurprise | female  |               | Science journalist author of The Big Fat Surprise advocate for   nutrition policy based on rigorous science mom                                        | 0.00331439 | 0.39166667 | 93685           | 1132            | 0.20616961       | 82.7606007         | 5/02/2014    | NYC                     | 19315        | https://t.co/cNnWOtVZEB | 68              | 28       | 222         | 69            | 126             |
| Stephan Guyenet, PhD | Stephan Guyenet   | whsource       | male    | PhD           | The neuroscience of eating behavior and obesity  Author of The Hungry Brain  Founder and director of Red Pen Reviews                                   | 0.09345238 | 0.53624339 | 37788           | 196             | 0.3227215        | 192.795918         | 11/04/2011   | Seattle, WA             | 12195        | https://t.co/8xY8Ra4CYm | 32              | 10       | 97          | 56            | 32              |
| Dr. Rhonda Patrick   | Rhonda Patrick    | foundmyfitness | female  | Dr.           | Im a PhD in biomedical science/expert on nutritional health   brain & aging http://t.co/VdqjL1RpZE                                                     | 0.13636364 | 0.45454546 | 328608          | 157             | 0.02392212       | 2093.04459         | 18/08/2009   |                         | 7861         | http://t.co/r3kuO77157  | 114             | 6        | 458         | 469           | 275             |
| Timothy Caulfield    | Timothy Caulfield | CaulfieldTim   | male    |               | Professor of health law & science policy speaker TV host   & author of the forthcoming book Relax Dammit Instagram @CaulfieldTim   GoScience           | 0          | 0.2        | 60927           | 2946            | 1.05458992       | 20.6812627         | 8/11/2011    | Edmonton Canada         | 64253        | https://t.co/HaxLtmuETK | 144             | 52       | 263         | 137           | 78              |



The word_freq file has the headings:
Word, freq, list1, list2, list3

Here is a sample of the top word frequencies that you might see in the table. 

| Word        | freq  | list1     | list2      | list3      |
|-------------|-------|-----------|------------|------------|
| covid19     | 10545 | medical   |            |            |
| health      | 9881  | nutrition |            |            |
| food        | 5286  | nutrition |            |            |
| research    | 4447  | claim     |            |            |
| nutrition   | 4111  | nutrition |            |            |
| diet        | 3011  | claim     |  nutrition |            |
| healthy     | 2827  | claim     |  medical   |  nutrition |
| coronavirus | 2796  | medical   |            |            |



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
