import time
from utils import Utils
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def main():
    # Initialize the Utils class
    miner = Utils()

    # 1. Scrape top 10 hot posts from a subreddit and save to a JSON file
    subreddit = 'EarthPorn'
    print(f"{Fore.GREEN}Starting data hoarding from subreddit: {subreddit}...")
    start_time = time.time()
    miner.data_hoarder(subreddit, limit=10, category='hot', output_file='earthporn_data.json')
    print(f"{Fore.GREEN}Data from subreddit '{subreddit}' saved to 'earthporn_data.json' "
          f"(Time taken: {time.time() - start_time:.2f} seconds)")

    # 2. Download images from the subreddit
    print(f"{Fore.GREEN}Starting image download from subreddit: {subreddit}...")
    start_time = time.time()
    miner.bulk_image_downloader(subreddit, limit=10, category='hot', output_folder='earthporn_images')
    print(f"{Fore.GREEN}Images downloaded from subreddit '{subreddit}' and saved in 'earthporn_images/' "
          f"(Time taken: {time.time() - start_time:.2f} seconds)")

    # 3. Perform OSINT on a Reddit user (example user: 'spez')
    username = 'spez'
    print(f"{Fore.GREEN}Scraping data for user: {username}...")
    start_time = time.time()
    miner.user_osint(username, limit=100, output_file='user_data_spez.json')
    print(f"{Fore.GREEN}User data for '{username}' saved to 'user_data_spez.json' "
          f"(Time taken: {time.time() - start_time:.2f} seconds)")

    # 4. Use Google Search to find Reddit threads on a specific topic
    search_query = "climate change"
    print(f"{Fore.GREEN}Searching Reddit via Google for: {search_query}...")
    start_time = time.time()
    search_results = miner.search_reddit(search_query, limit=5)
    print(f"{Fore.GREEN}Search completed (Time taken: {time.time() - start_time:.2f} seconds)")
    
    for idx, result in enumerate(search_results, start=1):
        print(f"{Fore.CYAN}\nResult {idx}:")
        print(f"{Fore.GREEN}Title: {Fore.WHITE}{result['title']}")
        print(f"{Fore.GREEN}Link: {Fore.WHITE}{result['link']}")
        print(f"{Fore.GREEN}Description: {Fore.WHITE}{result['description']}")

    # 5. Scrape details of a specific post (manually provide a permalink for the example)
    permalink = "/r/developersIndia/comments/1fdmeg5/why_is_php_paid_so_damn_less_in_india_i_cant_bear/"
    print(f"{Fore.GREEN}Scraping post details for: {permalink}...")
    start_time = time.time()
    post_details = miner.scrape_post_details(permalink)
    print(f"{Fore.GREEN}Post details scraped (Time taken: {time.time() - start_time:.2f} seconds)")
    
    # Display post details
    print(f"\n{Fore.CYAN}Title: {Fore.WHITE}{post_details['title']}")
    print(f"{Fore.CYAN}Body: {Fore.WHITE}{post_details['body'][:200]}... (Truncated for display)")
    print(f"{Fore.CYAN}Comments: {Fore.WHITE}{len(post_details['comments'])} comments found")

if __name__ == "__main__":
    main()
