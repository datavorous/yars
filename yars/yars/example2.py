import json

from yars import YARS

# Initialize the YARS Reddit miner
miner = YARS()
filename = "subreddit_data3.json"


# Function to scrape post details and comments from a given subreddit
def scrape_subreddit_data(subreddit_name, limit=5, filename=filename):
    try:
        # Fetch recent posts from the subreddit
        subreddit_posts = miner.fetch_subreddit_posts(
            subreddit_name, limit=limit, category="top", time_filter="all"
        )

        # Load existing data from JSON file if it exists
        try:
            with open(filename, "r") as json_file:
                existing_data = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = []

        a = 1
        # Scrape details and comments for each post
        for post in subreddit_posts:
            permalink = post["permalink"]
            post_details = miner.scrape_post_details(permalink)
            print("pong ", a)
            a += 1

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

                # Append the new post data to the existing data
                existing_data.append(post_data)

                # Save the data incrementally to the JSON file
                save_to_json(existing_data, filename)
            else:
                print(f"Failed to scrape details for post: {post['title']}")

    except Exception as e:
        print(f"Error occurred while scraping subreddit: {e}")


# Function to save post data to a JSON file
def save_to_json(data, filename=filename):
    try:
        with open(filename, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving data to JSON file: {e}")


# Scrape the desired subreddit (example: 'nosleep')
subreddit_name = "wbjee"
scrape_subreddit_data(subreddit_name, limit=3)
