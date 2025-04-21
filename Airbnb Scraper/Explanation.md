!['User Interface'](https://github.com/Nickopusan13/Nickopusan-Project/blob/master/Airbnb%20Scraper/image/UI.png)
# Airbnb Scraper
This project is a Python-based web scraper designed to extract detailed information from Airbnb listings. Users can specify a search location, scrape multiple pages of listings, and save the data to a Google Sheet. The project combines web automation, data processing, and a user-friendly graphical interface to streamline the scraping process.

## Project Structure
The project is organized into three main Python files:
- [`scraper.py`](scraper/scraper.py): Handles the core web scraping functionality.
- [`cleaner.py`](scraper/cleaner.py): Provides utility functions to clean and process the scraped data.
- [`main.py`](scraper/main.py): Offers a graphical user interface (GUI) for interacting with the scraper.
### 1. scraper.py
This file contains the `AirbnbScraper` class, which is responsible for scraping data from Airbnb. It uses the following libraries:
- `playwright`: For browser automation and scraping.
- `gspread`: For saving data to Google Sheets.
- `oauth2client`: For Google API authentication.

**Key Features**:
- **Authentication**: Logs into Airbnb using credentials stored in a .env file.
- **Search**: Performs a search for listings based on a user-specified location.
- **Data Extraction**: Scrapes detailed information from each listing, including:
  - Title and short description
  - Price and discounts
  - Host details
  - Reviews and ratings
  - Guest capacity, bedrooms, beds, and baths
  - Amenities (available and unavailable)
  - House rules and additional rules
  - Safety and property information
  - Listing URL and image URL
- **Pagination**: Navigates through multiple pages of search results (up to a user-defined maximum).
- **Concurrency**: Uses asynchronous scraping with a configurable concurrency level to process multiple listings simultaneously.
- **Data Storage**: Writes the scraped data to a Google Sheet, with columns predefined for all extracted fields.
The scraper also includes error handling, logging, and a stop mechanism to gracefully halt the process if needed.

### 2. cleaner.py
This file provides utility functions to process and clean the raw data scraped from Airbnb, ensuring it’s consistent and usable. It relies on regular expressions (re) for text manipulation.
**Key Functions**:
- `clean_text`: Removes unnecessary characters, whitespace, and newlines from text.
- `clean_hosted_by`: Extracts the host’s name from "Hosted by" text.
- `clean_rules`: Parses house rules and additional rules into separate lists, removing duplicates and formatting them as comma-separated strings.
- `clean_amenities`: Categorizes amenities into "available" and "unavailable" lists, handling special cases like "Unavailable:" prefixes.
- `extract_number`: Extracts numeric values (e.g., number of guests or beds) from text.
- `extract_rating`: Pulls out rating scores (e.g., "4.85") from text.
These functions are called by `scraper.py` to preprocess data before saving it to the Google Sheet.

### 3. main.py
This file creates a graphical user interface (GUI) using `tkinter`, allowing users to configure and run the scraper without modifying code. It features a modern Monokai-inspired theme for a polished look.
**Key Features**:

Input Fields: Users can specify:
Search location (e.g., "New York")
Maximum number of pages to scrape
Google Sheet name for data storage
Concurrency level (number of simultaneous scraping tasks)
Delay between requests (in seconds)
Controls: Buttons to start and stop the scraping process.
Real-Time Feedback: Displays logs (e.g., progress, errors) and status updates (e.g., "Scraping in progress").
Threading: Runs the scraper in a separate thread to keep the GUI responsive.
The GUI validates inputs, provides color-coded status indicators, and supports log clearing for a clean user experience.
