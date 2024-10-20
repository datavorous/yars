import json
import os
import sys

# Set up paths to access source files
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_path = os.path.join(project_root, "src")
sys.path.append(src_path)

# Import necessary modules from YARS
from yars.yars import YARS
from yars.utils import display_results, download_image

# Initialize the YARS Reddit miner
miner = YARS()
DEFAULT_FILENAME = "subreddit_data.json"


# Fetch and display top posts from a subreddit
def display_subreddit_posts(miner, subreddit, limit=5):
    """Fetch and display top subreddit posts."""
    posts = miner.fetch_subreddit_posts(
        subreddit, limit=limit, category="new", time_filter="week"
    )
    display_results(posts, "Top Posts")


# Fetch subreddit post details and comments, then save them to a JSON file
def save_subreddit_data(subreddit, limit=5, filename=DEFAULT_FILENAME):
    """Scrape subreddit data, including post details and comments, and save to a JSON file."""
    try:
        posts = miner.fetch_subreddit_posts(subreddit, limit=limit, category="top", time_filter="all")
        filepath = os.path.join(current_dir, filename)

        # Load existing data if available
        try:
            with open(filename, "r") as json_file:
                existing_data = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        for i, post in enumerate(posts, 1):
            permalink = post["permalink"]
            post_details = miner.scrape_post_details(permalink)
            print(f"Processing post {i}")

            if post_details:
                post_data = {
                    "title": post.get("title", ""),
                    "author": post.get("author", ""),
                    "created_utc": post.get("created_utc", ""),
                    "num_comments": post.get("num_comments", 0),
                    "score": post.get("score", 0),
                    "permalink": post.get("permalink", ""),
                    "image_url": post.get("image_url", ""),
                    "thumbnail_url": post.get("thumbnail_url", ""),
                    "body": post_details.get("body", ""),
                    "comments": post_details.get("comments", []),
                }

                # Append new post data to existing data
                existing_data.append(post_data)

                # Save data incrementally to JSON
                save_json_data(existing_data, filepath)
            else:
                print(f"Failed to scrape details for post: {post['title']}")

    except Exception as e:
        print(f"Error occurred while scraping subreddit: {e}")


# Save data to a JSON file
def save_json_data(data, filepath):
    """Save data to a JSON file."""
    try:
        with open(filepath, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully saved to {filepath}")
    except Exception as e:
        print(f"Error saving data to JSON file: {e}")


# Download images from subreddit posts
def download_subreddit_images(miner, subreddit, limit=5):
    """Download images from subreddit posts."""
    posts = miner.fetch_subreddit_posts(subreddit, limit=limit, category="new", time_filter="week")
    for idx, post in enumerate(posts[:3]):
        try:
            image_url = post.get("image_url", post.get("thumbnail_url", ""))
            if image_url:
                print(f"Downloading image from post {idx + 1}: {image_url}")
                download_image(image_url)
        except Exception as e:
            print(f"Error downloading image from post {idx + 1}: {e}")


# Fetch and display search results
def display_search_results(miner, query, limit=5):
    """Fetch and display search results."""
    results = miner.search_reddit(query, limit=limit)
    display_results(results, "Search Results")


# Fetch and display user data
def display_user_data(miner, username, limit=5):
    """Fetch and display Reddit user data."""
    user_data = miner.scrape_user_data(username, limit=limit)
    display_results(user_data, "User Data")


# Fetch and display post comments using a permalink
def display_post_comments(miner, permalink, limit=5):
    permalink = permalink.split("reddit.com")[1]
    post_details = miner.scrape_post_details(permalink)
    if post_details:
        display_results(post_details, "POST DATA")
    else:
        print("Failed to scrape post details.")

# Main execution
if __name__ == "__main__":
    subreddit = "pics"
    search_query = "OpenAI"
    username = "iamsecb"
    permalink = "https://www.reddit.com/r/getdisciplined/comments/1frb5ib/what_single_health_test_or_practice_has/"

    # Display subreddit data
    display_subreddit_posts(miner, subreddit, limit=3)

    # Scrape and save subreddit data to JSON
    save_subreddit_data(subreddit, limit=3)

    # Download images from subreddit posts
    download_subreddit_images(miner, subreddit, limit=3)

    # Display search results
    display_search_results(miner, search_query, limit=3)

    # Display user data
    display_user_data(miner, username, limit=3)

    # Display post comments
    display_post_comments(miner, permalink, limit=3)

