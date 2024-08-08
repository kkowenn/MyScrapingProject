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

def scrape_pinterest_images(url, num_images, save_dir, csv_file):
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
                if img_url and img_url.startswith('http') and '236x' in img_url and img_url not in images:
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

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

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
    pinterest_url = 'https://www.pinterest.com/search/pins/?q=thai%20tattoo&rs=typed'
    num_images = 500  # Increase the number of images as desired
    save_dir = 'final_project/pinterest_images'
    csv_file = 'final_project/image_links.csv'

    scrape_pinterest_images(pinterest_url, num_images, save_dir, csv_file)
