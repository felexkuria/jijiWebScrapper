import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import requests

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13.4; rv:109.0) Gecko/20100101 Firefox/115.0'
#angie
#base_url = "https://jiji.co.ke/sellerpage-hjrpeqhxrGhcqf3cDjy3wCDJ"

#maggie__household
base_url="https://jiji.co.ke/sellerpage-blpGsvzwLLydTtw3JY0VHBVk"
headers = {'User-Agent': user_agent}

response = requests.get(base_url, headers=headers)
driver = webdriver.Chrome()
driver.get(base_url)
element = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div[2]/div/div[2]/div[2]/div[1]/div[1]/div")

# Extract the text from the element
element_text = element.text

# Check if the text contains non-numeric characters
if not element_text.isdigit():
    # Remove non-numeric characters
    element_text = ''.join(c for c in element_text if c.isdigit())

# Convert to integer
element_number = int(element_text)

# Print the result
print(element_number)
# # Get scroll height
# last_height = driver.execute_script("return document.body.scrollHeight")

# while True:
#     # Scroll down to the bottom
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#     # Wait to load page content
#     time.sleep(SCROLL_PAUSE_TIME)

#     # Calculate new scroll height and compare
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break

#     last_height = new_height
SCROLL_PAUSE_TIME = 1
total_scroll_time = 0

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to the bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page content
    time.sleep(SCROLL_PAUSE_TIME)

    # Update total scroll time
    total_scroll_time += SCROLL_PAUSE_TIME

    # Check if one minute has passed
    if total_scroll_time >= 60*60:
        break

    # Calculate new scroll height and compare
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break

    last_height = new_height
products = []
prices = []
images = []
html_content = driver.page_source
soup = BeautifulSoup(html_content, "lxml")
# for page_number in range(1, 10):
#     url = f"{base_url}?page={page_number}"
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, "lxml")

    # Extract product and price information
for product in soup.find_all("div", class_="b-advert-listing-tile-item__details-title"):
        cleaned_text = re.sub(r"Sponsored.*", "", product.text.strip())
        products.append(cleaned_text)
        totalproducts =len(products)

for price in soup.find_all("div", class_="b-advert-listing-tile-item__details-price"):
       cleaned_price = price.text.strip().replace("KSh ", "")
       prices.append(cleaned_price)
    
for image in soup.find_all("div", class_="b-advert-listing-tile-item__image"):
    # Find the `img` tag within the `div`.
      img_tag = image.find("img")
    # Extract the `src` attribute from the `img` tag.
      image_src = img_tag["src"]
    # Append the image source link to the list.
      images.append(image_src)
       
      #  print(len(images))

# Save results to a CSV file


def get_next_filename(filename):
  """
  Returns the next available filename by appending a number to the original filename.
  """
  i = 1
  while os.path.exists(filename):
    filename = f"{filename[:-4]}{i}.csv"
    i += 1
  return filename

# Get the next available filename
filename = get_next_filename("jiji_products.csv")

# Open the file for writing
with open(filename, "w", newline="", encoding="utf-8") as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(["Product", "Price", "Image"])
  for i in range(len(products)):
    writer.writerow([products[i], prices[i], images[i]])

# Print the filename
print(f"Results saved to {filename}")


# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException

# # Initialize the WebDriver
# driver = webdriver.Chrome()

# # Read the CSV file
# products_df = pd.read_csv("jiji_products.csv")

# # Open the Jumia website
# driver.get("https://www.jumia.co.ke/")

# # Loop through each product name
# for index, row in products_df.iterrows():
#     product_name = row["Product"]

#     # Search for the product
#     search_input = driver.find_element(By.XPATH, "/html/body/div[1]/header/section/form/div/input")
#     search_input.send_keys(product_name)
#     search_input.submit()

#     # Wait for the search results to load
#     driver.implicitly_wait(10)

#     try:
#         # Check for "No results were found" message
#         no_results_element = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div/div[1]/h2"))
#         )
#         products_df.loc[index, "Availability"] = "Not Available"
#         products_df.loc[index, "Total Results"] = 0
#     except TimeoutException:
#         products_df.loc[index, "Availability"] = "Available"
#         # Set Total Results to a reasonable value, such as 1
#         products_df.loc[index, "Total Results"] = 1

#     # Clear the search input and results
#     search_input.clear()
#     driver.find_elements(By.XPATH, "/html/body/div/header/section/form/div/button/svg").click()

# Close the browser
driver.quit()

# Save the updated DataFrame to a new CSV file
# products_df.to_csv("jiji_products_with_jumia_results.csv", index=False)