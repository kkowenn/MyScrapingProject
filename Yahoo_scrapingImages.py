from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import requests
from bs4 import BeautifulSoup
import csv

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver

def scrape_images(url, num_images, save_dir, csv_file):
    # Ensure the directories exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    csv_dir = os.path.dirname(csv_file)
    if csv_dir and not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

    driver = create_driver()
    driver.get(url)
    time.sleep(2)  # Allow time for the page to load

    images = set()
    last_len = 0
    scroll_attempts = 0
    max_scroll_attempts = 20  # Adjust as needed

    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Image URL'])

        while len(images) < num_images and scroll_attempts < max_scroll_attempts:
            scroll_to_bottom(driver)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            img_tags = soup.find_all('img', {'src': True})

            for img_tag in img_tags:
                img_url = img_tag['src']
                if img_url and img_url.startswith('http') and img_url not in images:
                    images.add(img_url)
                    writer.writerow([img_url])
                    print(f"Scraped image {len(images)}: {img_url}")
                    if len(images) >= num_images:
                        break

            if len(images) == last_len:
                scroll_attempts += 1
            else:
                scroll_attempts = 0
            last_len = len(images)

            if scroll_attempts >= max_scroll_attempts:
                print("Reached maximum scroll attempts, stopping...")
                break

    for count, img_url in enumerate(images):
        save_image(img_url, os.path.join(save_dir, f'image_{count}.jpg'))
        print(f"Downloading image {count + 1}/{num_images}")

    driver.quit()

def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Increase sleep time to allow for more images to load

def save_image(url, filepath):
    try:
        response = requests.get(url)
        with open(filepath, 'wb') as file:
            file.write(response.content)
        print(f'Successfully downloaded {filepath}')
    except Exception as e:
        print(f'Failed to save {filepath}: {e}')

if __name__ == '__main__':
    yahoo_images_url = 'https://th.images.search.yahoo.com/search/images;_ylt=AwrKAVC2YJZm33YF6KidSwx.;_ylu=c2VjA3NlYXJjaARzbGsDYnV0dG9u;_ylc=X1MDMjExNDczNTAwNQRfcgMyBGZyA21jYWZlZQRmcjIDcDpzLHY6aSxtOnNiLXRvcARncHJpZAMEbl9yc2x0AzAEbl9zdWdnAzAEb3JpZ2luA3RoLmltYWdlcy5zZWFyY2gueWFob28uY29tBHBvcwMwBHBxc3RyAwRwcXN0cmwDMARxc3RybAMxOQRxdWVyeQNUaGFpJTIwVGF0dG9vJTIwU3ltYm9scwR0X3N0bXADMTcyMTEzMTIwMw--?p=Thai+Tattoo+Symbols&fr=mcafee&fr2=p%3As%2Cv%3Ai%2Cm%3Asb-top&ei=UTF-8&x=wrt&type=E210TH91215G0'  # Update to a valid URL
    num_images = 500  # Increase the number of images as desired
    save_dir = 'yahoo_images'
    csv_file = 'image_links.csv'

    scrape_images(yahoo_images_url, num_images, save_dir, csv_file)
