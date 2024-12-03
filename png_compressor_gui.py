import os
from tkinter import Tk, filedialog, Label, Button, messagebox
from tkinter import ttk
from tkinter import Scale
from PIL import Image

def select_input_folder():
    global input_folder
    input_folder = filedialog.askdirectory(title="Select Input Folder")
    if input_folder:
        input_label.config(text=f"Input Folder: {input_folder}")
    else:
        input_label.config(text="No folder selected")

def compress_images():
    if not input_folder or not scale_value.get() or not format_combobox.get():
        messagebox.showerror("Error", "Please select an input folder, scaling factor, and output format.")
        return

    try:
        # Create 'resized' folder inside the input folder
        output_folder = os.path.join(input_folder, "resized")
        os.makedirs(output_folder, exist_ok=True)
        
        # Get the selected scaling factor from the slider
        scale_factor = scale_value.get() / 100  # Convert percentage to decimal
        
        # Get the selected output format
        selected_format = format_combobox.get().lower()
        
        # Supported image extensions
        supported_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif'}
        
        # Initialize the progress bar
        total_files = len([file for file in os.listdir(input_folder) if any(file.lower().endswith(ext) for ext in supported_extensions)])
        progress_bar.config(maximum=total_files, value=0)
        
        # Process each image file
        for idx, file_name in enumerate(os.listdir(input_folder)):
            if any(file_name.lower().endswith(ext) for ext in supported_extensions):
                input_path = os.path.join(input_folder, file_name)
                output_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.{selected_format}")

                with Image.open(input_path) as img:
                    orig_width, orig_height = img.size
                    
                    # Calculate new width and height based on scale factor
                    new_width = int(orig_width * scale_factor)
                    new_height = int(orig_height * scale_factor)
                    
                    # Resize image to the new dimensions
                    img_resized = img.resize((new_width, new_height))
                    
                    # Save image with appropriate settings based on format
                    if selected_format in ['jpg', 'jpeg']:
                        img_resized.save(output_path, format="JPEG", optimize=True)
                    else:
                        img_resized.save(output_path, format=selected_format.upper(), optimize=True)

                # Update progress bar
                progress_bar.config(value=idx + 1)
                root.update_idletasks()

        messagebox.showinfo("Success", "All supported image files have been resized and compressed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def show_about():
    # Show a dialog box with author information
    messagebox.showinfo("About", "Batch Image Resizer and Compressor\n\nAuthor: Cemil Can Saylan\nVersion: 1.0")


# Create GUI window
root = Tk()
root.title("Batch Image Resizer and Compressor")

# Input folder selection
input_label = Label(root, text="No folder selected", wraplength=400)
input_label.pack(pady=2)
input_button = Button(root, text="Select Input Folder", command=select_input_folder)
input_button.pack(pady=5)

# Scaling factor selection (slider)
scale_label = Label(root, text="Select Scaling Factor (%):", )
scale_label.pack(pady=2)

scale_value = Scale(root, from_=1, to=100, orient="horizontal",  length=400, sliderlength=20, width=15, )
scale_value.set(100)  # Default to 100%
scale_value.pack(pady=5)

# Output format selection dropdown
format_label = Label(root, text="Select Output Format:",)
format_label.pack(pady=2)

format_combobox = ttk.Combobox(root, values=["PNG", "JPG", "JPEG", "GIF", "BMP", "TIFF"], state="readonly",)
format_combobox.set("PNG")  # Default to PNG
format_combobox.pack(pady=5)

# Progress bar
progress_label = Label(root, text="Progress:"
progress_label.pack(pady=2)

progress_bar = ttk.Progressbar(root, length=400, mode="determinate")
progress_bar.pack(pady=15)

# Compress button
compress_button = Button(root, text="Resize and Compress Image Files", command=compress_images,)
compress_button.pack(pady=10)

# About button
about_button = Button(root, text="About", command=show_about,)
about_button.pack(pady=5)

# Run the GUI
root.geometry("500x400")
root.mainloop()
