import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from mood_keywords import keywords

class TravisScottBot:
    def __init__(self, root):
        self.root = root
        self.root.title("🎧 Travis Scott Mood Bot")
        self.root.geometry("700x600")
        self.root.configure(bg='#2c2c2c')
        
        # Load the songs database
        try:
            with open("songs.json") as f:
                self.songs = json.load(f)
            self.all_albums = sorted(set(song["album"] for song in self.songs))
        except FileNotFoundError:
            messagebox.showerror("Error", "songs.json file not found!")
            self.songs = []
            self.all_albums = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = tk.Frame(self.root, bg='#2c2c2c')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="🎧 Travis Scott Mood Bot", 
            font=("Arial", 24, "bold"),
            bg='#2c2c2c',
            fg='#ffffff'
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            main_frame,
            text="Tell me your mood and I'll find the perfect Travis Scott song!",
            font=("Arial", 14),
            bg='#2c2c2c',
            fg='#cccccc'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Input section with visible border
        input_frame = tk.Frame(main_frame, bg='#404040', relief='solid', bd=2)
        input_frame.pack(fill='x', pady=(0, 20))
        
        # Mood input
        mood_label = tk.Label(
            input_frame,
            text="What's your mood? (e.g., sad, party, chill, hype)",
            font=("Arial", 14, "bold"),
            bg='#404040',
            fg='#ffffff'
        )
        mood_label.pack(pady=(15, 5))
        
        # Make input field more visible
        input_container = tk.Frame(input_frame, bg='#404040')
        input_container.pack(pady=(0, 10), padx=20, fill='x')
        
        self.mood_entry = tk.Entry(
            input_container,
            font=("Arial", 16),
            bg='#ffffff',  # White background for visibility
            fg='#000000',  # Black text
            insertbackground='#000000',  # Black cursor
            relief='solid',
            bd=2,
            width=40
        )
        self.mood_entry.pack(ipady=8, fill='x')
        self.mood_entry.bind('<Return>', lambda event: self.get_recommendation())
        
        # Album selection
        album_label = tk.Label(
            input_frame,
            text="Album (optional):",
            font=("Arial", 14, "bold"),
            bg='#404040',
            fg='#ffffff'
        )
        album_label.pack(pady=(10, 5))
        
        album_container = tk.Frame(input_frame, bg='#404040')
        album_container.pack(pady=(0, 15), padx=20, fill='x')
        
        self.album_var = tk.StringVar()
        album_dropdown = ttk.Combobox(
            album_container,
            textvariable=self.album_var,
            values=[''] + self.all_albums,
            state='readonly',
            font=("Arial", 14),
            width=38
        )
        album_dropdown.pack(ipady=5, fill='x')
        album_dropdown.set('')
        
        # Get recommendation button
        button_frame = tk.Frame(main_frame, bg='#2c2c2c')
        button_frame.pack(pady=20)
        
        get_button = tk.Button(
            button_frame,
            text="🎵 Get My Song Recommendation",
            font=("Arial", 16, "bold"),
            bg='#8B4513',
            fg='#ffffff',
            activebackground='#A0522D',
            activeforeground='#ffffff',
            pady=12,
            padx=20,
            relief='raised',
            bd=3,
            command=self.get_recommendation
        )
        get_button.pack()
        
        # Results section
        results_frame = tk.Frame(main_frame, bg='#404040', relief='solid', bd=2)
        results_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        results_label = tk.Label(
            results_frame,
            text="🎶 Your Recommendations:",
            font=("Arial", 16, "bold"),
            bg='#404040',
            fg='#ffffff'
        )
        results_label.pack(pady=(15, 10))
        
        # Results text area
        text_container = tk.Frame(results_frame, bg='#404040')
        text_container.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        self.results_text = scrolledtext.ScrolledText(
            text_container,
            font=("Arial", 12),
            bg='#ffffff',
            fg='#000000',
            wrap=tk.WORD,
            height=12,
            relief='solid',
            bd=1
        )
        self.results_text.pack(fill='both', expand=True)
        
        # Initial message
        self.results_text.insert(tk.END, 
            "👋 Welcome to the Travis Scott Mood Bot!\n\n"
            "How to use:\n"
            "1. Type your mood in the box above (sad, party, chill, hype, etc.)\n"
            "2. Optionally select an album\n"
            "3. Click the button or press Enter\n\n"
            "Try moods like: sad, party, chill, hype, angry, romantic, motivational, deep, happy, or funky!")
        self.results_text.config(state=tk.DISABLED)
        
        # Set focus to input field
        self.mood_entry.focus_set()
        
    def get_recommendation(self):
        user_input = self.mood_entry.get().strip().lower()
        album_input = self.album_var.get().strip()
        
        if not user_input:
            messagebox.showwarning("Input Required", "Please enter your mood!")
            return
        
        # Clear previous results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        # Match moods based on user input
        matched_moods = []
        for mood, words in keywords.items():
            if any(word in user_input for word in words):
                matched_moods.append(mood)
        
        # Handle non-existent album
        if album_input and album_input not in self.all_albums:
            self.results_text.insert(tk.END, 
                f"❌ The album '{album_input}' doesn't exist in the database.\n\n"
                f"Available albums:\n" + "\n".join(f"• {album}" for album in self.all_albums))
            self.results_text.config(state=tk.DISABLED)
            return
        
        # Filter songs based on mood and album
        recommendations = [
            song["title"] for song in self.songs
            if (not album_input or song["album"] == album_input)
            and any(m in song["mood"] for m in matched_moods)
        ]
        
        # Display results
        if matched_moods:
            if recommendations:
                mood_text = ", ".join(matched_moods)
                self.results_text.insert(tk.END, 
                    f"🎵 Perfect songs for your {mood_text} mood:\n\n")
                for i, rec in enumerate(recommendations, 1):
                    self.results_text.insert(tk.END, f"   {i}. {rec}\n")
                
                if album_input:
                    self.results_text.insert(tk.END, f"\n📀 From the album: {album_input}")
                    
                self.results_text.insert(tk.END, f"\n\n🎧 Found {len(recommendations)} song(s) for you!")
            else:
                if album_input:
                    self.results_text.insert(tk.END, 
                        f"😕 No {', '.join(matched_moods)} songs found in '{album_input}'.\n\n"
                        "💡 Try:\n• A different mood\n• Removing the album filter\n• Different keywords")
                else:
                    self.results_text.insert(tk.END, 
                        f"😕 No Travis songs match '{user_input}' vibe.\n\n"
                        "💡 Try moods like:\n• party, hype, lit\n• sad, emotional, heartbreak\n• chill, mellow, vibe\n• aggressive, rage, intense")
        else:
            self.results_text.insert(tk.END, 
                f"❓ I didn't catch a clear mood from '{user_input}'.\n\n"
                "💡 Try being more specific:\n"
                "• 'I want party songs'\n"
                "• 'I feel sad'\n"
                "• 'Something chill'\n"
                "• 'Hype music for workout'\n"
                "• 'Romantic vibes'\n"
                "• 'Deep and emotional'")
        
        self.results_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = TravisScottBot(root)
    root.mainloop()