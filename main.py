import tkinter as tk
import tkinter.font as font
from Gesture_Controller import gest_control
from eye import eye_move
from samvk import vk_keyboard
from PIL import Image, ImageTk
from aura import aura_chat

# Constants for dimensions
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 700
ICON_SIZE = (200, 200)
BUTTON_IMAGE_SIZE = (50, 50)

# Initialize main window
window = tk.Tk()
window.title("Gesture Controlled Virtual Mouse and Keyboard")
window.iconphoto(False, tk.PhotoImage(file='mn.png'))
window.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}')
window.configure(bg="white")

# Define fonts
title_font = font.Font(size=25, weight='bold', family='Helvetica')
button_font = font.Font(size=20)

# Title Label
label_title = tk.Label(window, text="Gesture Controlled Virtual Mouse and Keyboard", font=title_font, bg="white")
label_title.grid(row=0, column=0, columnspan=4, pady=(20, 10))

# Load and resize images
def load_image(path, size):
    try:
        image = Image.open(path)
        image = image.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None

# Center Icon
center_icon = load_image('icons/man.jpeg', ICON_SIZE)
label_icon = tk.Label(window, image=center_icon, bg="white")
label_icon.grid(row=1, column=1, columnspan=2, pady=(10, 20))

# Button images
btn1_image = load_image('icons/bot.png', BUTTON_IMAGE_SIZE)
btn2_image = load_image('icons/keyboard.png', BUTTON_IMAGE_SIZE)
btn3_image = load_image('icons/eye.jpeg', BUTTON_IMAGE_SIZE)
btn4_image = load_image('icons/hand.png', BUTTON_IMAGE_SIZE)

# Buttons
btn1 = tk.Button(window, text='VoiceBot', fg='green', command=aura_chat, image=btn1_image, compound='top', font=button_font)
btn1.grid(row=2, column=0, padx=20, pady=10)

btn2 = tk.Button(window, text='Keyboard', fg='red', command=vk_keyboard, image=btn2_image, compound='top', font=button_font)
btn2.grid(row=2, column=3, padx=20, pady=10)

btn3 = tk.Button(window, text='Eye', fg='blue', command=eye_move, image=btn3_image, compound='top', font=button_font)
btn3.grid(row=3, column=0, padx=20, pady=10)

btn4 = tk.Button(window, text='Gesture', fg='orange', command=gest_control, image=btn4_image, compound='top', font=button_font)
btn4.grid(row=3, column=3, padx=20, pady=10)

# Exit Button (Centered below other buttons)
btn5 = tk.Button(window, text='Exit', fg='red', command=window.quit, font=button_font)
btn5.grid(row=4, column=1, columnspan=2, pady=20)

window.mainloop()
