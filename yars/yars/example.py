from yars import YARS
from utils import display_results, download_image

miner = YARS()

search_results = miner.search_reddit("OpenAI", limit=3)
display_results(search_results, "SEARCH")
    

permalink = "https://www.reddit.com/r/getdisciplined/comments/1frb5ib/what_single_health_test_or_practice_has/".split('reddit.com')[1]
post_details = miner.scrape_post_details(permalink)
if post_details:
    display_results(post_details, "POST DATA")
else:
    print("Failed to scrape post details.")


user_data = miner.scrape_user_data("iamsecb", limit=2)
display_results(user_data, "USER DATA")


subreddit_posts = miner.fetch_subreddit_posts("generative", limit=10, category="new", time_filter="week")
display_results(subreddit_posts, "SUBREDDIT Top Posts")

for z in range(3):
    try:
        image_url = subreddit_posts[z]["image_url"]
    except:
        image_url = subreddit_posts[z]["thumbnail_url"]
    download_image(image_url)


