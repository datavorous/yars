import os
import json
import requests
from datetime import datetime
from urllib.parse import urlparse
from googlesearch import search
from reddit_miner import RedditMiner


class Utils(RedditMiner):
    def __init__(self, user_agent='Mozilla/5.0', proxy=None):
        super().__init__(user_agent, proxy)

    def data_hoarder(self, subreddit, limit=10, category='hot', time_filter='all', output_file='subreddit_data.json'):
        posts = self.fetch_reddit_data(subreddit, limit, category, time_filter)
        with open(output_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(posts, jsonfile, ensure_ascii=False, indent=4)

        print(f"Data saved to {output_file}")

    def user_osint(self, username, limit=100, output_file='user_data.json'):
        user_data = self.scrape_user_data(username, limit)
        print(len(user_data))
        with open(output_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(user_data, jsonfile, ensure_ascii=False, indent=2)

        print(f"User data saved to {output_file}")

    def download_image(self, image_url, output_folder='images'):

        os.makedirs(output_folder, exist_ok=True)

        filename = os.path.basename(urlparse(image_url).path)

        filepath = os.path.join(output_folder, filename)

        response = self.session.get(image_url, stream=True)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)
            print(f"Downloaded: {filepath}")
            return filepath
        else:
            print(f"Failed to download: {image_url}")
            return None