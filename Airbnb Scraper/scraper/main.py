import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from scraper import AirbnbScraper
import asyncio

class MonokaiTheme:
    BG = "#272822"
    CARD_BG = "#1E1F1C"
    TEXT = "#F8F8F2"
    INPUT_BG = "#3E3D32"
    ACCENT = "#A6E22E"
    SECONDARY = "#FD971F"
    TERTIARY = "#66D9EF"
    QUATERNARY = "#F92672"
    BORDER = "#49483E"
    ERROR = "#F92672"
    SUCCESS = "#A6E22E" 
    WARNING = "#E6DB74"

class ModernAirbnbScraperUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Airbnb Scraper")
        self.geometry("900x650")
        
        # Store scraper thread and stop event
        self.scraper_thread = None
        self.stop_event = threading.Event()
        
        # Apply monokai theme
        self.configure(bg=MonokaiTheme.BG)
        self.apply_theme()
        self.create_widgets()
    
    def apply_theme(self):
        self.style = ttk.Style()
        
        # Configure common styles
        self.style.configure("TFrame", background=MonokaiTheme.BG)
        self.style.configure("TLabel", background=MonokaiTheme.BG, foreground=MonokaiTheme.TEXT)
        self.style.configure("TLabelframe", background=MonokaiTheme.BG, foreground=MonokaiTheme.TEXT)
        self.style.configure("TLabelframe.Label", background=MonokaiTheme.BG, foreground=MonokaiTheme.TERTIARY, font=("Helvetica", 10, "bold"))
        
        # Configure button styles
        self.style.configure("Primary.TButton", 
                            background=MonokaiTheme.ACCENT, 
                            foreground=MonokaiTheme.BG,
                            font=("Helvetica", 9, "bold"))
        self.style.map("Primary.TButton",
                      background=[('active', MonokaiTheme.WARNING)],
                      foreground=[('active', MonokaiTheme.BG)])
        
        self.style.configure("Danger.TButton", 
                            background=MonokaiTheme.QUATERNARY, 
                            foreground=MonokaiTheme.TEXT,
                            font=("Helvetica", 9, "bold"))
        self.style.map("Danger.TButton",
                      background=[('active', '#FF8A99')],
                      foreground=[('active', MonokaiTheme.BG)])
        
        # Secondary actions style
        self.style.configure("Secondary.TButton", 
                            background=MonokaiTheme.TERTIARY, 
                            foreground=MonokaiTheme.BG,
                            font=("Helvetica", 9, "bold"))
        self.style.map("Secondary.TButton",
                      background=[('active', '#A0E0FF')],
                      foreground=[('active', MonokaiTheme.BG)])
    
    def create_widgets(self):
        main_frame = ttk.Frame(self, style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title with monokai colors
        title_label = ttk.Label(main_frame, 
                               text="AIRBNB SCRAPER", 
                               font=("Consolas", 18, "bold"), 
                               foreground=MonokaiTheme.QUATERNARY)
        title_label.pack(pady=(0, 20))
        
        # Add subtitle
        subtitle = ttk.Label(main_frame, 
                            text="Hello there! Let's scrape some listings.", 
                            font=("Consolas", 10, "italic"), 
                            foreground=MonokaiTheme.SECONDARY)
        subtitle.pack(pady=(0, 15))
        
        # Input frame with monokai styling
        input_frame = ttk.LabelFrame(main_frame, text="SCRAPING PARAMETERS", style="TLabelframe")
        input_frame.pack(fill=tk.X, pady=10)
        
        param_frame = ttk.Frame(input_frame)
        param_frame.pack(fill=tk.X, padx=15, pady=15)
        
        # Define consistent label style
        label_style = {"foreground": MonokaiTheme.TERTIARY, "font": ("Consolas", 9)}
        entry_style = {"bg": MonokaiTheme.INPUT_BG, 
                      "fg": MonokaiTheme.TEXT, 
                      "insertbackground": MonokaiTheme.ACCENT, 
                      "relief": tk.FLAT, 
                      "borderwidth": 1,
                      "highlightthickness": 1,
                      "highlightcolor": MonokaiTheme.SECONDARY,
                      "highlightbackground": MonokaiTheme.BORDER,
                      "font": ("Consolas", 9)}
        
        # First row
        ttk.Label(param_frame, text="Search Location:", **label_style).grid(row=0, column=0, sticky="w", pady=8)
        self.search_location = tk.Entry(param_frame, width=30, **entry_style)
        self.search_location.grid(row=0, column=1, padx=15, pady=8, sticky="ew")
        self.search_location.insert(0, "")
        
        ttk.Label(param_frame, text="Google Sheet Name:", **label_style).grid(row=0, column=2, sticky="w", padx=(15, 0), pady=8)
        self.sheet_name = tk.Entry(param_frame, width=30, **entry_style)
        self.sheet_name.grid(row=0, column=3, padx=15, pady=8, sticky="ew")
        self.sheet_name.insert(0, "Airbnb Listings")
        
        # Second row
        ttk.Label(param_frame, text="Max Pages:", **label_style).grid(row=1, column=0, sticky="w", pady=8)
        self.max_pages = tk.Entry(param_frame, width=30, **entry_style)
        self.max_pages.grid(row=1, column=1, padx=15, pady=8, sticky="ew")
        self.max_pages.insert(0, "1")
        
        ttk.Label(param_frame, text="Concurrency:", **label_style).grid(row=1, column=2, sticky="w", padx=(15, 0), pady=8)
        self.concurrency = tk.Entry(param_frame, width=30, **entry_style)
        self.concurrency.grid(row=1, column=3, padx=15, pady=8, sticky="ew")
        self.concurrency.insert(0, "3")
        
        # Third row
        ttk.Label(param_frame, text="Delay (seconds):", **label_style).grid(row=2, column=0, sticky="w", pady=8)
        self.delay = tk.Entry(param_frame, width=30, **entry_style)
        self.delay.grid(row=2, column=1, padx=15, pady=8, sticky="ew")
        self.delay.insert(0, "5")
        
        param_frame.columnconfigure(1, weight=1)
        param_frame.columnconfigure(3, weight=1)
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=15)
        
        self.start_btn = ttk.Button(button_frame, text="▶ START SCRAPING", command=self.start_scraping, style="Primary.TButton")
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="■ STOP SCRAPING", command=self.stop_scraping, state=tk.DISABLED, style="Secondary.TButton")
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        self.status_frame = ttk.Frame(main_frame, style="TFrame")
        self.status_frame.pack(fill=tk.X, pady=(5, 15))
        
        status_label = ttk.Label(self.status_frame, text="STATUS:", foreground=MonokaiTheme.TERTIARY, font=("Consolas", 9, "bold"))
        status_label.pack(side=tk.LEFT, padx=(0, 5))
        
        self.status_indicator = ttk.Label(self.status_frame, text="Ready", foreground=MonokaiTheme.ACCENT, font=("Consolas", 9))
        self.status_indicator.pack(side=tk.LEFT)
        log_frame = ttk.LabelFrame(main_frame, text="LOGS", style="TLabelframe")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        log_controls = ttk.Frame(log_frame)
        log_controls.pack(fill=tk.X, padx=10, pady=(10, 0))
        
        self.clear_logs_btn = ttk.Button(log_controls, text="CLEAR LOGS", command=self.clear_logs, style="Secondary.TButton")
        self.clear_logs_btn.pack(side=tk.RIGHT)
        
        self.log_area = scrolledtext.ScrolledText(log_frame, 
                                                wrap=tk.WORD, 
                                                height=15, 
                                                bg=MonokaiTheme.CARD_BG, 
                                                fg=MonokaiTheme.TEXT,
                                                insertbackground=MonokaiTheme.TEXT,
                                                font=("Consolas", 9),
                                                borderwidth=1,
                                                relief=tk.FLAT,
                                                highlightthickness=1,
                                                highlightcolor=MonokaiTheme.ACCENT,
                                                highlightbackground=MonokaiTheme.BORDER)
        self.log_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        self.log_area.tag_configure("error", foreground=MonokaiTheme.QUATERNARY)
        self.log_area.tag_configure("success", foreground=MonokaiTheme.ACCENT)
        self.log_area.tag_configure("warning", foreground=MonokaiTheme.WARNING)
        self.log_area.tag_configure("info", foreground=MonokaiTheme.TERTIARY)
        
        self.log("Welcome to Airbnb Scraper", "success")
        self.log("Enter search parameters and click START SCRAPING", "info")
        
    def log(self, message, level="default"):
        self.log_area.configure(state=tk.NORMAL)
        if level != "default":
            self.log_area.insert(tk.END, message + "\n", level)
        else:
            self.log_area.insert(tk.END, message + "\n")
        self.log_area.configure(state=tk.DISABLED)
        self.log_area.see(tk.END)
    
    def clear_logs(self):
        self.log_area.configure(state=tk.NORMAL)
        self.log_area.delete(1.0, tk.END)
        self.log_area.configure(state=tk.DISABLED)
        self.log("Logs cleared", "info")
        
    def update_status(self, status, color=None):
        if color is None:
            color = MonokaiTheme.ACCENT
        self.status_indicator.config(text=status, foreground=color)
        
    def start_scraping(self):
        # Validate inputs
        try:
            if not self.search_location.get().strip():
                self.log("Error: Search location cannot be empty", "error")
                self.update_status("Invalid input", MonokaiTheme.QUATERNARY)
                return
                
            max_pages = int(self.max_pages.get())
            concurrency = int(self.concurrency.get())
            delay = int(self.delay.get())
            
            if max_pages <= 0 or concurrency <= 0 or delay < 0:
                self.log("Error: Numeric values must be positive", "error")
                self.update_status("Invalid input", MonokaiTheme.QUATERNARY)
                return
                
        except ValueError:
            self.log("Error: Invalid numeric input", "error")
            self.update_status("Invalid input", MonokaiTheme.QUATERNARY)
            return
            
        # If validation passes
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.stop_event.clear()
        self.update_status("Scraping in progress...", MonokaiTheme.WARNING)
        
        params = {
            "search_location": self.search_location.get(),
            "max_pages": max_pages,
            "sheet_name": self.sheet_name.get(),
            "concurrency": concurrency,
            "delay": delay
        }
        
        self.log(f"Starting scraper with params: {params}", "info")
        
        self.scraper_thread = threading.Thread(
            target=self.run_async_scraper,
            kwargs=params,
            daemon=True
        )
        self.scraper_thread.start()
        
    def stop_scraping(self):
        self.stop_event.set()
        self.log("Stopping scraper... Please wait", "warning")
        self.update_status("Stopping...", MonokaiTheme.QUATERNARY)
        
    def run_async_scraper(self, search_location, max_pages, sheet_name, concurrency, delay):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            scraper = AirbnbScraper(
                search_location=search_location,
                max_pages=max_pages,
                sheet_name=sheet_name,
                concurrency=concurrency,
                delay=delay,
                stop_event=self.stop_event,
                log_callback=lambda msg: self.after(0, lambda: self.log(msg))
            )
            
            loop.run_until_complete(scraper.start())
        except Exception as e:
            self.after(0, lambda: self.log(f"Error: {str(e)}", "error"))
            self.after(0, lambda: self.update_status("Error occurred", MonokaiTheme.QUATERNARY))
        finally:
            loop.close()
            self.after(0, self.on_scraping_finished)
            
    def on_scraping_finished(self):
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
        if self.stop_event.is_set():
            self.log("Scraping stopped by user", "warning")
            self.update_status("Ready", MonokaiTheme.ACCENT)
        else:
            self.log("Scraping completed successfully!", "success")
            self.update_status("Ready", MonokaiTheme.ACCENT)

if __name__ == "__main__":
    app = ModernAirbnbScraperUI()
    app.mainloop()
