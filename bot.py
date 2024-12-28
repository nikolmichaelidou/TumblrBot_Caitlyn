from pytumblr import TumblrRestClient
import schedule
import time
import logging
import os
from dotenv import load_dotenv
from time import sleep
from random import randint

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    filename='tumblr_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# Initialize the Tumblr client with environment variables
client = TumblrRestClient(
    os.getenv('API_KEY'),
    os.getenv('API_SECRET'),
    os.getenv('TOKEN'),
    os.getenv('TOKEN_SECRET')
)

def retry_with_backoff(func, max_retries=3):
    """Retry function with exponential backoff"""
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if i == max_retries - 1:
                raise e
            sleep_time = (2 ** i) + randint(0, 1)
            logging.warning(f"Attempt {i+1} failed, retrying in {sleep_time} seconds...")
            sleep(sleep_time)

def post_content():
    """Post content with retry mechanism"""
    try:
        content = {
            'title': 'Daily Caitlyn Kiramman Update',
            'body': 'Here's your daily dose of Caitlyn content!',
            'state': 'published',
            'tags': ['Caitlyn Kiramman', 'Arcane', 'League of Legends']
        }
        
        def post():
            client.create_text(
                os.getenv('BLOG_NAME', 'your-blog-name'),
                **content
            )
        
        retry_with_backoff(post)
        logging.info('Successfully posted content.')
    except Exception as e:
        logging.error('Error posting content', exc_info=True)

def like_and_reblog_posts(limit=5):
    """Like and reblog posts with rate limiting"""
    search_tags = ['Arcane', 'Caitlyn', 'Caitlyn Kiramman', 'League of Legends', 'Caitvi']
    for tag in search_tags:
        try:
            posts = client.tagged(tag, limit=limit)
            for post in posts:
                sleep(1)  # Rate limiting
                try:
                    retry_with_backoff(
                        lambda: client.like(post_id=post['id'], reblog_key=post['reblog_key'])
                    )
                    logging.info(f"Liked post {post['id']}")
                    
                    sleep(1)  # Rate limiting between actions
                    
                    retry_with_backoff(
                        lambda: client.reblog(os.getenv('BLOG_NAME'), id=post['id'], 
                                           reblog_key=post['reblog_key'])
                    )
                    logging.info(f"Reblogged post {post['id']}")
                except Exception as e:
                    logging.error(f"Error processing post {post['id']}", exc_info=True)
        except Exception as e:
            logging.error(f"Error fetching posts for tag '{tag}'", exc_info=True)

# Schedule tasks with proper intervals
schedule.every(8).hours.do(post_content)
schedule.every(4).hours.do(like_and_reblog_posts, limit=5)

# Main loop with error handling
def main():
    logging.info("Bot started successfully")
    while True:
        try:
            schedule.run_pending()
            sleep(60)
        except Exception as e:
            logging.error("Error in main loop", exc_info=True)
            sleep(300)  # Wait 5 minutes on error

if __name__ == "__main__":
    main()