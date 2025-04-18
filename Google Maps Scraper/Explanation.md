![Google Maps UI Screenshot](https://github.com/Nickopusan13/Nickopusan-Portofolio/blob/master/Google%20Maps%20Scraper/Image/Google%20Maps%20UI.png?raw=true)
# Google Maps Scraper
## Overview
The Google Maps Scraper is a Python-based tool designed to extract business information from Google Maps based on a user-provided search query (e.g., "restaurants in New York"). It leverages asynchronous web scraping with Playwright, processes the raw data for consistency, and provides a graphical user interface (GUI) built with Tkinter. The scraped data is saved as CSV files, both in raw and cleaned formats, making it ready for analysis or further use.

This project is ideal for users who need structured data from Google Maps, such as business names, ratings, addresses, and websites, without manually collecting it.

Features
Web Scraping: Automates browser interaction with Google Maps using Playwright to collect business data.
Data Cleaning: Formats and removes inconsistencies from the scraped data for better usability.
Graphical User Interface: Offers an intuitive Tkinter-based GUI with a visually appealing starry night background.
Asynchronous Operations: Uses asyncio to handle scraping tasks efficiently, keeping the UI responsive.
Components
The project is split into three main files, each with a specific role:

1. main.py
Purpose: Serves as the entry point of the application, managing the GUI and coordinating the scraping and cleaning processes.

StarryBackground Class:
Creates a canvas with a black background, twinkling stars, and a moon with craters for aesthetic appeal.
Stars twinkle randomly every 500 milliseconds to enhance the user experience.
ScraperApp Class:
UI Setup: Initializes a window with:
A search entry field for the user to input a query.
A "Start Scraping" button to begin the process.
A status label at the bottom to display progress or results.
Scraping Trigger: When the button is clicked, the start_scraping method:
Validates the search term (ensures it’s not empty).
Disables the button to prevent multiple runs.
Starts a separate thread for the scraping task to avoid freezing the GUI.
Asynchronous Task Management: The run_scraping_task method:
Uses asyncio.run to execute the async_scrape function.
Instantiates a GoogleMapsScraper object to scrape data.
Calls a DataCleaner object to clean the scraped data.
Updates the UI with success messages (file paths) or errors via a status queue.
Feedback: Displays pop-up messages for success or failure and resets the UI when done.
2. scraper.py
Purpose: Contains the GoogleMapsScraper class, which handles the core web scraping logic using Playwright.

Initialization:
Sets up an output directory (output) and a set (seen_names) to track unique business names and avoid duplicates.
Defines the base URL as https://www.google.com/maps?hl=en.
CSV Handling:
Creates a CSV file named after the sanitized search query (e.g., restaurants_in_New_York.csv).
Writes headers: Name, Rating, Review, Address, Price, Phone Number, Website, Description, URL.
Scraping Process (start_url method):
Launches a headless Chromium browser with Playwright.
Navigates to Google Maps, inputs the search query, and submits it.
Waits for search results to load and scrolls through them to ensure all items are visible.
Scrolling Logic (scroll_page method):
Scrolls the results feed incrementally until the "end of page" message appears.
Triggers the get_data method to extract data from loaded items.
Data Extraction (get_data method):
Identifies all business listings on the page.
For each item:
Clicks to open its details.
Extracts fields like name, rating, review count, address, price, phone number, website, description, and URL using CSS selectors.
Skips duplicates based on the business name.
Writes the data to the CSV file.
Includes a progress callback to update the GUI with the current business being scraped.
3. cleaner.py
Purpose: Contains the DataCleaner class, which processes and refines the raw scraped data.

Cleaning Functions:
clean_description: Strips whitespace from text fields or returns None if empty.
clean_rating: Converts ratings to floats, handling commas or invalid formats.
clean_review: Extracts numeric review counts, removing parentheses and hyphens.
clean_price: Removes currency symbols and extra spaces from price data.
clean_phone: Strips whitespace from phone numbers.
clean_website: Filters out invalid URLs (e.g., Google business links) and ensures proper format.
Data Processing (clean_scraped_data method):
Reads the raw CSV file using Pandas.
Applies cleaning functions to each row.
Removes duplicate rows and entries missing a name.
Saves the cleaned data to a new file prefixed with cleaned_ (e.g., cleaned_restaurants_in_New_York.csv).
Usage
Run the Application:
Execute python main.py to launch the GUI.
Enter Search Term:
Type a query (e.g., "cafes in San Francisco") into the search field.
Start Scraping:
Click "Start Scraping" to begin.
Monitor Progress:
Watch the status bar for updates (e.g., "Scraping Starbucks...").
View Results:
On completion, a pop-up shows the paths to the raw and cleaned CSV files (e.g., output/restaurants.csv and output/cleaned_restaurants.csv).
