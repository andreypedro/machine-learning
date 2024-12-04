import os
import requests
from bs4 import BeautifulSoup

def fetch_image_urls(query, num_images, user_agent):
    """Fetch image URLs from a search engine."""
    urls = []
    page = 0
    while len(urls) < num_images:
        search_url = f"https://www.google.com/search?q={query}&tbm=isch&ijn={page}"
        headers = {"User-Agent": user_agent}
        response = requests.get(search_url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch URLs for {query}. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        image_elements = soup.find_all("img")

        for img in image_elements:
            if len(urls) >= num_images:
                break
            src = img.get("src")
            if src and src.startswith("http"):
                urls.append(src)

        page += 1

    print(f"Found {len(urls)} image URLs for query '{query}'")
    return urls

def download_images(urls, save_dir):
    """Download images from a list of URLs."""
    os.makedirs("datasets/" + save_dir, exist_ok=True)

    for i, url in enumerate(urls):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                file_path = os.path.join("datasets/" + save_dir, f"image_{i+1}.jpg")
                with open(file_path, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Downloaded: {file_path}")
            else:
                print(f"Failed to download {url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")

# Exemplo de uso
if __name__ == "__main__":
    queries = ["cat", "dog"]
    num_images = 100
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    
    for query in queries:
        urls = fetch_image_urls(query, num_images, user_agent)
        download_images(urls, query + "s")