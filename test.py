import tweepy

# OAuth1 authentication
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)

api = tweepy.API(auth)

# Upload the image
image_path = "test.png"
media = api.media_upload(filename=image_path)
media_id = media.media_id

# OAuth2 authentication for creating tweet
client = tweepy.Client(
    bearer_token,
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
)

# Create a tweet with the uploaded media
client.create_tweet(text="TESTING", media_ids=[media_id])
