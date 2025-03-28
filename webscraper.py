
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time
from selenium.common.exceptions import WebDriverException

# Initialize the WebDriver
driver = webdriver.Chrome()

# Read the CSV file
products_df = pd.read_csv("jiji_products.csv")

# Open the Jumia website
driver.get("https://www.jumia.co.ke/")

# Loop through each product name
for index, row in products_df.iterrows():
    product_name = row["Product"]

    # Search for the product
    search_input = driver.find_element(By.XPATH, "/html/body/div[1]/header/section/form/div/input")
    search_input.clear()
    time.sleep(1)

    while True:
        try:
            search_input.send_keys(product_name)
            break
        except WebDriverException:
            search_input.clear()
            time.sleep(1)
            product_name = next(products_df["Product"])
            try:
                 search_input.send_keys(product_name)
                 break
                # comment: 
            except WebDriverException:
                search_input.clear()
                time.sleep(1)
                product_name = next(products_df["Product"])
                
            # end try

    search_input.submit()

 
    driver.implicitly_wait(1)

    try:
        # Check for "No results were found" message
        no_results_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/main/div/div[1]/h2"))
        )
        products_df.loc[index, "Availability"] = "Not Available"
        products_df.loc[index, "Total Results"] = 0
    except TimeoutException:
        products_df.loc[index, "Availability"] = "Available"
        # Set Total Results to a reasonable value, such as 1
        products_df.loc[index, "Total Results"] = 1

   # Wait for the reset button to be visible
wait = WebDriverWait(driver, 10)
reset_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@aria-label='Reset']")))

# Click on the reset button
reset_button.click()

# Close the browser after all searches are complete
driver.quit()
