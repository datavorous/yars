<div align="center">
  
<img src="logo.svg" width="10%">

# YARS (Yet Another Reddit Scraper)

[![GitHub stars](https://img.shields.io/github/stars/datavorous/yars.svg?style=social&label=Stars&style=plastic)](https://github.com/datavorous/yars/stargazers)<br>

</div>

YARS is a Python package designed to simplify the process of scraping Reddit for posts, comments, user data, and other media. The package also includes utility functions. It is built using **Python** and relies on the **requests** module for fetching data from Reddit’s public API. The scraper uses simple `.json` requests, avoiding the need for official Reddit API keys, making it lightweight and easy to use.

## Features

- **Reddit Search**: Search Reddit for posts using a keyword query.
- **Post Scraping**: Scrape post details, including title, body, and comments.
- **User Data Scraping**: Fetch recent activity (posts and comments) of a Reddit user.
- **Subreddit Posts Fetching**: Retrieve posts from specific subreddits with flexible options for category and time filters.
- **Image Downloading**: Download images from posts.
- **Results Display**: Utilize `Pygments` for colorful display of JSON-formatted results.

> [!WARNING]
> Use with rotating proxies, or Reddit might gift you with an IP ban.  
> I could extract max 2552 posts at once from 'r/all' using this.  
> [Here](https://files.catbox.moe/zdra2i.json) is a **7.1 MB JSON** file containing the top 100 posts from 'r/nosleep', which included post titles, body text, all comments and their replies, post scores, time of upload etc.

## Dependencies

- `requests`
- `Pygments`

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/datavorous/YARS.git
   cd yars
   cd yars
   ```

2. Install Poetry (if not already installed):

   ```
   pip install poetry
   poetry shell
   ```

3. Install dependencies using Poetry:

   ```
   poetry install
   ```

4. Run the application:
   ```
   cd yars
   poetry run python example.py
   ```

## Usage

We will use the following Python script to demonstrate the functionality of the scraper. The script includes:

- Searching Reddit
- Scraping post details
- Fetching user data
- Retrieving subreddit posts
- Downloading images from posts

#### Code Overview

```python
from yars import YARS
from utils import display_results, download_image

miner = YARS()
```

#### Step 1: Searching Reddit

The `search_reddit` method allows you to search Reddit using a query string. Here, we search for posts containing "OpenAI" and limit the results to 3 posts. The `display_results` function is used to present the results in a formatted way.

```python
search_results = miner.search_reddit("OpenAI", limit=3)
display_results(search_results, "SEARCH")
```

#### Step 2: Scraping Post Details

Next, we scrape details of a specific Reddit post by passing its permalink. If the post details are successfully retrieved, they are displayed using `display_results`. Otherwise, an error message is printed.

```python
permalink = "https://www.reddit.com/r/getdisciplined/comments/1frb5ib/what_single_health_test_or_practice_has/".split('reddit.com')[1]
post_details = miner.scrape_post_details(permalink)
if post_details:
    display_results(post_details, "POST DATA")
else:
    print("Failed to scrape post details.")
```

#### Step 3: Fetching User Data

We can also retrieve a Reddit user’s recent activity (posts and comments) using the `scrape_user_data` method. Here, we fetch data for the user `iamsecb` and limit the results to 2 items.

```python
user_data = miner.scrape_user_data("iamsecb", limit=2)
display_results(user_data, "USER DATA")
```

#### Step 4: Fetching Subreddit Posts

The `fetch_subreddit_posts` method retrieves posts from a specified subreddit. In this example, we fetch 11 top posts from the "generative" subreddit from the past week.

```python
subreddit_posts = miner.fetch_subreddit_posts("generative", limit=11, category="top", time_filter="week")
display_results(subreddit_posts, "EarthPorn SUBREDDIT New Posts")
```

#### Step 5: Downloading Images

For the posts retrieved from the subreddit, we try to download their associated images. The `download_image` function is used for this. If the post doesn't have an `image_url`, the thumbnail URL is used as a fallback.

```python
for z in range(3):
    try:
        image_url = subreddit_posts[z]["image_url"]
    except:
        image_url = subreddit_posts[z]["thumbnail_url"]
    download_image(image_url)
```

### Complete Code Example

```python
from yars import YARS
from utils import display_results, download_image

miner = YARS()

# Search for posts related to "OpenAI"
search_results = miner.search_reddit("OpenAI", limit=3)
display_results(search_results, "SEARCH")

# Scrape post details using its permalink
permalink = "https://www.reddit.com/r/getdisciplined/comments/1frb5ib/what_single_health_test_or_practice_has/".split('reddit.com')[1]
post_details = miner.scrape_post_details(permalink)
if post_details:
    display_results(post_details, "POST DATA")
else:
    print("Failed to scrape post details.")

# Fetch recent activity of user "iamsecb"
user_data = miner.scrape_user_data("iamsecb", limit=2)
display_results(user_data, "USER DATA")

# Fetch top posts from the subreddit "generative" from the past week
subreddit_posts = miner.fetch_subreddit_posts("generative", limit=11, category="top", time_filter="week")
display_results(subreddit_posts, "EarthPorn SUBREDDIT New Posts")

# Download images from the fetched posts
for z in range(3):
    try:
        image_url = subreddit_posts[z]["image_url"]
    except:
        image_url = subreddit_posts[z]["thumbnail_url"]
    download_image(image_url)
```

You can now use these techniques to explore and scrape data from Reddit programmatically.

# Docs

## Class: YARS

A class to interact with Reddit's API and perform various operations such as searching for posts,
scraping post details, fetching user data, and retrieving posts from specific subreddits using the age old .json trick.

### `__init__(self, user_agent=get_random_user_agent(), proxy=None)`

Initialize the YARS scraper with a custom user agent and optional proxy configuration.

- **user_agent** (str): Custom user agent for requests.
- **proxy** (str): Optional proxy URL.

### `set_uer_agent(self, user_agent)`

Update user agent for requests.

- **user_agent** (str): Custom user agent for requests.

### `set_random_user_agent(self)`

Set a random user agent for requests.

### `search_reddit(self, query, limit=10, after=None, before=None)`

Search Reddit for posts matching the query.

- **query** (str): Search query string.
- **limit** (int): Max number of posts (default 10).
- **after** (str): Fetch results after this ID.
- **before** (str): Fetch results before this ID.
- **random_agent** (bool): Use a random user agent for requests.

### `scrape_post_details(self, permalink)`

Retrieve detailed information about a Reddit post.

- **permalink** (str): The permalink to the post.

- Returns a dictionary with:
  - **title** (str): The post title.
  - **body** (str): The post body.
  - **comments** (list): A list of comments.

### `_extract_comments(self, comments)`

Recursively extract comments and their replies from a Reddit post.

- **comments** (list): List of comments.

- Returns a list of comments and their replies.

### `scrape_user_data(self, username, limit=10)`

Fetch recent activity (posts/comments) of a user.

- **username** (str): Reddit username.
- **limit** (int): Max number of items (default 10).
- Returns a list of posts and comments.

### `fetch_subreddit_posts(self, subreddit, limit=10, category='hot', time_filter='all')`

Fetch posts from a subreddit based on category and time filter.

- **subreddit** (str): The subreddit to fetch from.
- **limit** (int): Max number of posts.
- **category** (str): Type of posts ('hot', 'top', 'new').
- **time_filter** (str): Time filter for top posts (default 'all').

## Utility Functions

### `display_results(results, title)`

Displays search or scrape results in a formatted, syntax-highlighted manner using Pygments.

- **results** (dict): The results to display.
- **title** (str): The title of the results.

### `download_image(image_url, output_folder='images', session=None)`

Downloads an image from the provided URL and saves it in the specified output folder.

- **image_url** (str): URL of the image to download.
- **output_folder** (str): Folder to save the image.
- **session** (requests.Session): Optional requests session.

### `export_json(data, filename='output.json')`

Export data to a JSON file.

- **data** (dict): Data to export.
- **filename** (str): Output filename.

### `export_csv(data, filename='output.csv')`

Export data to a CSV file.

- **data** (dict): Data to export.
- **filename** (str): Output filename.

## Contributing

Contributions are welcome! For feature requests, bug reports, or questions, please open an issue. If you would like to contribute code, please open a pull request with your changes.

### Our Notable Contributors

<a href="https://github.com/datavorous/yars/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=datavorous/yars" />
</a>