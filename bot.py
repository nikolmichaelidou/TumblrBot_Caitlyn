from pytumblr import TumblrRestClient
import schedule
import time
import logging

# Set up logging
logging.basicConfig(filename='tumblr_bot.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the Tumblr client
client = TumblrRestClient(
    'consumer_key',
    'consumer_secret',
    'oauth_token',
    'oauth_secret'
)

# Function: Auto-post content
def post_content(client):
    try:
        client.create_text('your-blog-name', title='Daily Update', body='Here’s something new!')
        logging.info('Successfully posted content.')
    except Exception as e:
        logging.error('Error posting content', exc_info=True)

# Function: Like and reblog posts
def like_and_reblog_posts():
    search_tags = ['Arcane', 'Caitlyn', 'Caitlyn Kiramman', 'League of Legends', 'Caitvi']
    for tag in search_tags:
        try:
            posts = client.tagged(tag, limit=5)
            for post in posts:
                try:
                    client.like(post_id=post['id'], reblog_key=post['reblog_key'])
                    logging.info(f"Liked post with id '{post['id']}'")
                    client.reblog('your-blog-name', id=post['id'], reblog_key=post['reblog_key'])
                    logging.info(f"Reblogged post with id '{post['id']}'")
                except Exception as e:
                    logging.error(f"Error processing post '{post['id']}'", exc_info=True)
        except Exception as e:
            logging.error(f"Error fetching posts for tag '{tag}'", exc_info=True)

# Schedule tasks
schedule.every(8).hours.do(post_content, client)
schedule.every(8).hours.do(like_and_reblog_posts)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
