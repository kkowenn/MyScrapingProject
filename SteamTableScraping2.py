from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from bs4 import BeautifulSoup

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.headless = True  # Run in headless mode
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# URL to scrape
url = "https://steamdb.info/charts/?sort=24h"
driver.get(url)

# Function to extract data from the current page
def extract_data():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table')
    if table is None:
        raise Exception("Failed to find the table with class 'table'")
    headers = [th.text.strip() for th in table.find('thead').find_all('th')]
    rows = table.find('tbody').find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        data.append([col.text.strip() for col in cols])
    return pd.DataFrame(data, columns=headers)

# Initialize empty DataFrame to store all data
all_data = pd.DataFrame()

# Loop through pages and extract data
while True:
    # Extract data from the current page and append to all_data
    df = extract_data()
    all_data = pd.concat([all_data, df], ignore_index=True)

    try:
        # Find and click the "Next" button
        next_button = driver.find_element(By.XPATH, "//button[@class='dt-paging-button next']")
        if 'disabled' in next_button.get_attribute('class'):
            break
        next_button.click()
        # Wait for the new page to load
        WebDriverWait(driver, 10).until(EC.staleness_of(next_button))
    except:
        break

# Close the WebDriver
driver.quit()

# Select relevant columns
all_data = all_data[['Name', 'Current', '24h Peak', 'All-Time Peak']]

# Remove commas and convert columns to numeric for proper sorting
all_data['Current'] = pd.to_numeric(all_data['Current'].str.replace(',', ''), errors='coerce')
all_data['24h Peak'] = pd.to_numeric(all_data['24h Peak'].str.replace(',', ''), errors='coerce')
all_data['All-Time Peak'] = pd.to_numeric(all_data['All-Time Peak'].str.replace(',', ''), errors='coerce')

# Sort the DataFrame by 'Current' column in descending order
all_data = all_data.sort_values(by='Current', ascending=False)

# Save DataFrame to an Excel file
excel_file_path = 'steam_charts.xlsx'
all_data.to_excel(excel_file_path, index=False)

print(f"Data saved to {excel_file_path}")
