import tkinter as tk
from tkinter import filedialog, simpledialog
import os

def load_images():
    images = []
    folder_path = folder_selector()
    for image_path in os.listdir(folder_path):
        file_ext = image_path.split(".")[-1]
        full_path = os.path.join(folder_path, image_path)
        if os.path.isfile(full_path):
            if file_ext == "jpg" or file_ext == "jpeg" or file_ext == "png":
                images.append(full_path)
    return images

def folder_selector():
    print("Please select the folder containing the images to be blurred")
    tk.Tk().withdraw()
    folder_path = filedialog.askdirectory()
    if not folder_path:
        print("\nNo folder selected!")
        print("You can close the program by closing this window\n")
        folder_path = folder_selector()
    return folder_path


def select_blur_level():
    print("Please select the blur level")
    tk.Tk().withdraw()
    blur_level = simpledialog.askinteger("Blur level", "Enter a number between 1 and 10")
    if not blur_level:
        print("\nNo blur level selected!")
        print("You can close the program by closing this window\n")
        blur_level = select_blur_level()
    if blur_level < 1 or blur_level > 10:
        print("\nInvalid blur level!")
        print("You can close the program by closing this window\n")
        blur_level = select_blur_level()
    return blur_level