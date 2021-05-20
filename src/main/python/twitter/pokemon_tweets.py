import json
import tweepy as tw
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import smtplib
import os
from dateutil.relativedelta import relativedelta
import datetime as dt

# authentication details stored locally
pass_key_path = r'C:\Users\tkdmc\Documents\GitHub\mchung_pass\twitter_pass.json'

with open(pass_key_path) as f:
    data = json.load(f)

consumer_key = data['consumer_key']
consumer_secret = data['consumer_secret_key']
access_token = data['access_token']
access_token_secret = data['access_token_secret']


def search_for_tweet(search_query, date_since):
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    tweets = tw.Cursor(api.search,
                       q=search_query,
                       lang="en",
                       since=date_since).items(200)

    # output into dataframe
    tweets_res = [[tweet.user.screen_name, tweet.created_at, tweet.text] for tweet in tweets]

    df = pd.DataFrame(data=tweets_res,
                      columns=["username", "creation_time", "tweet"])

    return df


def send_email(sender, reciever, email_body, email_subject, file_name):
    # Create a multipart message
    # Modified from https://djangocentral.com/sending-emails-with-csv-attachment-using-python/

    msg = MIMEMultipart()
    body_part = MIMEText(email_body, 'plain')
    msg['Subject'] = email_subject
    msg['From'] = sender
    msg['To'] = reciever
    # Add body to email
    msg.attach(body_part)
    # open and read the CSV file in binary

    with open('pokemon_tweets_results.csv', 'rb') as file:
        # Attach the file with filename to the email
        msg.attach(MIMEApplication(file.read(), Name=file_name))

    # Create SMTP object
    session = smtplib.SMTP('smtp.gmail.com', 587)
    # Login to the server
    session.starttls()  # enable security
    session.login(sender, data[sender])

    # Convert the message to a string and send it
    session.sendmail(msg['From'], msg['To'], msg.as_string())
    session.quit()


if __name__ == '__main__':
    # search for tweets
    user_ID = 'Pokemon'  # only want tweets from @Pokemon
    search_query = "#PokemonBrilliantDiamond" + " -filter:retweets".format(user_ID)
    date_since = (dt.datetime.today() - relativedelta(months=2)).strftime('%Y-%m-%d')  # start from the last two months

    result_file_name = 'pokemon_tweets_results.csv'

    df = search_for_tweet(search_query, date_since)
    df.to_csv(result_file_name)

    email_body = """ Pokemon Brilliant Diamond Tweets"""
    email_subject = """ Pokemon Brilliant Diamond Tweets"""
    sender = 'pokemonwithmichelle@gmail.com'
    receiver = 'pokemonwithmichelle@gmail.com'

    send_email(sender=sender, reciever=receiver, email_body=email_body, email_subject=email_subject,
               file_name=result_file_name)

    # remove at end so as to not commit it to Github
    if os.path.exists(result_file_name):
        os.remove(result_file_name)


