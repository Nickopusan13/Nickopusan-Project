import asyncio
import tkinter as tk
from tkinter import ttk, messagebox
from queue import Queue
import threading
import os
import random
from scraper import GoogleMapsScraper
from cleaner import DataCleaner

BG_COLOR = "#000000"
STAR_COLOR = "#FFFFFF"
MOON_COLOR = "#F4F4F4"
CRATER_COLOR = "#CCCCCC"
PRIMARY_COLOR = "#00FFFF"
SECONDARY_COLOR = "#000000"
TEXT_COLOR = "#FFFFFF"
STATUS_BG = "#222222"
FONT_REGULAR = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
TITLE_FONT = ("Space Age", 18, "bold")

class StarryBackground:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.stars = []
        self.moon = None
        self.create_night_sky()
        
    def create_night_sky(self):
        for _ in range(100):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.choice([1, 1, 1, 2])
            star = self.canvas.create_oval(x, y, x+size, y+size, fill=STAR_COLOR, outline="")
            self.stars.append(star)
        moon_x = self.width - 100
        moon_y = 50
        self.moon = self.canvas.create_oval(moon_x-30, moon_y-30, moon_x+30, moon_y+30, 
                                          fill=MOON_COLOR, outline="")
        self.canvas.create_oval(moon_x-10, moon_y-15, moon_x+5, moon_y, fill=CRATER_COLOR, outline="")
        self.canvas.create_oval(moon_x-25, moon_y+10, moon_x-15, moon_y+20, fill=CRATER_COLOR, outline="")
        self.canvas.create_oval(moon_x+5, moon_y+5, moon_x+15, moon_y+15, fill=CRATER_COLOR, outline="")
        self.twinkle_stars()

    def twinkle_stars(self):
        for star in self.stars:
            if random.random() < 0.3:  # 10% chance to twinkle
                self.canvas.itemconfig(star, fill=random.choice(["#FFFFFF", "#DDDDDD", "#AAAAAA"]))
        self.canvas.after(500, self.twinkle_stars)

class ScraperApp:
    def __init__(self, root):
        self.root = root
        self.status_queue = Queue()
        self.setup_ui()
        self.running = False

    def setup_ui(self):
        self.root.title("Google Maps Scraper")
        self.root.configure(bg=BG_COLOR)
        self.root.geometry("600x400")
        self.root.minsize(550, 350)

        # Create starry background
        self.canvas = tk.Canvas(self.root, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.starry_bg = StarryBackground(self.canvas, 600, 400)

        # Main container
        main_container = tk.Frame(self.canvas, bg="#111111", bd=2, 
                                 relief=tk.FLAT, padx=20, pady=20)
        main_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=500, height=300)

        # Header
        header_frame = tk.Frame(main_container, bg="#111111")
        header_frame.pack(pady=(0, 15))
        tk.Label(header_frame, 
                text="Google Maps Scraper",
                font=TITLE_FONT,
                bg="#111111",
                fg=PRIMARY_COLOR).pack()

        # Search section
        search_frame = tk.Frame(main_container, bg="#111111")
        search_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(search_frame, 
                text="Enter Search Term:",
                font=FONT_BOLD,
                bg="#111111",
                fg=TEXT_COLOR).pack(anchor=tk.W, pady=(0, 5))
        
        self.search_entry = ttk.Entry(search_frame, font=FONT_REGULAR)
        self.search_entry.configure(style='Dark.TEntry')
        self.search_entry.pack(fill=tk.X, pady=5, ipady=5)

        # Start button
        self.start_btn = tk.Button(main_container,
                                text="Start Scraping",
                                command=self.start_scraping,
                                font=FONT_BOLD,
                                bg=PRIMARY_COLOR,
                                fg=SECONDARY_COLOR,
                                activebackground="#00AAAA",
                                activeforeground=SECONDARY_COLOR,
                                relief=tk.FLAT,
                                padx=20,
                                pady=8,
                                cursor="hand2")
        self.start_btn.pack(pady=15, fill=tk.X)

        # Status bar
        self.status_label = tk.Label(self.root,
                                  text="Ready",
                                  font=FONT_REGULAR,
                                  bg=STATUS_BG,
                                  fg=TEXT_COLOR,
                                  padx=10,
                                  pady=5)
        self.status_label.place(relx=0.5, rely=0.95, anchor=tk.S)

        self._configure_styles()

    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Dark.TEntry',
                        fieldbackground="#222222",
                        foreground=TEXT_COLOR,
                        bordercolor=PRIMARY_COLOR,
                        lightcolor=PRIMARY_COLOR)
        style.map('Dark.TEntry',
                 fieldbackground=[('active', "#222222")],
                 bordercolor=[('focus', PRIMARY_COLOR)])

    def start_scraping(self):
        if self.running:
            return

        search_term = self.search_entry.get()
        if not search_term:
            messagebox.showwarning("Input Error", "Please enter a search term!")
            return

        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.status_label.config(text=f"Initializing scrape for '{search_term}'...", fg=PRIMARY_COLOR)
        self.root.after(100, self.check_status_queue)
        threading.Thread(target=self.run_scraping_task, args=(search_term,), daemon=True).start()

    def check_status_queue(self):
        while not self.status_queue.empty():
            message = self.status_queue.get()
            self.status_label.config(text=message, fg="orange")
        if self.running:
            self.root.after(100, self.check_status_queue)

    def update_status(self, message):
        self.status_queue.put(message)

    def run_scraping_task(self, search_term):
        try:
            async def async_scrape():
                def progress_callback(name):
                    self.root.after(0, self.update_status, f"Scraping {name}...")

                scraper = GoogleMapsScraper(progress_callback)
                await scraper.start_url(search_term)
                
                # Clean the data after scraping
                if scraper.file_path and os.path.exists(scraper.file_path):
                    cleaner = DataCleaner()
                    cleaned_path = cleaner.clean_scraped_data(scraper.file_path)
                    return scraper.file_path, cleaned_path
                return None, None

            file_path, cleaned_path = asyncio.run(async_scrape())
            if cleaned_path:
                result = f"Success! Files saved to:\n{os.path.basename(file_path)}\n{os.path.basename(cleaned_path)}"
            else:
                result = "Scraping completed but no data was saved"
                
            self.root.after(0, self.on_success, result)
        except Exception as e:
            self.root.after(0, self.on_error, str(e))
        finally:
            self.root.after(0, self.reset_ui)

    def on_success(self, message):
        self.status_label.config(text=message, fg="#28a745")
        messagebox.showinfo("Success", message)

    def on_error(self, error):
        self.status_label.config(text=f"Error: {error}", fg="#dc3545")
        messagebox.showerror("Error", error)

    def reset_ui(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScraperApp(root)
    root.mainloop()