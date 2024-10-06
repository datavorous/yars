import json
import os
from urllib.parse import urlparse

import requests
from pygments import formatters, highlight, lexers


def display_results(results, title):
    """
    Display the results in a formatted manner using Pygments for syntax highlighting.

    Args:
    results (list or dict): List of dictionaries or a single dictionary containing the results.
    title (str): Title of the results section.
    """
    # Print the title
    print(f"\n{'-'*20} {title} {'-'*20}")

    if isinstance(results, list):
        for item in results:
            if isinstance(item, dict):
                # Format JSON and apply syntax highlighting
                formatted_json = json.dumps(item, sort_keys=True, indent=4)
                colorful_json = highlight(
                    formatted_json,
                    lexers.JsonLexer(),
                    formatters.TerminalFormatter(),
                )
                print(colorful_json)
            else:
                print(item)  # Fallback for non-dict items
            # print("-" * 50)
    elif isinstance(results, dict):
        # Format JSON for a single dictionary result
        formatted_json = json.dumps(results, sort_keys=True, indent=4)
        colorful_json = highlight(
            formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter()
        )
        print(colorful_json)
        # print("-" * 50)
    else:
        print("No results to display.")


def download_image(image_url, output_folder="images", session=None):
    """
    Downloads an image from the specified URL and saves it to the output folder.

    Parameters:
    - image_url (str): The URL of the image to be downloaded.
    - output_folder (str): The folder where the image will be saved. Defaults to 'images'.
    - session (requests.Session): Optional. A requests session to use for downloading the image. Defaults to None.

    Returns:
    - str: The filepath where the image is saved, or None if the download failed.
    """
    os.makedirs(output_folder, exist_ok=True)

    filename = os.path.basename(urlparse(image_url).path)
    filepath = os.path.join(output_folder, filename)

    if session is None:
        session = requests.Session()

    response = session.get(image_url, stream=True)
    if response.status_code == 200:
        with open(filepath, "wb") as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
        print(f"Downloaded: {filepath}")
        return filepath
    else:
        print(f"Failed to download: {image_url}")
        return None
