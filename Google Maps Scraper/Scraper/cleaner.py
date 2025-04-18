import pandas as pd
import re
import os

class DataCleaner:
    def __init__(self):
        pass

    def clean_description(self, text):
        if isinstance(text, str):
            return text.strip() if text else None
        return None

    def clean_rating(self, rating):
        try:
            if isinstance(rating, str):
                return float(rating.replace(',', '.').strip())
            if isinstance(rating, (int, float)):
                return float(rating)
        except:
            return None
    
    def clean_review(self, review):
        try:
            if isinstance(review, (int, float)):
                return float(str(review).replace('-', ''))

            if isinstance(review, str):
                review = review.replace('(', '').replace(')', '')
                review = review.replace(',', '.').replace('-', '').strip()
                return float(review)
        except Exception as e:
            print(f"Error cleaning review: {review} → {e}")
            return None

    def clean_price(self, price):
        if isinstance(price, str):
            price = price.replace("Â", "").replace("·", "").replace('\xa0', ' ')
            price = price.replace('$$', '').replace('$', '')
            price = re.sub(r'\s+', ' ', price)
            return price.strip() if price else None
        return None

    def clean_phone(self, phone_number):
        if isinstance(phone_number, str):
            return phone_number.strip() if phone_number else None
        return None

    def clean_website(self, website):
        if isinstance(website, str):
            if "business.google.com" in website:
                return None
            if "http" in website:
                return website
        return None

    def clean_data(self, row):
        return [
            self.clean_description(row[0]),  # Name
            self.clean_rating(row[1]),        # Rating
            self.clean_review(row[2]),        # Review
            self.clean_description(row[3]),  # Address
            self.clean_price(row[4]),        # Price
            self.clean_phone(row[5]),        # Phone Number
            self.clean_website(row[6]),      # Website
            self.clean_description(row[7]),   # Description
            self.clean_description(row[8])    # URL
        ]

    def clean_scraped_data(self, input_file_path):
        directory = os.path.dirname(input_file_path)
        filename = os.path.basename(input_file_path)
        output_file_path = os.path.join(directory, f"cleaned_{filename}")
        
        try:
            df = pd.read_csv(input_file_path)
            cleaned_data = df.apply(self.clean_data, axis=1)
            cleaned_df = pd.DataFrame(cleaned_data.tolist(), 
                                     columns=['Name', 'Rating', 'Review', 'Address', 
                                              'Price', 'Phone Number', 'Website', 
                                              'Description', 'URL'])
            cleaned_df = cleaned_df.drop_duplicates()
            cleaned_df = cleaned_df.dropna(subset=['Name'])
            
            # Save cleaned data
            cleaned_df.to_csv(output_file_path, index=False)
            print(f"Successfully cleaned data saved to: {output_file_path}")
            return output_file_path
            
        except Exception as e:
            print(f"Error cleaning data: {str(e)}")
            return None

if __name__ == "__main__":
    input_path = r"C:\Freelance\Scrapy\pw_project\google_maps\output\test_search.csv"
    cleaner = DataCleaner()
    cleaned_file = cleaner.clean_scraped_data(input_path)
    if cleaned_file:
        print(f"Cleaned file created at: {cleaned_file}")