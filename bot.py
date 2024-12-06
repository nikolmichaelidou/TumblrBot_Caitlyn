from pytumblr import TumblrRestClient

client = TumblrRestClient(
    'consumer_key',
    'consumer_secret',
    'oauth_token',
    'oauth_secret'
)

client.create_text('All Caitlyn Kiramman Content', title='...', body='Your Daily Caitlyn Kiramman Content')

client.create_photo('Caitlyn Kiramman Simp', state='published', tags=['daily', 'art', 'Caitlyn', 'Arcane'], data=['path/to/image.jpg'])

import schedule
import time

def post_content():
    client.create_text('your-blog-name', title='Daily Update', body='Here’s something new!')

schedule.every(8).hours.do(post_content)

while True:
    schedule.run_pending()
    time.sleep(1)
