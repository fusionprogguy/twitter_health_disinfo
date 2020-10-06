# import the modules
import tweepy
from textblob import TextBlob
import pandas as pd
import csv
import gender_guesser.detector as gender
from collections import Counter, defaultdict
import datetime
import re
import traceback
import warnings
import statistics
import matplotlib.pyplot as plt

# Obtain your twitter developer account and enter your secret keys to access the API
consumer_key = "xxxx"
consumer_secret = "xxxx"
access_token = "xxxx"
access_token_secret = "xxxx"

# which Twitter list and who owns it
twitter_user = 'fusionprogguy'         # Your Twitter username goes here eg '@fusionprogguy' -> 'fusionprogguy'
twitter_health_list = 'Health-Quacks'  # List names with spaces get dashes 'Health Quacks' - > 'Health-Quacks'

limit_users = 1500         # Maximum number of users to check
number_of_tweets = 200     # Tweet limit. Default is 200

# authorization of consumer key and consumer secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

# set access to user's access key and access secret
auth.set_access_token(access_token, access_token_secret)

# calling the api
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)  # wait_on_rate_limit=True, wait_on_rate_limit_notify=True

remove_titles = ['(', ')', 'she/her', 'he/him', 'they/them', 'AdvAPD', 'AEP', 'APD', 'CDE', 'CFS', 'CLT', 'CNSC', 'CSCS', 'CSSD', 'Dr.', 'Dr', 'DR', 'Doctor',
                 'DPT', 'FAAOS', 'FACC', 'FAAP', 'FACLM', 'FACP', 'FACSM', 'FAIDH', 'FAMS', 'FAND', 'FASA', 'JD', 'LDN', 'LD',
                 'M.D.', 'MD', 'MHS', 'MLIS', 'MPH', 'MSCE', 'MSc', 'MS', 'MTR',
                 'Ph.D.', 'PhD', 'Professor', 'Prof.', 'Prof', 'PT', 'RDN', 'RD', 'ScD', 'ScM', 'ER physician', 'Nutritionist', 'Dietician']

# These orgs are misidentified as being either male or female
orgs = ['Cleveland Clinic', 'Stanford Medicine', 'Weston A. Price Foundation', 'Mayo Clinic', 'WebMD', 'WebMD_Blogs', 'FDA Drug Information',
        'The BMJ', 'The Atlantic Health', 'The Lancet Global Health', 'The Nutrition Source',
        'The George Institute for Global Health', 'The TVA', 'The Health Sciences Academy', 'The Gut Foundation', 'The Conversation H+M', 'The Nutrition Consultant', 'The Microbiome Diet',
        'The Food Physio', 'Take That, Medicine!', 'CDC', 'WebMD', 'Harvard Health', 'BBC Health News', 'Gates Foundation', 'Family Health Guide', 'NIH', 'NYT Health', 'NPR Health News',
        'NBC News Health', 'HHS.gov', 'NEJM', 'AMA', 'TIME Health', 'WSJ Health News', 'Department of Health and Social Care', 'CBS News Health', 'L.A. Times Health', 'WebMD_Blogs', 'JAMA',
        'U.S. FDA', 'HarvardPublicHealth', 'American Heart Association', 'Reuters Health', 'Health', 'HuffPost Food', 'Medscape', 'Garmin', 'Kaiser Health News',
        'Muscular Development', 'Maye Musk', 'Health Affairs', 'Modern Healthcare', 'Sir Patrick Vallance', 'STAT', 'Nursing Times', 'Muscle & Performance', 'Cochrane',
        'European Society of Cardiology', 'Australian Government Department of Health', 'USDA Nutrition', 'American College of Cardiology', 'American Heart News', 'YLMSportScience',
        'NPRFood', 'NSCA', 'BJSM Community', 'JAMA Internal Medicine', 'NSW Health', 'Better Health', 'USDA Team Nutrition', 'MedPage Today', 'NASEM Health', 'Nutrition.gov', 'pharmalot',
        'Physicians Committee', 'AHA Science', 'PLOS Medicine', 'Cochrane UK', 'Annals of Int Med', 'BMJ', 'NHMRC', 'Cardiology Today', 'Precision Nutrition', 'Sport Australia',
        'SitemanCancerCenter', 'Heart_BMJ', 'American Journal of Sports Medicine', 'Healthline Nutrition', 'MedCity News', 'Weill Cornell Medicine', 'ScienceBasedMed', 'VicHealth',
        'CancerCouncilOz', 'BDA British Dietetic Association', 'ABC Life', 'AMA Media', 'Elsevier Cardiology', 'iMedicalApps.com', 'Examine.com', 'NIAAA News', 'Journal of Physiology',
        'Sustainable Harvard', 'Salk Institute', 'Australian Physiotherapy Association', 'CardioSmart', 'WHAT THE HEALTH', 'EAT', 'MJA', 'Nutrition Society', 'Imperial Medicine',
        'CJSM', 'ASCP', 'Gut Journal', 'Real Food Media', 'PhysiciansFirstWatch', 'LiveScienceHealth', 'Dietitians of Canada', 'Garvan Institute of Medical Research',
        'Cancer Council Victoria', 'Nutrition Australia', 'TalkingNutrition', 'SER', 'Exercise and Sport Sciences Reviews', 'National Rural Health Alliance', 'Food Matters Live',
        'American Society for Nutrition', 'WCRF International', 'MDLinx', 'Massachusetts Medical Society (MMS)', 'SciComm Hub', 'Medical Observer', 'Livable Future', 'Tufts Nutrition',
        'JAMA Network Open', 'Azmina Nutrition', 'Baker Institute', 'BMJ Evidence-Based Medicine', 'BMJ Global Health', 'National Lipid Association', 'Elsevier Nutrition',
        'Food Psych Podcast', 'SportsScienceMed', 'American Institute for Cancer Research', 'Sydney_Health', 'Dietitian Connection', 'StanfordHealthPolicy', 'JournalofPediatrics',
        'Science of Football', 'optimising nutrition', 'Deakin Nutrition', 'Champagne Nutrition', 'TrueHealthInitiative', 'SAGE Health & Nursing', 'American Society for Nutrition Journals',
        'Grains & Legumes Nutrition Council', 'SydneyCycleways', 'Kidney Health', 'BadScienceWatch', 'Health Watch', "Australian Women's Health Network", "Racial Health Equity",
        'Peppermint Wellness', 'Glycemic Index Foundation', 'Heart Foundation', 'VIS Nutrition', 'Healthy Weight Week', 'Heart Research Institute', 'Cancer Council Media',
        'AJHE', 'JMNI', 'BMJ Nutrition, Prevention & Health', 'Science of Nutrition', 'Simply Nutrition']

ignore_words = ['rt', '@', '$', '&', '/', '', '-', '―', 'im', "i'm", "i’m", "i’ve", "we’ve", "it's", "it’s", 'too', "don’t", "can’t", "they’re", "won’t", 'every', 'happy', 'two', 'talk', 'days', 'months', 'off', '&', '&amp', 'a', 'about', 'after', 'all', 'also', 'am', 'an', 'and', 'any', 'are', 'as', 'at', 'back', 'be', 'been',
                'being', 'best', 'between', 'boys', 'but', 'by', 'oh', 'can', 'car', 'cars', 'cat', 'cats', 'check', 'could', 'dad', 'day', 'did', 'do', 'does', 'dog', 'dogs', "don't", 'during', 'even', 'fan', 'find', 'first', 'for', 'former', 'free',
                'from', 'get', 'girls', 'go', 'going', 'good', 'great', 'had', 'has', 'have', 'he', 'help', 'her', 'here', 'high', 'his', 'home', 'how', 'husband', 'i', 'id', 'if', 'important', 'in', 'interested', 'into', 'is', 'it', 'its', 'join',
                'just', 'keep', 'kid', 'kids', 'know', 'last', 'latest', 'learn', 'like', 'live', 'look', 'looking', 'love', 'lover', 'made', 'make', 'many', 'may', 'me', 'mine', 'mom', 'more', 'most', 'mother', 'much', 'mum', 'music', 'my',
                'myself', 'need', 'new', 'next', 'no', 'not', 'now', 'of', 'often', 'ok', 'on', 'one', 'online', 'only', 'or', 'other', 'our', 'out', 'over', 'own', 'part', 'people', 'please', 'posted', 'read', 'really', 'right', 'risk', 'see', 'share',
                'she', 'should', 'so', 'some', 'still', 'study', 'take', 'team', 'than', 'thank', 'thanks', 'that', 'that', 'the', 'their', 'them', 'there', 'these', 'they', 'think', 'this', 'those', 'time', 'to', 'today', 'top' 'bad', 'up', 'us',
                'use', 'very', 'via', 'views', 'want', 'was', 'way', 'we', 'week', 'well', 'were', 'what', "what’s", 'when', 'where', 'which', 'who', 'why', 'wife', 'will', 'with', 'work', 'working', 'would', 'years', 'you', 'your']

special_symbols = ['(', ')', '"', '“', '”', "'", ',', '.', '!', '?', ';', '#', '=', '≠', '//', ':', '-', '—','―', '+', '|', '||', '•', '○', '*', ':)', '~', '…', '...', '\n']  # '//', ':', '@'

def clean(x):
    # Cleaning the tweets
    # Creating a function called clean. removing hyperlink, #, RT, @mentions
    x = re.sub(r"^RT[\s]+', '", x)
    x = re.sub(r"https?:\/\/.*[\r\n]*', '", x)
    x = re.sub(r"#', '", x)
    x = re.sub(r"@[A-Za-z0–9]+', '", x)
    return x

def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def remove_symbols(text, bool_remove_url):
    text = remove_emoji(text)
    left_text = ''
    extract_url = ''

    if bool_remove_url:
        # Remove urls
        text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)

        # Remove user @ references and '#' from tweet
        # text = re.sub(r'\@\w+|\#', '', text)
        for sym in special_symbols:
            # if 'https' not in text:
            text = text.replace(sym, ' ').strip()

        # print('T1', left_text + '***')
        return text

    else:
        if 'http' in text:
            test = re.search("(?P<url>https?://[^\s]+)", text)
            if test is not None:   # if there is a url, extract it
                extract_url = test.group("url").strip()
            left_text = text.split('http')[0].strip()
            # print('T2', left_text + '***')
        else:
            left_text = text.strip()
            # print('T3', left_text + '***')

        for sym in special_symbols:
            # if 'https' not in text:
            left_text = left_text.replace(sym, '')

        # print('T4', left_text + '***')
        return (left_text + ' ' + extract_url).strip()



wordDict = defaultdict(int)  # Dictionary is initilized with a zero

# health_list_members = api.list_members(twitter_user, twitter_health_list)  # user, list  # Only retrieves 20 people

print('Retrieving bios and tweets from', twitter_user, 'list:', twitter_health_list)

# You can set date limits if you wish
today = datetime.datetime.today()
date_time_string = today.strftime("%Y-%m-%d_%I-%M-%S_%p")

since_date = '2017-01-01'
until_date = today.strftime('%Y-%m-%d')
print("Today's date", until_date)
print()

# Load up word dictionaries
claim_words = []
medical_words = []
nutrition_words = []

with open('claim_keywords.csv', 'r', newline='') as f:
    for row in csv.reader(f):
        claim_words.append(row[0])

with open('medical_keywords.csv', 'r', newline='') as f:
    for row in csv.reader(f):
        medical_words.append(row[0])

with open('nutrition_keywords.csv', 'r', newline='') as f:
    for row in csv.reader(f):
        nutrition_words.append(row[0])

print('Word dictionary')
print('Claim words')
print(claim_words)
print('Medical words')
print(medical_words)
print('Nutritional words')
print(nutrition_words)

# health_list_members = tweepy.Cursor(api.list_members, twitter_user, twitter_health_list, since=since_date,until=until_date).items()
health_list_members = tweepy.Cursor(api.list_members, twitter_user, twitter_health_list).items()
d = gender.Detector()  # Guesses the gender based on first name

# print('Health people:', len(health_list_members))
print()

# Create bio csv file
bio_filename = "health_user_info-" + twitter_health_list + "-" + date_time_string + ".csv"
csvfile_bio = open(bio_filename, 'w', encoding="utf-8", newline='')
c_bio = csv.writer(csvfile_bio)

# write the header row for CSV file
bio_header = ['name', 'clean_name', 'screen_name', 'gender', 'qualification', 'bio', 'polarity', 'sentiment', 'followers_count', 'following_count', 'Status:Followers', 'Follower:Following', 'acct_created', 'location', 'status_count', 'user_url', 'count_retrieved', 'count_RT', 'count_claim', 'count_medical', 'count_nutrition']
print(bio_header)
c_bio.writerow(bio_header)

df = pd.DataFrame(columns=bio_header)

# Create tweet file
tweets_filename = "health_tweets-" + twitter_health_list + "-" + date_time_string + ".csv"
csvfile_tweets = open(tweets_filename, 'w', encoding="utf-8", newline='')
c_tweets = csv.writer(csvfile_tweets)

tweets_header = ['claim', 'medical', 'nutrition',  'claim_str', 'medi_str', 'nutri_str', 'polarity', 'subjectivity', 'name', 'qualification', 'date', 'tweet']   # 'tweet_id'
print(tweets_header)
c_tweets.writerow(tweets_header)


male_polarity = []
female_polarity = []
org_polarity = []
unknown_polarity = []

male_sentiment = []
female_sentiment = []
org_sentiment = []
unknown_sentiment = []


for idx, user in enumerate(health_list_members):

    if idx >= limit_users:
        break

    # Fetch user info
    name = user.name

    # Remove any titles eg Dr. DR, MD, M.D. etc
    clean_name = name

    if '_' in clean_name:
        clean_name = clean_name.replace('_', ' ')  # eg Mark_Sisson -> 'Mark Sisson'

    if '(' in clean_name:
        clean_name = clean_name.replace('(', ' ')

    if ')' in clean_name:
        clean_name = clean_name.replace(')', ' ')

    qualification = []
    for title in remove_titles:
        # print(title)

        if title in clean_name:
            # print('Cleaning', name)
            qualification.append(title)

            if ',' in clean_name:
                clean_name = clean_name.replace(', ' + title, '')
            else:
                clean_name = clean_name.replace(' ' + title, '')
                clean_name = clean_name.replace(title, '').strip()  # Eg 'Dr. Rhonda'
            # print('Cleaned', clean_name)
    qualification = ', '.join(qualification)

    screen_name = user.screen_name

    first_name = clean_name.split(' ')[0]  # Get the first name

    if first_name.lower() == 'the' or clean_name in orgs:  # Eg The BMJ, The Lancet Global Health, The George Institute for Global Health
        gender = 'organisation'  # Likely an organisation, business or app
    else:
        gender = d.get_gender(first_name)  # Guess the gender based on the first name

    bio = user.description

    # for sym in special_symbols:
    #    bio = bio.replace(sym, '')

    bio = remove_symbols(bio, False)

    followers_count = user.followers_count
    following_count = user.friends_count

    dt = datetime.datetime(user.created_at.year, user.created_at.month, user.created_at.day)  # user.created_at
    # print(dt, type(dt), type(user.created_at.day))
    created = datetime.datetime.strptime(str(dt)[:10], '%Y-%m-%d').date()
    location = user.location
    status_count = user.statuses_count

    '''
    try:
        # Try to unwrap the shortened url
        # This is a slow process as the page has to be opened. Skip this line to speed up the process.
        if user.url is not None:
            user_url = requests.get(user.url).url   # eg Ken D Berry MD's website user.url = 'https://t.co/lvD0d50sVr' -> 'https://drberry.com/'
        else:
            user_url = ''
    except:
        user_url = user.url
    '''
    user_url = user.url

    # Status:Followers
    if followers_count > 0:
        status_follower = status_count / followers_count
    else:
        status_follower = ''

    # Follower:Following
    if following_count > 0:
        follower_following = followers_count / following_count
    else:
        follower_following = ''

    # Add each member to the csv
    print(idx, name, gender, qualification, location, created)
    if bio.strip() != '':
        print(bio)
    print(followers_count, following_count, status_follower, follower_following, status_count, user_url)
    print()
    
    # Set limits on health influencer to filter the most popular and most active
    if followers_count > 1000 and status_count > 1000:

        # Get status updates from the user
        try:
            tweets = api.user_timeline(screen_name=screen_name, count=number_of_tweets, exclude_replies=True, tweet_mode="extended")
        except:
            # tweepy.error.TweepError: Not authorized.   # Perhaps if the user has banned you or has set their profile to private
            print('Not authorized to view account')
            continue

        print(screen_name, 'Tweets:')
        tmp = []
        # Create array of tweet information
        # Using 'tweet.text' is a Tweepy truncated status update. Use tweet.full_text for the full tweet
        tweets_for_csv = [[name, qualification, tweet.created_at.strftime('%Y/%m/%d'), tweet.full_text] for tweet in tweets]   # tweet.id_str

        count_retrieved = 0
        count_claim = 0
        count_medical = 0
        count_nutrition = 0
        count_RT = 0

        array_polarity = []
        array_sentiment = []

        for twt in tweets_for_csv:
            text_tweet = remove_symbols(twt[3], False).replace('\n', ' ')  # Tweet text

            claim_w = []
            medi_w = []
            nutri_w = []

            # Skip any tweets with RT in them
            if text_tweet[:3] == 'RT ':  # Check the first 3 letters of the tweet
                count_RT += 1
                # continue

            # https://textblob.readthedocs.io/en/dev/quickstart.html#wordlists
            tweet = TextBlob(text_tweet)

            # output sentiment polarity
            # print('Sentiment')
            # print(text_tweet, type(text_tweet))
            # print(tweet.sentiment.polarity, tweet.sentiment.subjectivity)

            # Tally word counts from tweets
            tweet_text_list = str(text_tweet).split(' ')  # Make the tweet into a list of words
            # print(tweet_text_list)

            bool_claim = False
            bool_medical = False
            bool_nutrition = False

            # print('Check', text_tweet)

            # Check for individual word matches
            for word in tweet_text_list:
                word = word.lower().strip()

                if word not in ignore_words:  # and word not in remove_titles
                    if not word.isnumeric():
                        if len(word) > 2 and 'http' not in word:
                            # if '...' not in word:  # This occurs often as the tweets are cut short and thus creates new words
                            wordDict[word] += 1

                            if word in claim_words:
                                # print('Claim', word)
                                claim_w.append(word)
                                bool_claim = True
                                count_claim += 1

                            if word in medical_words:
                                # print('Med', word)
                                medi_w.append(word)
                                bool_medical = True
                                count_medical += 1

                            if word in nutrition_words:
                                # print('Nutri', word)
                                nutri_w.append(word)
                                bool_nutrition = True
                                count_nutrition += 1

            # Check for longer phrases
            for claim_word in claim_words:
                if len(claim_word.split()) > 1:
                    if claim_word in text_tweet and claim_word not in claim_w:
                        # print('Claim', claim_word)
                        claim_w.append(claim_word)
                        wordDict[claim_word] += 1
                        bool_claim = True
                        count_claim += 1

            for med_word in medical_words:
                if len(med_word.split()) > 1:
                    if med_word in text_tweet and med_word not in medi_w:
                        # print('Med', med_word)
                        medi_w.append(med_word)
                        wordDict[med_word] += 1
                        bool_medical = True
                        count_medical += 1

            for nutr_word in nutrition_words:
                if len(nutr_word.split()) > 1:
                    if nutr_word in text_tweet and nutr_word not in nutri_w:
                        # print('Nutri', nutr_word)
                        nutri_w.append(nutr_word)
                        wordDict[nutr_word] += 1
                        bool_nutrition = True
                        count_nutrition += 1

            # print(count_retrieved, bool_claim, bool_medical, bool_nutrition, twt)
            # if bool_claim and (bool_medical or bool_nutrition):
            if True:
                array_polarity.append(tweet.sentiment.polarity)
                array_sentiment.append(tweet.sentiment.subjectivity)

                claim_str = ''
                medi_str = ''
                nutri_str = ''

                if len(claim_w) > 0:
                    claim_str = ', '.join(claim_w)
                    # print('Claims:', claim_str)
                if len(medi_w) > 0:
                    medi_str = ', '.join(medi_w)
                    # print('Medi:', medi_str)
                if len(nutri_w) > 0:
                    nutri_str = ', '.join(nutri_w)
                    # print('Nutri:', nutri_str)

                check_claim = [bool_claim, bool_medical, bool_nutrition, claim_str, medi_str, nutri_str, tweet.sentiment.polarity, tweet.sentiment.subjectivity]
                row = check_claim + twt  # check_claim.extend(twt)
                c_tweets.writerow(row)

                print(name + ":", text_tweet)
                print('Claim', claim_str, 'Medi', medi_str, 'Nutri', nutri_str)  # type(check_claim), type(row))

                if len(claim_w) + len(medi_w) + len(nutri_w) > 0:
                    print()

            count_retrieved += 1

        print('Retrieved:', count_retrieved, 'RT', count_RT, 'Claims:', count_claim, 'Medical:', count_medical, 'Nutrition:', count_nutrition)
        print()

        # Set the minimum number of tweets you'll allow for each person. Make sure there is always a claim, and then a medical or nutrition keyword.
        if count_retrieved > 9 and count_claim > 0 and (count_medical + count_nutrition) > 0:
            polarity = statistics.median(array_polarity)
            sentiment = statistics.median(array_sentiment)

            row = [name, clean_name, screen_name, gender, qualification, bio, polarity, sentiment, followers_count, following_count, status_follower, follower_following, created, location, status_count, user_url, count_retrieved, count_RT, count_claim, count_medical, count_nutrition]
            c_bio.writerow(row)
            df.loc[name] = row

            '''
            warnings.simplefilter("error")
            try:
                plt.text(sentiment, polarity, re.sub(r"[^\x00-\x7f]", r"", name))  # re.sub(r"[^\x00-\x7f]", r"", name)
            except RuntimeWarning:
                #  RuntimeWarning: Glyph 129385 missing from current font.
                print('RuntimeWarning: Glyph 129385 missing from current font.', name, len(name))
            '''

            # Create a scatter plot
            # plt.scatter(sentiment, polarity, color='purple')

            if gender == 'male' or gender == 'mostly_male':
                male_polarity.append(polarity)
                male_sentiment.append(sentiment)
                # print('Gender', gender, male_polarity, male_sentiment)
            elif gender == 'female' or gender == 'mostly_female':
                female_polarity.append(polarity)
                female_sentiment.append(sentiment)
                # print('Gender', gender, female_polarity, female_sentiment)
            elif gender == 'organisation':
                org_polarity.append(polarity)
                org_sentiment.append(sentiment)
                # print('Gender', gender, org_polarity, org_sentiment)
            else:
                unknown_polarity.append(polarity)
                unknown_sentiment.append(sentiment)
                # print('Gender', gender, unknown_polarity, unknown_sentiment)

print()
print(df)
print()

x_axis = ['status_count', 'count_nutrition', 'count_claim', 'count_claim', 'count_retrieved', 'count_retrieved', 'sentiment', 'followers_count']
y_axis = ['followers_count', 'count_medical', 'count_nutrition', 'count_medical', 'count_claim', 'count_RT', 'polarity', 'following_count']

for i, x in enumerate(x_axis):
    y = y_axis[i]
    plt.figure()

    # Break up the plot into gender categories
    df_male = df[df['gender'].isin(['male', 'mostly_male'])]
    df_female = df[df['gender'].isin(['female', 'mostly_female'])]
    df_org = df[df['gender'].isin(['organisation'])]
    df_unknown = df[df['gender'].isin(['unknown', 'andy'])]

    try:
        # print('string', x, type(x), y, type(y))
        plt.scatter(df_male[x], df_male[y], color='blue', label='men')
        plt.scatter(df_female[x], df_female[y], color='red', label='women')
        plt.scatter(df_org[x], df_org[y], color='orange', label='organisations')
        plt.scatter(df_unknown[x], df_unknown[y], color='green', label='unknown')
    except Exception as e:
        # exc = e
        print(e)
        print(x)
        print(y)
        tb_str = ''.join(traceback.format_exception(None, e, e.__traceback__))
        print(tb_str)

    # Titles and labels for the scatter plot
    plt.title(x + ' vs ' + y, fontsize=20)
    plt.xlabel(x, fontsize=15)  # '← Negative — — — — — — Positive →'
    plt.ylabel(y, fontsize=15)  # ← Facts — — — — — — — Opinions →
    plt.legend(loc='upper left')
    plot_name = (str(x) + ' ' + str(y)).replace(':', '_')
    plt.savefig(plot_name + '.png')

# Create a scatter plot

'''
plt.figure()
if male_sentiment != [] and male_polarity != []:
    plt.scatter(statistics.median(male_sentiment), statistics.median(male_polarity), color='blue', label='Male')
if female_sentiment != [] and female_polarity != []:
    plt.scatter(statistics.median(female_sentiment), statistics.median(female_polarity), color='red', label='Female')
if org_sentiment != [] and org_polarity != []:
    plt.scatter(statistics.median(org_sentiment), statistics.median(org_polarity), color='orange', label='Org')
if unknown_sentiment != [] and unknown_polarity != []:
    plt.scatter(statistics.median(unknown_sentiment), statistics.median(unknown_polarity), color='green', label='unknown')
'''



# Close and save the CSV
csvfile_bio.close()


# Save the bio / tweet word count
outfile = "word_freq-" + twitter_health_list + "-" + date_time_string + ".csv"
print()
print('Saving', outfile)
fp = open(outfile, encoding='utf-8-sig', mode='w', newline='')
fp.write('Word,freq,list1,list2,list3\n')

sort_dict = sorted(wordDict.items(), key=lambda x: (x[1], x[0]), reverse=True)  # , reverse=True
for tag, count in sort_dict:  # Sort the dictionary by most common words first

    word_list = []
    if tag in claim_words:
        word_list.append('claim')

    if tag in medical_words:
        word_list.append('medical')

    if tag in nutrition_words:
        word_list.append('nutrition')

    if len(word_list) >= 1:
        print(tag, count, word_list)
        fp.write('{},{},{}\n'.format(tag.lower(), count, ', '.join(word_list)))
    else:
        fp.write('{},{}\n'.format(tag.lower(), count))

print(len(sort_dict))
print('Closing', outfile)
fp.close()
