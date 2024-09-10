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
        data = []

        for post in posts:
            post_details = self.scrape_post_details(post['permalink'])
            if post_details:
                post.update({
                    'body': post_details['body'],
                    'comments': post_details['comments']
                })
            data.append(post)

        with open(output_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, ensure_ascii=False, indent=2)

        print(f"Data saved to {output_file}")

    def user_osint(self, username, limit=100, output_file='user_data.json'):
        user_data = self.scrape_user_data(username, limit)
        
        with open(output_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(user_data, jsonfile, ensure_ascii=False, indent=2)

        print(f"User data saved to {output_file}")

    def bulk_image_downloader(self, subreddit, limit=10, category='hot', time_filter='all', output_folder='images'):
        posts = self.fetch_reddit_data(subreddit, limit, category, time_filter)
        os.makedirs(output_folder, exist_ok=True)
        links_file = os.path.join(output_folder, 'image_data.json')

        image_data = []

        for post in posts:
            image_url = post.get('image_url') or post.get('thumbnail_url')
            if image_url:
                if 'preview' in image_url:
                    image_url = post.get('thumbnail_url', '')
                
                if image_url and any(ext in image_url.lower() for ext in ['.png', '.jpg', '.jpeg', '.gif']):
                    filename = self._download_image(image_url, output_folder)
                    if filename:
                        image_data.append({
                            'title': post['title'],
                            'url': image_url,
                            'local_filename': filename
                        })

        with open(links_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(image_data, jsonfile, ensure_ascii=False, indent=2)

        print(f"Images downloaded to {output_folder}")
        print(f"Image data saved to {links_file}")

    def _download_image(self, url, folder):
        response = self.session.get(url, stream=True)
        if response.status_code == 200:
            filename = os.path.join(folder, os.path.basename(urlparse(url).path))
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(8192):
                    f.write(chunk)
            print(f"Downloaded: {filename}")
            return filename
        else:
            print(f"Failed to download: {url}")
            return None

