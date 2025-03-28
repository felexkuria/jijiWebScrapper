# Jiji Web Scraper

This project is a web scraper designed to extract product information from Jiji and optionally search for products on Jumia. It uses Selenium and BeautifulSoup for web scraping and requires Python to run.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

1. **Python** (version 3.8 or higher)
2. **Google Chrome** (latest version)
3. **ChromeDriver** (compatible with your Chrome version)

## Installation

Follow these steps to set up and run the project:

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Jiji_web_Scrapper
```

### 2. Install Dependencies

Install the required Python libraries using the requirements.txt file:
`pip install -r requirement.txt`

### 3. Set Up ChromeDriver

Download the ChromeDriver that matches your Chrome version from ChromeDriver [Downloads](https://developer.chrome.com/docs/chromedriver/downloads). Place the chromedriver executable in a directory included in your system's PATH or in the project directory.

### 4. Run the Scraper

- BeautifulSoup Scraper
  To scrape product information from Jiji using BeautifulSoup, run:

  ```bash
  python beautifulSoup.py
  ```

- Selenium Scraper
  To search for products on Jumia using Selenium, run:

  ```bash
  python webscraper.py
  ```

- Output
  The scraped product data will be saved in a CSV file named jiji_products.csv or a similar name if the file already exists.
  The Selenium scraper will update the CSV file with product availability and total results from Jumia.
- Notes
  Ensure your internet connection is stable while running the scraper.
  If you encounter issues with ChromeDriver, verify that the version matches your Chrome browser.

License
This project is licensed under the MIT License. See the LICENSE file for details
