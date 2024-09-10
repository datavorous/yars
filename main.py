import requests
from googlesearch import search

class RedditMiner:
    def __init__(self, user_agent='Mozilla/5.0', proxy=None):
        self.headers = {'User-Agent': user_agent}
        self.session = requests.Session()
        self.session.headers.update(self.headers)

        # Add proxy configuration if provided
        if proxy:
            self.session.proxies.update({
                'http': proxy,
                'https': proxy
            })

    def search_reddit(self, query, limit=10, after=None, before=None, lang="en", sleep_interval=0):
        time_filter = f" after:{after}" if after else ""
        time_filter += f" before:{before}" if before else ""

        google_query = f'site:reddit.com {query}{time_filter}'
        search_results = search(google_query, num_results=limit, lang=lang, sleep_interval=sleep_interval, advanced=True)
        
        results = [{'title': result.title, 'link': result.url, 'description': result.description} for result in search_results]
        return results

    def scrape_user_data(self, username, limit=10):
        base_url = f"https://www.reddit.com/user/{username}/.json"
        params = {'limit': limit, 'after': None}
        all_items = []
        count = 0

        while count < limit:
            response = self.session.get(base_url, params=params)
            
            # Check for status code errors
            if response.status_code != 200:
                print(f"Failed to fetch data for user {username}: {response.status_code}")
                break

            try:
                data = response.json()
            except ValueError:
                print(f"Failed to parse JSON response for user {username}.")
                break
            
            if 'data' not in data or 'children' not in data['data']:
                print(f"No 'data' or 'children' field found in response for user {username}.")
                break

            items = data['data']['children']
            if not items:
                print(f"No more items found for user {username}.")
                break

            for item in items:
                kind = item['kind']
                item_data = item['data']
                if kind == 't3':  # This represents a post
                    post_url = f"https://www.reddit.com{item_data.get('permalink', '')}"
                    all_items.append({
                        'type': 'post',
                        'title': item_data.get('title', ''),
                        'subreddit': item_data.get('subreddit', ''),
                        'url': post_url,
                        'created_utc': item_data.get('created_utc', '')
                    })
                elif kind == 't1':  # This represents a comment
                    comment_url = f"https://www.reddit.com{item_data.get('permalink', '')}"
                    all_items.append({
                        'type': 'comment',
                        'subreddit': item_data.get('subreddit', ''),
                        'body': item_data.get('body', ''),
                        'created_utc': item_data.get('created_utc', ''),
                        'url': comment_url
                    })
                count += 1
                if count >= limit:
                    break

            params['after'] = data['data'].get('after')
            if not params['after']:
                break
        
        return all_items

    def fetch_reddit_data(self, subreddit, limit=100):
        base_url = f"https://www.reddit.com/r/{subreddit}/.json"
        params = {'limit': limit, 'after': None}
        all_posts = []
        count = 0

        while count < limit:
            response = self.session.get(base_url, params=params)
            if response.status_code != 200:
                print(f"Failed to fetch data: {response.status_code}")
                break

            data = response.json()
            posts = data['data']['children']
            
            if not posts:
                break

            for post in posts:
                post_data = post['data']
                post_info = {
                    'title': post_data['title'],
                    'author': post_data['author'],
                    'permalink': post_data['permalink']
                }

                # Check if the post contains an image and add image URL if present
                if post_data.get('post_hint') == 'image' and 'url' in post_data:
                    post_info['image_url'] = post_data['url']
                elif 'preview' in post_data and 'images' in post_data['preview']:
                    post_info['image_url'] = post_data['preview']['images'][0]['source']['url']

                # Check if the post contains a thumbnail
                if 'thumbnail' in post_data and post_data['thumbnail'] and post_data['thumbnail'] != 'self':
                    post_info['thumbnail_url'] = post_data['thumbnail']
                
                all_posts.append(post_info)
                count += 1
                if count >= limit:
                    break

            params['after'] = data['data']['after']
            if not params['after']:
                break

        return all_posts

    def scrape_post_details(self, permalink):
        url = f"https://www.reddit.com{permalink}.json"
        response = self.session.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch post data: {response.status_code}")
            return None

        post_data = response.json()
        main_post = post_data[0]['data']['children'][0]['data']
        title = main_post['title']
        body = main_post.get('selftext', '')
        comments = self._extract_comments(post_data[1]['data']['children'])
        
        return {'title': title, 'body': body, 'comments': comments}

    def _extract_comments(self, comments):
        extracted_comments = []
        for comment in comments:
            if comment['kind'] == 't1':
                extracted_comments.append({
                    'author': comment['data']['author'],
                    'body': comment['data']['body'],
                    'replies': self._extract_comments(comment['data']['replies']['data']['children']) if comment['data']['replies'] else []
                })
        return extracted_comments

    

# Initialize the RedditMiner
miner = RedditMiner()

# 1. Search Reddit
search_results = miner.search_reddit("python programming", limit=5)
print("Search Results:")
for result in search_results:
    print(f"Title: {result['title']}")
    print(f"Link: {result['link']}")
    print(f"Description: {result['description']}")
    print("---")

# 2. Scrape User Data
user_data = miner.scrape_user_data("spez", limit=5)
print("\nUser Data:")
for item in user_data:
    if item['type'] == 'post':
        print(f"Post: {item['title']} in r/{item['subreddit']}")
    else:
        print(f"Comment in r/{item['subreddit']}: {item['body'][:50]}...")
    print(f"URL: {item['url']}")
    print("---")

# 3. Fetch Subreddit Data
subreddit_posts = miner.fetch_reddit_data("AskReddit", limit=5)
print("\nSubreddit Posts:")
for post in subreddit_posts:
    print(f"Title: {post['title']}")
    print(f"Author: {post['author']}")
    print(f"Permalink: {post['permalink']}")
    if 'image_url' in post:
        print(f"Image URL: {post['image_url']}")
    if 'thumbnail_url' in post:
        print(f"Thumbnail URL: {post['thumbnail_url']}")
    print("---")

# 4. Scrape Post Details
post_details = miner.scrape_post_details("/r/ArtistLounge/comments/16nht0k/what_do_you_think_about_generative_art/")
if post_details:
    print("\nPost Details:")
    print(f"Title: {post_details['title']}")
    print(f"Body: {post_details['body']}")
    print("Top-level comments:")
    for comment in post_details['comments']:
        print(f"- {comment['author']}: {comment['body']}")


"""
# 5. Using a proxy (optional)
proxy_miner = RedditMiner(proxy="http://your-proxy-url:port")
proxy_search_results = proxy_miner.search_reddit("proxy test", limit=1)
print("\nProxy Search Result:")
print(proxy_search_results[0]['title'])
"""
