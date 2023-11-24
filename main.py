# main.py

import tkinter as tk
from PIL import Image, ImageDraw, ImageTk  # For adding images
from how_to_play import HowToPlay
from initDb import init_db
from edit_questions import edit_questions_window

# Define a larger font for the buttons
button_font = ('Arial', 20, 'bold')

def add_vignette(image, edge_transparency=128, edge_width_ratio=0.1):
    width, height = image.size
    edge_width = min(width, height) * edge_width_ratio  # Define the width of the edge

    # Create a radial gradient mask
    mask = Image.new("L", (width, height), 255)  # Start with a fully opaque mask
    draw = ImageDraw.Draw(mask)

    max_radius = int(min(width, height) / 2)
    for i in range(max_radius, 0, -1):  # Start from the outside of the ellipse
        # Calculate fill value: it should start from `edge_transparency` and go to 0
        if max_radius - i < edge_width:
            fill_value = int((1 - ((max_radius - i) / edge_width)) * edge_transparency)
        else:
            fill_value = edge_transparency  # Maintain edge transparency until it reaches the edge_width

        # Draw the ellipse from larger to smaller
        draw.ellipse(
            (width / 2 - i, height / 2 - i, width / 2 + i, height / 2 + i),
            fill=fill_value
        )

    # Apply the mask to the alpha channel of the image
    image.putalpha(mask)

    return image


def show_game():
    print("Show game")

def show_main_menu():
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    set_background_image()  # Set the background image
    # Recreate the main menu
    create_main_menu()

def edit_questions():
    edit_window = edit_questions_window(root)

def set_background_image():
    # Load the background image
    background_image = Image.open('background.png')  # Replace 'background.png' with your actual file path
    # Convert the image to a PhotoImage
    tk_background_image = ImageTk.PhotoImage(background_image)

    # Calculate how many times to tile the image
    num_tiles_x = root.winfo_screenwidth() // tk_background_image.width() + 1
    num_tiles_y = root.winfo_screenheight() // tk_background_image.height() + 1

    # Tile the image across the background
    for x in range(num_tiles_x):
        for y in range(num_tiles_y):
            background_label = tk.Label(root, image=tk_background_image)
            background_label.image = tk_background_image  # Keep a reference
            background_label.place(x=x * tk_background_image.width(), y=y * tk_background_image.height())


def create_main_menu():
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate the size of the logo (10% of the screen or 50x50 pixels, whichever is smaller)
    logo_size = min(200, screen_width // 5, screen_width // 5)

    # Open the logo with PIL
    original_logo = Image.open('quizLogo.png').convert("RGBA")
    resized_logo = original_logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    # Add a vignette to the resized logo
    vignette_logo = add_vignette(resized_logo, 255, 0.1)
    logo = ImageTk.PhotoImage(vignette_logo)

    # Add the logo image to the Label
    logo_label = tk.Label(root, image=logo)
    logo_label.image = logo  # Keep a reference so it's not garbage collected
    logo_label.pack(pady=20)
    
    # Create a frame to hold the buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=40)  # Increase the spacing from the logo

    play_button = tk.Button(button_frame, text="PLAY", command=show_game, font=button_font, padx=20, pady=10)
    play_button.pack(pady=20, fill='x')  # `fill='x'` makes the button expand to fill the frame

    edit_questions_button = tk.Button(button_frame, text="EDIT QUESTIONS", command=edit_questions, font=button_font, padx=20, pady=10)
    edit_questions_button.pack(pady=20, fill='x')

    how_to_play_button = tk.Button(button_frame, text="HOW TO PLAY", command=show_how_to_play, font=button_font, padx=20, pady=10)
    how_to_play_button.pack(pady=20, fill='x')

    quit_button = tk.Button(button_frame, text="QUIT", command=root.quit, font=button_font, padx=20, pady=10)
    quit_button.pack(pady=20, fill='x')

def show_how_to_play():
    # Clear the window
    for widget in root.winfo_children():
        widget.destroy()

    # Images for how to play
    images = ["KeyboardPlayers.png", "KeyboardSelectAnswer.png"]  # replace with your actual image paths

    # Create the How to Play page
    HowToPlay(root, images, show_main_menu)

root = tk.Tk()

# Make the window full screen
root.attributes('-fullscreen', True)
# Or you can use this for a maximized window, which may be more user-friendly:
# root.state('zoomed')

set_background_image()  # Set the background image
create_main_menu()  # Start with the main menu

# Call the init_db function to initialize the database at startup
init_db() #name of the database is quiz_game.db

root.mainloop()
