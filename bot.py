from pytumblr import TumblrRestClient
"""
This script uses the pytumblr library to interact with the Tumblr API and automate posting content to a Tumblr blog.

Functions:
    post_content(): Creates a text post on the specified Tumblr blog with a daily update message.
    like_and_reblog_posts(): Automatically likes and reblogs posts with specified tags.

Scheduled Tasks:
    The script schedules both post_content and like_and_reblog_posts functions to run every 8 hours.

Modules:
    pytumblr: Provides the TumblrRestClient class to interact with the Tumblr API.
    schedule: Allows scheduling of tasks at specific intervals.
    time: Provides time-related functions.

Usage:
    Ensure you have the pytumblr, schedule, and time modules installed.
    Replace 'consumer_key', 'consumer_secret', 'oauth_token', and 'oauth_secret' with your actual Tumblr API credentials.
    Replace 'your-blog-name' with the name of your Tumblr blog.
    Replace 'path/to/image.jpg' with the actual path to the image you want to post.
    Run the script to start the automated posting process.
"""

client = TumblrRestClient(
    'consumer_key',
    'consumer_secret',
    'oauth_token',
    'oauth_secret'
)
#Auto-Posting Content
#Text Post
client.create_text('your-blog-name', title='...', body='Your Daily Caitlyn Kiramman Content')
#Photo Post
client.create_photo('Caitlyn Kiramman Simp', state='published', tags=['Arcane', 'Caitlyn', 'Caitlyn Kiramman', 'League of Legends', 'Caitvi'], data=['path/to/image.jpg'])

import schedule
import time

def post_content():
    global client
    client.create_text('your-blog-name', title='Daily Update', body='Here’s something new!')

schedule.every(8).hours.do(post_content)

while True:
    schedule.run_pending()
    time.sleep(1)


def like_and_reblog_posts():
    search_tags = ['Arcane', 'Caitlyn', 'Caitlyn Kiramman', 'League of Legends', 'Caitvi']
    for tag in search_tags:
        try:
            posts = client.tagged(tag, limit=5)
            # Like the post
            try:
                client.like(post_id=post['id'], reblog_key=post['reblog_key'])
                # Reblog the post
                try:
                    client.reblog('your-blog-name', id=post['id'], reblog_key=post['reblog_key'])
                except Exception as e:
                    print(f"An error occurred while reblogging post with id '{post['id']}': {e}")
            except Exception as e:
                print(f"An error occurred while liking post with id '{post['id']}': {e}")
        except Exception as e:
            print(f"An error occurred while fetching or processing posts for tag '{tag}': {e}")

# Schedule the like_and_reblog_posts function to run every 8 hours, same as post_content
schedule.every(8).hours.do(like_and_reblog_posts)
