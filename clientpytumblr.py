client = pytumblr.TumblrRestClient(
    '<consumer_key>',
    '<consumer_secret>',
    '<oauth_token>',
    '<oauth_secret>',
)

client.info() # Grabs the current user information