import os
import sys
import asyncio
import threading
import customtkinter as ctk
from tkinter import messagebox, StringVar, filedialog
import builtins
import webbrowser
from urllib.parse import urlparse, parse_qs

# Import your scraper
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from scraper import YellowPagesScraper

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class ScraperApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Yellow Pages Scraper")
        self.geometry("700x550")  # Made taller to accommodate the new field
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Variables
        self.url_var = StringVar(value="https://www.yellowpages.com/search?search_terms=Vacation+Rentals&geo_location_terms=Miami+Beach%2C+FL")
        self.status_var = StringVar(value="Ready")
        self.output_path_var = StringVar()
        self.output_filename_var = StringVar(value="y2.csv")  # Default filename
        self.is_running = False
        self.scraper = None
        self.loop = None
        self.original_print = print  # Store the original print function
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Create widgets
        self.create_widgets()
        
        # Set default output path
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.join(base_dir, "output")
        os.makedirs(self.output_dir, exist_ok=True)
        self.update_output_path()  # Set the initial output path
        
    def update_output_path(self):
        """Update the full output path when filename changes"""
        filename = self.output_filename_var.get().strip()
        if not filename:
            filename = "y2.csv"  # Default name if empty
            self.output_filename_var.set(filename)
        
        # Ensure .csv extension
        if not filename.lower().endswith('.csv'):
            filename += '.csv'
            self.output_filename_var.set(filename)
            
        full_path = os.path.join(self.output_dir, filename)
        self.output_path_var.set(full_path)
        
    def create_widgets(self):
        # Title
        title_label = ctk.CTkLabel(self.main_frame, text="Yellow Pages Scraper", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # URL input
        url_frame = ctk.CTkFrame(self.main_frame)
        url_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        url_frame.grid_columnconfigure(1, weight=1)
        
        url_label = ctk.CTkLabel(url_frame, text="URL:", font=ctk.CTkFont(size=14))
        url_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")
        
        self.url_entry = ctk.CTkEntry(url_frame, textvariable=self.url_var, font=ctk.CTkFont(size=14), width=400)
        self.url_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        
        validate_btn = ctk.CTkButton(url_frame, text="Validate", width=80, command=self.validate_url)
        validate_btn.grid(row=0, column=2, padx=(5, 10), pady=10)
        
        # Output filename - NEW
        filename_frame = ctk.CTkFrame(self.main_frame)
        filename_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        filename_frame.grid_columnconfigure(1, weight=1)
        
        filename_label = ctk.CTkLabel(filename_frame, text="Filename:", font=ctk.CTkFont(size=14))
        filename_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")
        
        self.filename_entry = ctk.CTkEntry(filename_frame, textvariable=self.output_filename_var, font=ctk.CTkFont(size=14))
        self.filename_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        
        # Button to suggest filename based on search terms
        auto_name_btn = ctk.CTkButton(filename_frame, text="Auto Name", width=80, command=self.auto_generate_filename)
        auto_name_btn.grid(row=0, column=2, padx=(5, 10), pady=10)
        
        # Output path (now read-only)
        output_frame = ctk.CTkFrame(self.main_frame)
        output_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        output_frame.grid_columnconfigure(1, weight=1)
        
        output_label = ctk.CTkLabel(output_frame, text="Output Path:", font=ctk.CTkFont(size=14))
        output_label.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")
        
        output_entry = ctk.CTkEntry(output_frame, textvariable=self.output_path_var, font=ctk.CTkFont(size=14), width=400, state="readonly")
        output_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        
        browse_btn = ctk.CTkButton(output_frame, text="Browse", width=80, command=self.browse_output)
        browse_btn.grid(row=0, column=2, padx=(5, 10), pady=10)
        
        # Connect filename changes to update path
        self.output_filename_var.trace_add("write", lambda *args: self.update_output_path())
        
        # Control buttons
        control_frame = ctk.CTkFrame(self.main_frame)
        control_frame.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        control_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.start_btn = ctk.CTkButton(control_frame, text="Start Scraping", font=ctk.CTkFont(size=16), 
                                        fg_color="green", hover_color="dark green", command=self.start_scraping)
        self.start_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.stop_btn = ctk.CTkButton(control_frame, text="Stop", font=ctk.CTkFont(size=16), 
                                      fg_color="red", hover_color="dark red", command=self.stop_scraping, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        open_output_btn = ctk.CTkButton(control_frame, text="Open Results", font=ctk.CTkFont(size=16), command=self.open_output)
        open_output_btn.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        # Log frame
        log_label = ctk.CTkLabel(self.main_frame, text="Log:", font=ctk.CTkFont(size=14, weight="bold"))
        log_label.grid(row=5, column=0, padx=20, pady=(20, 5), sticky="w")
        
        self.log_text = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont(size=12), height=150)
        self.log_text.grid(row=6, column=0, padx=20, pady=(5, 10), sticky="nsew")
        self.main_frame.grid_rowconfigure(6, weight=1)
        
        # Status bar
        status_frame = ctk.CTkFrame(self.main_frame, fg_color=("gray85", "gray25"))
        status_frame.grid(row=7, column=0, padx=20, pady=(5, 10), sticky="ew")
        
        status_label = ctk.CTkLabel(status_frame, textvariable=self.status_var, font=ctk.CTkFont(size=12))
        status_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
    def auto_generate_filename(self):
        """Generate filename based on URL search parameters"""
        url = self.url_var.get().strip()
        
        try:
            parsed = urlparse(url)
            query_params = parse_qs(parsed.query)
            
            # Extract search terms and location
            search_terms = query_params.get('search_terms', [''])[0].replace(' ', '_')
            location = query_params.get('geo_location_terms', [''])[0].replace(' ', '_')
            
            if search_terms and location:
                # Create filename: search_location.csv
                filename = f"{search_terms}_{location}.csv"
                # Clean up characters that shouldn't be in filenames
                for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|', ',']:
                    filename = filename.replace(char, '')
                self.output_filename_var.set(filename)
            else:
                # If can't parse meaningful terms, create a timestamp-based name
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                self.output_filename_var.set(f"yellowpages_{timestamp}.csv")
        except:
            # Default to timestamp if anything goes wrong
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.output_filename_var.set(f"yellowpages_{timestamp}.csv")
            
    def validate_url(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "URL cannot be empty")
            return False
        
        try:
            parsed = urlparse(url)
            if parsed.scheme and parsed.netloc and 'yellowpages.com' in parsed.netloc:
                messagebox.showinfo("Valid URL", "URL is valid and points to Yellow Pages.")
                
                # Suggest filename based on URL parameters
                self.auto_generate_filename()
                
                return True
            else:
                messagebox.showwarning("Warning", "URL may not be valid for Yellow Pages. Please check.")
                return False
        except:
            messagebox.showerror("Error", "Invalid URL format")
            return False
    
    def browse_output(self):
        # Open dialog that starts in the output directory
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir=self.output_dir,
            initialfile=self.output_filename_var.get()
        )
        if filename:
            # Update both the path and extract the filename for the filename field
            self.output_path_var.set(filename)
            new_filename = os.path.basename(filename)
            
            # Update the filename field without triggering update_output_path
            self.output_filename_var.trace_remove("write", self.output_filename_var.trace_info()[0][1])
            self.output_filename_var.set(new_filename)
            self.output_filename_var.trace_add("write", lambda *args: self.update_output_path())
            
            # Update output directory for future use
            self.output_dir = os.path.dirname(filename)
    
    def open_output(self):
        output_path = self.output_path_var.get()
        if not output_path:
            messagebox.showerror("Error", "No output file specified")
            return
            
        if not os.path.exists(output_path):
            messagebox.showerror("Error", f"File does not exist: {output_path}")
            return
            
        # Open the file with the default application
        try:
            if sys.platform == 'win32':
                os.startfile(output_path)
            elif sys.platform == 'darwin':  # macOS
                os.system(f'open "{output_path}"')
            else:  # Linux
                os.system(f'xdg-open "{output_path}"')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {str(e)}")
    
    # Custom print redirection
    def custom_print(self, *args, **kwargs):
        message = " ".join(map(str, args))
        # Use after() to safely update the UI from any thread
        self.after(0, lambda: self._update_log(message))
        # Still print to console using the original print function
        self.original_print(*args, **kwargs)
    
    def _update_log(self, message):
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
    
    async def run_scraper(self):
        url = self.url_var.get().strip()
        # Modify the scraper to use our custom output path
        self.scraper = YellowPagesScraper()
        # Override the filename
        self.scraper.filename = self.output_path_var.get()
        # Close existing file if any
        if hasattr(self.scraper, 'csv_file') and self.scraper.csv_file:
            self.scraper.csv_file.close()
        # Create new CSV file
        file_exists = os.path.isfile(self.scraper.filename)
        self.scraper.csv_file = open(self.scraper.filename, mode="a", newline="", encoding="utf-8")
        self.scraper.writer = csv.writer(self.scraper.csv_file)
        if not file_exists:
            self.scraper.writer.writerow(["Company", "Address", "Phone Number", "Website"])
        
        try:
            self.is_running = True
            self.custom_print(f"Starting scraper with URL: {url}")
            self.custom_print(f"Output file: {self.scraper.filename}")
            self.status_var.set("Scraping in progress...")
            await self.scraper.start(url)
            self.custom_print("Scraping completed successfully!")
            self.status_var.set("Scraping completed")
        except Exception as e:
            self.custom_print(f"Error during scraping: {str(e)}")
            self.status_var.set(f"Error: {str(e)}")
        finally:
            self.is_running = False
            # Use after() to safely update UI from a non-main thread
            self.after(0, self.update_buttons)
    
    def start_scraping(self):
        if self.is_running:
            return
            
        if not self.validate_url():
            return
            
        # Replace the global print function
        global print
        self.original_print = print  # Store the original print function
        print = self.custom_print     # Replace with our custom print
        
        # Update button states
        self.is_running = True
        self.update_buttons()
        
        # Clear log
        self.log_text.delete("1.0", "end")
        
        # Create and run scraper in a separate thread
        def run_async_loop():
            try:
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
                self.loop.run_until_complete(self.run_scraper())
            except Exception as e:
                self.custom_print(f"Fatal error: {str(e)}")
            finally:
                if self.loop and self.loop.is_running():
                    self.loop.close()
                self.loop = None
                global print
                print = self.original_print  # Restore original print
                
                # Update UI from the main thread
                self.after(0, self.after_scraping)
        
        threading.Thread(target=run_async_loop, daemon=True).start()
    
    def after_scraping(self):
        self.is_running = False
        self.update_buttons()
        messagebox.showinfo("Scraping Complete", "The scraping process has finished.")
    
    def stop_scraping(self):
        if not self.is_running or not self.loop:
            return
            
        self.custom_print("Stopping scraper...")
        self.status_var.set("Stopping...")
        
        # Schedule task to stop the loop
        if self.loop and self.loop.is_running():
            asyncio.run_coroutine_threadsafe(self.stop_scraper_async(), self.loop)
    
    async def stop_scraper_async(self):
        # Close the browser if it exists
        if self.scraper and hasattr(self.scraper, 'browser'):
            try:
                await self.scraper.browser.close()
            except:
                pass
        
        # Close file
        if self.scraper and hasattr(self.scraper, 'csv_file'):
            try:
                self.scraper.csv_file.close()
            except:
                pass
    
    def update_buttons(self):
        if self.is_running:
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self.url_entry.configure(state="disabled")
            self.filename_entry.configure(state="disabled")
        else:
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
            self.url_entry.configure(state="normal")
            self.filename_entry.configure(state="normal")
    
    def on_closing(self):
        if self.is_running:
            if messagebox.askyesno("Quit", "Scraping is in progress. Are you sure you want to quit?"):
                self.stop_scraping()
                self.destroy()
        else:
            self.destroy()

if __name__ == "__main__":
    # Fix for high DPI screens
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
        
    # Import csv module needed by the scraper
    import csv
    
    app = ScraperApp()
    app.mainloop()