import tweepy
import ssl
import psycopg2
ssl._create_default_https_context = ssl._create_unverified_context

# Getting UserID:

def get_user_ID(email):

    query = f"SELECT * FROM users WHERE email = '{email}'"
    connection = psycopg2.connect(host='ec2-3-229-166-245.compute-1.amazonaws.com', database='d81l57ohoqttlu', user='owrzrgewethgnm', password='179c8ce1e814e2081f9f1cdf42240a30f465d6c1b61e442d7ff9d5a42f3e775f')
    c = connection.cursor()

    c.execute(query)
    result = c.fetchall()
    user_id = result[0][4]

    connection.commit()
    c.close()
    connection.close()

    return user_id

def get_twitter_replies(name):
    # Oauth keys
    consumer_key = "44nG5dXxs0EXFcXIMUWt4YCBd"
    consumer_secret = "iG8MtPyvN4wI2uJtHKxfGha5jVFWEmzlSPCSS3SkOtiRfrGWEC"
    access_token = "1458819035148087298-Zao7rpD2JEGyQ7GDapL98q21ANL141"
    access_token_secret = "7wwb7xEIaqS7MNa6hzNftFTYz9QvXf04GJMuegu5aooda"

    # Authentication with Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # update these for the tweet you want to process replies to 'name' = the account username and you can find the tweet id within the tweet URL

    # Need to scrape this from web URL.
    tweet_id = '1484576688763719685'
    replies=[] 
    for tweet in tweepy.Cursor(api.search_tweets,q='to:'+name, result_type='recent', tweet_mode='extended').items(100):
        replies.append(tweet)
        
        # if hasattr(tweet, 'in_reply_to_status_id_str'):
        #     if (tweet.in_reply_to_status_id_str==tweet_id):
        #         replies.append(tweet)
    
    return replies



def update_db(replies, user_id):
    connection = psycopg2.connect(host='ec2-3-229-166-245.compute-1.amazonaws.com', database='d81l57ohoqttlu', user='owrzrgewethgnm', password='179c8ce1e814e2081f9f1cdf42240a30f465d6c1b61e442d7ff9d5a42f3e775f')
    c = connection.cursor()


    default_senti_score = -1

    for tweet in replies:
        
        query = "INSERT INTO twitter_replies (user_id, reply, sentiscore) VALUES (%s, %s, %s);"
        review = (user_id, tweet.full_text.replace('\n', ' '), default_senti_score, )
        c.execute(query, review)

    connection.commit()
    c.close()
    connection.close()


update_db(get_twitter_replies('amazon'), 70)