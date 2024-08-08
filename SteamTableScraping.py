import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the Steam price history page
base_url = "https://steampricehistory.com/popular"
page_number = 1

# Define the structure of the data
data = {
    "Game": [],
    "Current Price": [],
    "Discount": [],
    "Recommendations": []
}

while True:
    # Fetch the page content
    response = requests.get(f"{base_url}?page={page_number}")
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract data from the table
    table = soup.find('table')
    if not table:
        break

    rows = table.find_all('tr')[1:]  # Skip the header row

    for row in rows:
        columns = row.find_all('td')
        game = columns[1].text.strip()
        current_price = columns[2].text.strip()
        discount = columns[3].text.strip()
        recommendations = columns[4].text.strip()

        data["Game"].append(game)
        data["Current Price"].append(current_price)
        data["Discount"].append(discount)
        data["Recommendations"].append(recommendations)

    # Check if there is a next page
    pagination = soup.find('ul', class_='pagination-list')
    if not pagination:
        break
    next_page = pagination.find('a', rel='next')
    if not next_page:
        break

    # Move to the next page
    page_number += 1

# Create a DataFrame
df = pd.DataFrame(data)

# Save DataFrame to an Excel file
excel_file = "steam_prices_games.xlsx"
df.to_excel(excel_file, index=False)

print(f"Data has been saved to {excel_file}")
