import tkinter as tk
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import random

# Initialize system volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Get volume range
volume_range = volume.GetVolumeRange()  # Typically (-65.25, 0.0)
min_vol, max_vol = volume_range[0], volume_range[1]

# Create the main window
root = tk.Tk()
root.title("Random Volume Control")
root.geometry("800x400")  # Larger window for bigger clickable area

# Volume bar
canvas = tk.Canvas(root, width=600, height=40, bg="white")
canvas.pack(pady=20)

# Draw the volume bar
canvas.create_rectangle(10, 15, 590, 25, outline="black", fill="lightgray")

# Volume knob
knob = canvas.create_oval(290, 5, 310, 35, fill="blue")  # Initial position at center

# Function to set random volume
def set_random_volume(event=None):
    # Generate a random volume level within the valid range
    random_vol = random.uniform(min_vol, max_vol)
    volume.SetMasterVolumeLevel(random_vol, None)

    # Update knob position and volume label
    update_knob_position(random_vol)

# Function to update knob position based on volume level
def update_knob_position(vol_level):
    tilt_x = (vol_level - min_vol) / (max_vol - min_vol)  # Normalize to 0-1 range
    new_knob_x = 10 + tilt_x * 580  # Map to bar position (10 to 590)
    canvas.coords(knob, new_knob_x, 5, new_knob_x + 20, 35)
    volume_label.config(text=f"Volume: {int(tilt_x * 100)}%")

# Volume label
volume_label = tk.Label(root, text="Volume: 50%", font=("Arial", 16))
volume_label.pack(pady=20)

# Bind mouse click to set random volume
root.bind("<Button-1>", set_random_volume)  # Click anywhere to set random volume

# Run the application
root.mainloop()