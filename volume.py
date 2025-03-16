import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import subprocess
import time
import webbrowser
import random

# Initialize system volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Create the main window
root = tk.Tk()
root.title("Accurate Random Volume Control")
root.geometry("800x400")
root.iconbitmap("icon.ico")

# Background Image
bg_image = Image.open("Background.jpg").resize((800, 400))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Volume bar
canvas = tk.Canvas(root, width=600, height=40, bg="#FFFFFF", highlightthickness=0)
canvas.pack(pady=20)
canvas.create_rectangle(10, 15, 590, 25, outline="#2D221E", fill="#B5A899")

# Volume knob
knob = canvas.create_oval(290, 5, 310, 35, fill="#5B8C5A")

# Volume label
volume_label = tk.Label(root, text="Volume: 50%", font=("Arial", 16), bg="#FFFFFF", fg="#2D221E")
volume_label.pack(pady=20)

# Click counter
click_count = 0
disable_knob_click = False  # Flag to control knob movement

# Smooth knob movement
def animate_knob(target_x):
    current_x = canvas.coords(knob)[0]
    if abs(current_x - target_x) < 2:
        canvas.coords(knob, target_x, 5, target_x + 20, 35)
    else:
        step = 5 if current_x < target_x else -5  # Faster movement steps
        canvas.coords(knob, current_x + step, 5, current_x + step + 20, 35)
        root.after(5, lambda: animate_knob(target_x))  # Faster animation timing

# Trigger Chrome closure and video
def trigger_surprise():
    global disable_knob_click
    disable_knob_click = True  # Disable further clicks on the knob
    subprocess.run("taskkill /f /im chrome.exe", shell=True)
    volume.SetMasterVolumeLevelScalar(1.0, None)
    time.sleep(1)
    webbrowser.open("https://youtu.be/7AjkW-VzRa0?autoplay=1", new=1)
    root.after(1000, root.destroy)  # Close program after the video starts

# Question flow
def ask_question_2():
    question_label.config(text="Do you need some help??")
    yes_button.config(command=trigger_surprise)
    no_button.config(command=trigger_surprise)

def ask_question_1():
    global disable_knob_click
    disable_knob_click = True  # Disable knob movement during questions
    question_label.config(text="Are you not sure about the volume??")
    yes_button.pack(pady=5)
    no_button.pack(pady=5)
    yes_button.config(command=ask_question_2)
    no_button.config(command=ask_question_2)

# Random volume control
def set_random_volume(event=None):
    global click_count, disable_knob_click
    if disable_knob_click:  # Prevent knob movement during questions
        return

    click_count += 1
    random_vol = random.uniform(0.0, 1.0)
    volume.SetMasterVolumeLevelScalar(random_vol, None)

    # Smoothly animate knob
    target_x = 10 + random_vol * 580
    animate_knob(target_x)

    volume_label.config(text=f"Volume: {int(random_vol * 100)}%")

    if click_count == 5:
        ask_question_1()

# Smooth fade-in animation
def fade_in(opacity=0.1):
    if opacity <= 1.0:
        root.attributes("-alpha", opacity)
        root.after(10, lambda: fade_in(opacity + 0.05))  # Faster fade-in

# Questions
question_label = tk.Label(root, text="", font=("Arial", 16), bg="#FFFFFF", fg="#2D221E")
question_label.pack(pady=10)

yes_button = tk.Button(root, text="YES", bg="#5B8C5A", fg="white", font=("Arial", 14), width=10)
no_button = tk.Button(root, text="NO", bg="#B55E5E", fg="white", font=("Arial", 14), width=10)

# Initialize knob position
current_volume = volume.GetMasterVolumeLevelScalar()
target_x = 10 + current_volume * 580
animate_knob(target_x)
volume_label.config(text=f"Volume: {int(current_volume * 100)}%")

# Bind mouse click to set random volume
root.bind("<Button-1>", set_random_volume)

# Start fade-in animation
root.attributes("-alpha", 0)
fade_in()

# Run the application
root.mainloop()
