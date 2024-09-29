import requests
import time

class YARS:
    """
    A class to interact with Reddit's API and perform various operations such as searching for posts, 
    scraping post details, fetching user data, and retrieving posts from specific subreddits using the age old .json trick.
    """

    def __init__(self, user_agent='Mozilla/5.0', proxy=None):
        """
        Initializes the YARS object with a user agent and optional proxy configuration.

        Parameters:
        - user_agent (str): The user agent string to use for requests. Defaults to 'Mozilla/5.0'.
        - proxy (str): Optional. Proxy URL to use for requests. Defaults to None.
        """
        # Set up headers with the specified user agent
        self.headers = {'User-Agent': user_agent}
        
        # Create a session to manage requests
        self.session = requests.Session()
        self.session.headers.update(self.headers)

        # If a proxy is provided, configure it for the session
        if proxy:
            self.session.proxies.update({
                'http': proxy,
                'https': proxy
            })

    def search_reddit(self, query, limit=10, after=None, before=None):
        """
        Searches Reddit for posts matching the given query.

        Parameters:
        - query (str): The search query string.
        - limit (int): The maximum number of posts to return. Defaults to 10.
        - after (str): Optional. Fetch results after this ID. Defaults to None.
        - before (str): Optional. Fetch results before this ID. Defaults to None.

        Returns:
        - list: A list of dictionaries containing post title, link, and description.
        """
        url = "https://www.reddit.com/search.json"
        params = {
            'q': query,  # Search query
            'limit': limit,  # Number of results to return
            'sort': 'relevance',  # Sort by relevance
            'type': 'link'  # Search for posts only
        }
        # Add 'after' and 'before' parameters if provided
        if after:
            params['after'] = after
        if before:
            params['before'] = before

        # Send the request
        response = self.session.get(url, params=params)
        if response.status_code != 200:
            # Handle failed request
            print(f"Failed to fetch search results: {response.status_code}")
            return []

        # Parse the response JSON
        data = response.json()
        results = []
        
        # Extract relevant information from each post in the results
        for post in data['data']['children']:
            post_data = post['data']
            results.append({
                'title': post_data['title'],
                'link': f"https://www.reddit.com{post_data['permalink']}",
                'description': post_data.get('selftext', '')[:269]  # Truncate description to 269 characters
            })
        return results

    def scrape_post_details(self, permalink):
        """
        Retrieves detailed information about a specific post given its permalink.

        Parameters:
        - permalink (str): The permalink URL of the post.

        Returns:
        - dict: A dictionary containing the post's title, body, and comments.
        """
        url = f"https://www.reddit.com{permalink}.json"
        
        # Send the request to get post details
        response = self.session.get(url)
        if response.status_code != 200:
            # Handle failed request
            print(f"Failed to fetch post data: {response.status_code}")
            return None

        # Parse the response JSON
        post_data = response.json()
        if not isinstance(post_data, list) or len(post_data) < 2:
            # Validate the response structure
            print("Unexpected post data structure")
            return None

        # Extract main post data
        main_post = post_data[0]['data']['children'][0]['data']
        title = main_post['title']
        body = main_post.get('selftext', '')

        # Extract comments using helper function
        comments = self._extract_comments(post_data[1]['data']['children'])
        
        return {'title': title, 'body': body, 'comments': comments}

    def _extract_comments(self, comments):
        """
        Recursively extracts comments and their replies from the post data.

        Parameters:
        - comments (list): A list of comment objects from Reddit's API.

        Returns:
        - list: A list of extracted comments and replies.
        """
        extracted_comments = []
        
        for comment in comments:
            # Check if the comment is a dictionary and of the right kind ('t1')
            if isinstance(comment, dict) and comment.get('kind') == 't1':
                comment_data = comment.get('data', {})
                extracted_comment = {
                    'author': comment_data.get('author', ''),
                    'body': comment_data.get('body', ''),
                    'replies': []  # Placeholder for nested replies
                }

                # Recursively extract replies if they exist
                replies = comment_data.get('replies', '')
                if isinstance(replies, dict):
                    extracted_comment['replies'] = self._extract_comments(replies.get('data', {}).get('children', []))
                
                # Append the extracted comment to the list
                extracted_comments.append(extracted_comment)
        
        return extracted_comments

    def scrape_user_data(self, username, limit=10):
        """
        Fetches recent activity (posts and comments) of a specified Reddit user.

        Parameters:
        - username (str): The Reddit username.
        - limit (int): The maximum number of items to fetch. Defaults to 10.

        Returns:
        - list: A list of dictionaries containing user activity.
        """
        base_url = f"https://www.reddit.com/user/{username}/.json"
        params = {'limit': limit, 'after': None}
        all_items = []
        count = 0

        # Continue fetching data until the limit is reached
        while count < limit:
            response = self.session.get(base_url, params=params)
            
            # Check for response status code errors
            if response.status_code != 200:
                print(f"Failed to fetch data for user {username}: {response.status_code}")
                break

            try:
                # Attempt to parse the JSON response
                data = response.json()
            except ValueError:
                # Handle parsing errors
                print(f"Failed to parse JSON response for user {username}.")
                break
            
            # Validate the data structure
            if 'data' not in data or 'children' not in data['data']:
                print(f"No 'data' or 'children' field found in response for user {username}.")
                break

            items = data['data']['children']
            if not items:
                # Break if no more items are found
                print(f"No more items found for user {username}.")
                break

            # Process each item (post or comment)
            for item in items:
                kind = item['kind']
                item_data = item['data']
                if kind == 't3':  # 't3' represents a post
                    post_url = f"https://www.reddit.com{item_data.get('permalink', '')}"
                    all_items.append({
                        'type': 'post',
                        'title': item_data.get('title', ''),
                        'subreddit': item_data.get('subreddit', ''),
                        'url': post_url,
                        'created_utc': item_data.get('created_utc', '')
                    })
                elif kind == 't1':  # 't1' represents a comment
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

            # Set 'after' parameter for pagination
            params['after'] = data['data'].get('after')
            if not params['after']:
                break
        
        return all_items
        
    def fetch_subreddit_posts(self, subreddit, limit=10, category='hot', time_filter='all'):
        """
        Fetches posts from a specified subreddit based on category and time filter.

        Parameters:
        - subreddit (str): The name of the subreddit to fetch posts from.
        - limit (int): The maximum number of posts to fetch. Defaults to 10.
        - category (str): The category of posts ('hot', 'top', 'new'). Defaults to 'hot'.
        - time_filter (str): The time filter for 'top' posts. Defaults to 'all'.

        Returns:
        - list: A list of dictionaries containing post data.
        """
        if category not in ['hot', 'top','new']:
            raise ValueError("Category must be either 'hot','top' or 'new'")

        batch_size = min(100, limit)  # Set batch size, won't fetch more than 100 at once
        total_fetched = 0
        after = None
        all_posts = []

        # Continue fetching until the desired number of posts is reached
        while total_fetched < limit:
            # Choose the appropriate URL based on category
            if category == 'hot':
                url = f"https://www.reddit.com/r/{subreddit}/hot.json"
            elif category == 'top':  # category == 'top'
                url = f"https://www.reddit.com/r/{subreddit}/top.json"
            else:
                url = f"https://www.reddit.com/r/{subreddit}/new.json"

            params = {
                'limit': batch_size,
                'after': after,
                'raw_json': 1,
                't': time_filter  # Time filter for 'top' category
            }

            response = self.session.get(url, params=params)
            if response.status_code != 200:
                # Handle failed request
                print(f"Failed to fetch data: {response.status_code}")
                return all_posts

            # Parse the response JSON
            data = response.json()
            posts = data['data']['children']

            if not posts:
                break 

            # Extract relevant information from each post
            for post in posts:
                post_data = post['data']
                post_info = {
                    'title': post_data['title'],
                    'author': post_data['author'],
                    'permalink': post_data['permalink'],
                    'score': post_data['score'],
                    'num_comments': post_data['num_comments'],
                    'created_utc': post_data['created_utc']
                }

                # Include image URLs if available
                if post_data.get('post_hint') == 'image' and 'url' in post_data:
                    post_info['image_url'] = post_data['url']
                elif 'preview' in post_data and 'images' in post_data['preview']:
                    post_info['image_url'] = post_data['preview']['images'][0]['source']['url']

                # Include thumbnail if available and not a 'self' post
                if 'thumbnail' in post_data and post_data['thumbnail'] and post_data['thumbnail'] != 'self':
                    post_info['thumbnail_url'] = post_data['thumbnail']
                
                # Append the post information to the list
                all_posts.append(post_info)
                total_fetched += 1
                
                if total_fetched >= limit:
                    break

            # Set 'after' parameter for pagination
            after = data['data'].get('after')
            #print(f"> Posts Fetched: {total_fetched}")

            if not after:
                # Break if no more posts are available
                print("No more posts to fetch.")
                break

            # Avoid rate-limiting by sleeping between requests
            time.sleep(0.5)

        return all_posts[:limit]  # Return the exact number of posts requested



