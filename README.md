# IMDb Web Scraping Project

Welcome to the second article of my web scraping guide. In the first article, I demonstrated how to find, extract, and clean data from a single web page on IMDb. In this article, I'll delve into scraping multiple web pages – a list containing 20 pages and a total of 1,000 movies – using a Python web scraper.


## Overview



- **Import Libraries:** Import the necessary libraries such as `requests`, `BeautifulSoup`, `pandas`, and more.

- **Set Headers:** Set headers to specify our preferred language when making requests.

- **Initialize Empty Lists:** Create empty lists to store movie data.

- **Create a Range of Page Numbers:** We'll use a loop to iterate through pages. This range will be used to generate the page numbers.

- **Loop Through Pages:**
  - Make a request to IMDb's URL for each page.
  - Parse the HTML content using BeautifulSoup.
  - Find movie containers on the page.
  - Introduce sleep periods to control the crawl rate.

- **Extract and Append Data:**
  - Loop through each movie container.
  - Extract the following attributes:
  - Movie Name
  - Append extracted data to respective lists.

- **Create a DataFrame:**
  - Create a DataFrame to store the scraped data.
  - Include columns for movie title, year, IMDb rating, metascore, votes, gross earnings, and runtime.

- **Data Cleaning and Preprocessing:** Implement data cleaning and preprocessing steps.
  - Convert data to appropriate data types.
  - Handle missing data using default values or dropping rows/columns.

- **Save DataFrame to CSV:** Save the cleaned data into a CSV file for further analysis.

## Basic Data-Quality Best Practices (Optional)

- **Handling Missing Data:**
  - Check for missing data using the `.isnull().sum()` method.
  - Consider filling missing values with default values or deleting rows/columns with significant missing data.

- **Data Type Consistency:**
  - Ensure data types are consistent and appropriate for each column.

By following these steps and best practices, you'll create a robust web scraping script that extracts valuable data from multiple pages on IMDb and ensures data quality for analysis.
