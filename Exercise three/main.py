import tkinter as tk
from modules.gui import StartScreen

def main():
    root = tk.Tk()
    start_screen = StartScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()