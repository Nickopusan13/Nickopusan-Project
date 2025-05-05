# Yellow Pages Scraper
This project is a Python-based web scraper designed to extract business listings from Yellow Pages. It uses Playwright for browser automation and features a user-friendly graphical interface to streamline the scraping process.

## Project Structure
The project is organized into four main Python files:
- [`middlewares.py`](scraper/middlewares.py): Handles fetching random headers and user agents.
- [`cleaner.py`](scraper/cleaner.py): Provides utility functions to clean and process the scraped data.
- [`scraper.py`](scraper/scraper.py): Contains the core web scraping functionality.  
- [`main.py`](scraper/main.py): Offers a graphical user interface (GUI) for interacting with the scraper.

### 1. middlewares.py
This file contains the `Middlewares` class, which is responsible for fetching random headers and user agents from the ScrapeOps API. It uses the following libraries:
- Standard Python libraries for HTTP requests.  
**Key Features**:  
- **get_random_headers()**: Fetches random browser headers and user agents. It attempts up to three times in case of failures and falls back to a default user agent if unsuccessful.  
### 2. cleaner.py
This file provides utility functions to process and clean the raw data scraped from Yellow Pages, ensuring it’s consistent and usable. It relies on regular expressions (re) for text manipulation.  
**Key Functions**:
- `clean_phone(text)`: Cleans and formats phone numbers extracted from the website into a standard (XXX) XXX-XXXX format.
### 3. scraper.py
This file contains the `YellowPagesScraper` class, which handles the core scraping logic. It uses the following libraries:
- `playwright`: For browser automation and scraping.
**Key Features**:
- **Initialization**: Sets up the output CSV file and prepares it for writing data.
- **Scraping Loop**: Navigates to the given URL, applies stealth techniques, and parses the page for business listings.
- **Data Extraction**: Scrapes detailed information from each listing, including:  
    - Company name  
    - Address
    - Phone number
    - Website
- **Pagination**: Follows "next page" links to scrape multiple pages.
- **Error Handling**: Saves HTML to a debug file if an unknown page layout is encountered.
- **Data Storage**: Writes the scraped data to a CSV file, with columns predefined for all extracted fields.
### 4. main.py
This file creates a graphical user interface (GUI) using `CustomTkinter`, allowing users to configure and run the scraper without modifying code. It features a modern look and feel.
**Key Features**:
- **Input Fields**: Users can specify:
    - Yellow Pages search URL
    - Output filename
- **Controls**: Buttons to start, stop, and open the scraping results.
- **Real-Time Feedback**: Displays logs (e.g., progress, errors) and status updates (e.g., "Scraping in progress").
- **Threading**: Runs the scraper in a separate thread to keep the GUI responsive.

## Usage
1. **Run the Application**: Execute `python main.py` to launch the GUI.
2. **Enter URL**: Input the Yellow Pages search URL.
3. **Validate URL**: Optionally, validate the URL to ensure it points to Yellow Pages.
4. **Set Filename**: The application suggests a filename based on the search terms, or you can specify your own.
5. **Start Scraping**: Click "Start Scraping" to begin the process.
6. **Monitor Progress**: View real-time logs in the GUI.
7. **Open Results**: Once completed, click "Open Results" to view the CSV file.

## Example
- **Search URL**: `https://www.yellowpages.com/search?search_terms=Vacation+Rentals&geo_location_terms=Miami+Beach%2C+FL`
- **Output**: A CSV file containing business listings with columns for Company, Address, Phone Number, and Website.

## Notes
- The scraper uses random headers and user agents to avoid detection.
- It handles different page layouts by checking for specific selectors.  
- Users should respect Yellow Pages' terms of service and robots.txt.
