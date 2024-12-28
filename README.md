# Caitlyn Kiramman Tumblr Bot

An autonomous bot designed for Tumblr, posting Caitlyn Kiramman content every 4 hours. This project aims to keep fans engaged with regular updates featuring Caitlyn Kiramman.

## Features
- Automatically posts curated Caitlyn Kiramman content every 4 hours.
- Fully automated workflow for consistent posting.
- Configurable scheduling and content customization.

## Setup Instructions

### Prerequisites
- [Python](https://www.python.org/) 
- A Tumblr account
- [Tumblr API Key](https://www.tumblr.com/docs/en/api/v2)

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/caitlyn-kiramman-tumblr-bot.git
   ```

### Configuration
1. Create a `.env` file in the root directory:
   ```
   TUMBLR_CONSUMER_KEY=your_consumer_key
   TUMBLR_CONSUMER_SECRET=your_consumer_secret
   TUMBLR_TOKEN_KEY=your_token_key
   TUMBLR_TOKEN_SECRET=your_token_secret
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
1. Start the bot:
   ```bash
   python bot.py
   ```

2. The bot will automatically:
   - Post content every 4 hours
   - Log activities in `bot.log`
   - Handle rate limiting and errors

### Custom Settings
Edit `config.py` to modify:
- Posting frequency
- Content filters
- Image sources
- Hashtag preferences

### Contributing
1. Fork the repository
2. Create a feature branch
3. Submit a Pull Request
