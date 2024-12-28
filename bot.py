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
def post_content():
    try:
        client.create_text('your-blog-name', title='Daily Update', body='Here’s something new!')
        logging.info('Successfully posted content.')
    except Exception as e:
        logging.error('Error posting content', exc_info=True)

# Function: Like and reblog posts
def like_and_reblog_posts(limit=5):
    search_tags = ['Arcane', 'Caitlyn', 'Caitlyn Kiramman', 'League of Legends', 'Caitvi']
    for tag in search_tags:
        try:
            posts = client.tagged(tag, limit=limit)
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

# Function: Answer asks
def answer_asks():
    try:
        asks = client.inbox(limit=5)
        for ask in asks['posts']:
            if ask['type'] == 'question':
                client.answer('your-blog-name', ask['id'], answer='Thanks for your question! Here’s my reply...')
                logging.info(f"Answered question with ID: {ask['id']}")
    except Exception as e:
        logging.error('Error answering asks', exc_info=True)

# Function: Send messages to followers
def send_messages_to_followers():
    try:
        followers = client.followers('your-blog-name', limit=5)
        for follower in followers['users']:
            try:
                client.send_a_post(
                    recipient_blog_url=follower['name'],
                    post_content='Hello! Thanks for following my blog!'
                )
                logging.info(f"Sent a message to {follower['name']}")
                time.sleep(1)  # Avoid hitting rate limits
            except Exception as e:
                logging.error(f"Failed to send a message to {follower['name']}", exc_info=True)
    except Exception as e:
        logging.error('Error fetching followers', exc_info=True)

# Function: Process inbox messages
def process_inbox_messages():
    try:
        inbox = client.inbox(limit=10)
        for message in inbox['posts']:
            try:
                if message['type'] == 'text':
                    logging.info(f"Message from {message['blog_name']}: {message['body']}")
                elif message['type'] == 'photo':
                    logging.info(f"Photo message from {message['blog_name']}: {message['photos']}")
                else:
                    logging.info(f"Unhandled message type from {message['blog_name']}: {message['type']}")
            except Exception as e:
                logging.error(f"Error processing message from {message['blog_name']}", exc_info=True)
    except Exception as e:
        logging.error('Error fetching inbox messages', exc_info=True)

# Schedule tasks
schedule.every(8).hours.do(post_content)
schedule.every(8).hours.do(like_and_reblog_posts, limit=5)
schedule.every(8).hours.do(answer_asks)
schedule.every(8).hours.do(send_messages_to_followers)
schedule.every(8).hours.do(process_inbox_messages)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)