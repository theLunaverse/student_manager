import tkinter as tk
from PIL import Image, ImageTk
from .constants import *

class Tutorial:
    def __init__(self, root):
        self.root = root
        self.current_slide = 0
        self.tutorial_images = [
            self.load_image(TUTORIAL_1, WIDTH, HEIGHT),
            self.load_image(TUTORIAL_2, WIDTH, HEIGHT)
        ]
        self.setup_ui()
    
    def load_image(self, path, width, height):
        """Load and resize image"""
        try:
            img = Image.open(path)
            img = img.resize((width, height), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None
    
    def setup_ui(self):
        """Setup tutorial overlay"""
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Tutorial image
        if self.tutorial_images[self.current_slide]:
            self.image_item = self.canvas.create_image(0, 0, image=self.tutorial_images[self.current_slide], anchor="nw")
        
        # Buttons (colored and bigger)
        self.skip_btn = self.create_button("Skip Tutorial", 570, 560, self.skip_tutorial, TUTORIAL_SKIP_COLOR)
        self.next_btn = self.create_button("Next", 540, 618, self.next_slide, TUTORIAL_NEXT_COLOR)
    
    def create_button(self, text, x, y, command, color):
        """Create colored tutorial button"""
        btn = tk.Label(self.root, text=text, bg=color, fg=TUTORIAL_BUTTON_TEXT_COLOR,
                      font=(FONT, 16, 'bold'), cursor='hand2',
                      padx=20, pady=10)
        btn.bind('<Enter>', lambda e: btn.config(bg='dark' + color))  # Darker on hover
        btn.bind('<Leave>', lambda e: btn.config(bg=color))
        btn.bind('<Button-1>', lambda e: command())
        
        self.canvas.create_window(x, y, window=btn)
        return btn
    
    def next_slide(self):
        """Go to next tutorial slide"""
        self.current_slide += 1
        
        if self.current_slide < len(self.tutorial_images):
            # Update image
            self.canvas.itemconfig(self.image_item, image=self.tutorial_images[self.current_slide])
        else:
            self.finish_tutorial()
    
    def skip_tutorial(self):
        """Skip tutorial and go to main app"""
        self.finish_tutorial()
    
    def finish_tutorial(self):
        """Finish tutorial and start main app"""
        self.canvas.destroy()
        
        # Clear any remaining widgets and create StudentManager directly on root
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Import and create StudentManager
        from .student_manager import StudentManager
        StudentManager(self.root)

class StartScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.resizable(False, False)
        
        # Load images
        self.bg_image = self.load_image(START_BG, WIDTH, HEIGHT)
        self.start_btn_image = self.load_image(START_BUTTON, START_BTN_WIDTH, START_BTN_HEIGHT)
        self.quit_btn_image = self.load_image(QUIT_BUTTON, QUIT_BTN_WIDTH, QUIT_BTN_HEIGHT)
        
        self.setup_ui()
    
    def load_image(self, path, width, height):
        """Load and resize image"""
        try:
            img = Image.open(path)
            img = img.resize((width, height), Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None
    
    def setup_ui(self):
        """Setup start screen UI"""
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Background
        if self.bg_image:
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        
        # Start Button
        if self.start_btn_image:
            self.start_btn = self.canvas.create_image(WIDTH/2, START_BTN_Y, image=self.start_btn_image)
            self.canvas.tag_bind(self.start_btn, '<Button-1>', self.start_app)
        
        # Quit Button
        if self.quit_btn_image:
            self.quit_btn = self.canvas.create_image(QUIT_BTN_X, QUIT_BTN_Y, image=self.quit_btn_image)
            self.canvas.tag_bind(self.quit_btn, '<Button-1>', self.quit_app)
    
    def start_app(self, event=None):
        """Start the main application"""
        for widget in self.root.winfo_children():
            widget.destroy()
        Tutorial(self.root)  # Go to tutorial first

    def quit_app(self, event=None):
        """Quit the application"""
        self.root.quit()