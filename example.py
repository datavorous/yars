"""
Using this data_hoarder() we can extract massive no of post-data from the subreddits.
It saves in a json file in the following format:

[
    {
        "title": "TITLE_GOES_HERE",
        "author": "AUTHOR_USERNAME",
        "permalink": "/r/SUBREDDIT_NAME/comments/SOME_ID/POST_TITLE/",
        "score": SCORE(INT),
        "num_comments": NO_OF_COMMENTS(INT),
        "created_utc": 1716902623.0
    },
    {
        "title": "TITLE_GOES_HERE",
        "author": "AUTHOR_USERNAME",
        "permalink": "/r/SUBREDDIT_NAME/comments/SOME_ID/POST_TITLE/",
        "score": SCORE(INT),
        "num_comments": NO_OF_COMMENTS(INT),
        "created_utc": 1719949630.0,
        "image_url": "https://i.redd.it/LOLOLOL.png",
        "thumbnail_url": "https://a.thumbs.redditmedia.com/LOLOLOLOL.jpg"
    }
]

NOTE: IMG AND THUMBNAIL ARE ADDED ONLY IF THEY ARE PRESENT
IF THE IMG LINK IS OF SOME EXTERNAL SERVICE, THUMBNAIL LINK IS ONLY RETURNED


Now, you can use RedditMiner, and call the scrape_post_details() function to get Post title, Body Text, and Top Level Comments(around 80-90)

Also, have fun using download_image() of Utils class ;)

"""

import time
from utils import Utils
from reddit_miner import RedditMiner

miner = Utils()

def get_data():
    subreddit = 'all'

    print(f"Target: r/{subreddit}")

    start_time = time.time()

    miner.data_hoarder(subreddit, limit=2500, category='top', output_file="hi.json")
    # Stress Test lesgoo
    print(f"Data from subreddit '{subreddit}' saved."
              f"(Time taken: {time.time() - start_time:.2f} seconds)")


get_data()
# We get the base data of a subreddit

miner.download_image("https://i.redd.it/f58v4g8mwh551.jpg")
# we could have used this alongside the extracted posts data


# This will be useful, i presume
permalink = "/r/developersIndia/comments/1fdmeg5/why_is_php_paid_so_damn_less_in_india_i_cant_bear/"
post_details = miner.scrape_post_details(permalink)

print(f"\nTitle: {post_details['title']}")
print(f"Body: {post_details['body'][:200]}... (Truncated for display)")
print(f"Comments: {len(post_details['comments'])} comments found")
# Get Comments, and Body Text of certain Posts using the permalink   


# Other Utility Stuffs
########################################
username = 'spez'
print(f"Scraping data for user: {username}")
miner.user_osint(username, limit=3000, output_file='user_data.json')
print(f"User data for '{username}' saved to 'user_data.json' ")
# Get posts and comments of a certain user

search_query = "climate change"
print(f"Searching Reddit for: {search_query}...")
search_results = miner.search_reddit(search_query, limit=5)
print(f"Search completed.")
    
for idx, result in enumerate(search_results, start=1):
    print(f"\nResult {idx}:")
    print(f"Title: {result['title']}")
    print(f"Link: {result['link']}")
    print(f"Description: {result['description']}")
# Search on Reddit for Posts related to this
"""