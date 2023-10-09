import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox  # Add this import
import qrcode
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import ttk
from pyzbar.pyzbar import decode

# Define dynamic limits for module size and border size
MIN_MODULE_SIZE = 1
MAX_MODULE_SIZE = 25
MIN_BORDER_SIZE = 0
MAX_BORDER_SIZE = 25

def generate_qr_code():
    text = text_entry.get()
    version = version_var.get()
    error_correction = error_correction_var.get()
    fill_color = fill_color_entry.get()
    box_size = box_size_combobox.get()
    border_size = border_size_combobox.get()
    save_image = save_image_var.get()
    image_format = image_format_var.get()

    if not text:
        tkinter.messagebox.showerror("Error", "Text cannot be empty.")
        return

    try:
        version = int(version)
    except ValueError:
        tkinter.messagebox.showerror("Error", "Invalid value for version.")
        return

    if error_correction == "L":
        error_correction = qrcode.constants.ERROR_CORRECT_L
    elif error_correction == "M":
        error_correction = qrcode.constants.ERROR_CORRECT_M
    elif error_correction == "Q":
        error_correction = qrcode.constants.ERROR_CORRECT_Q
    elif error_correction == "H":
        error_correction = qrcode.constants.ERROR_CORRECT_H
    else:
        tkinter.messagebox.showerror("Error", "Invalid error correction level.")
        return

    if not fill_color:
        fill_color = "#000000"

    if not box_size:
        tkinter.messagebox.showerror("Error", "Module size cannot be empty.")
        return

    try:
        box_size = int(box_size)
        if not (MIN_MODULE_SIZE <= box_size <= MAX_MODULE_SIZE):
            tkinter.messagebox.showerror("Error", f"Module size must be between {MIN_MODULE_SIZE} and {MAX_MODULE_SIZE}.")
            return
    except ValueError:
        tkinter.messagebox.showerror("Error", "Invalid value for module size.")
        return

    if not border_size:
        tkinter.messagebox.showerror("Error", "Border size cannot be empty.")
        return

    try:
        border_size = int(border_size)
        if not (MIN_BORDER_SIZE <= border_size <= MAX_BORDER_SIZE):
            tkinter.messagebox.showerror("Error", f"Border size must be between {MIN_BORDER_SIZE} and {MAX_BORDER_SIZE}.")
            return
    except ValueError:
        tkinter.messagebox.showerror("Error", "Invalid value for border size.")
        return

    qr = qrcode.QRCode(
        version=version,
        error_correction=error_correction,
        box_size=box_size,
        border=border_size,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color="white")

    if save_image:
        file_name = f"qrcode{datetime.now().strftime('%y%m%d-%H%M%S')}"
        if image_format == "JPEG":
            img = img.convert("RGB")
            file_name += ".jpg"
        elif image_format == "PNG":
            file_name += ".png"
        else:
            file_name += ".bmp"
        
        img.save(file_name)

    display_qr_code(img)

def display_qr_code(img):
    qr_code_window = tk.Toplevel(root)
    qr_code_window.title("QR Code")
    
    img = ImageTk.PhotoImage(img)
    
    img_label = tk.Label(qr_code_window, image=img)
    img_label.image = img
    img_label.pack()
    
    qr_code_window.mainloop()

def toggle_dropdown_state():
    if save_image_var.get():
        image_format_dropdown["state"] = "active"
    else:
        image_format_dropdown["state"] = "disabled"

def browse_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
    image_path_label.config(text=file_path)
    decode_qr_code(file_path)

def decode_qr_code(image_path):
    try:
        img = Image.open(image_path)
        decoded_objects = decode(img)
        decoded_text = ""
        for obj in decoded_objects:
            decoded_text += f"Type: {obj.type}\nData: {obj.data.decode('utf-8')}\n\n"
        
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, decoded_text)
        result_text.config(state=tk.DISABLED)
    except Exception as e:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Error: {str(e)}")
        result_text.config(state=tk.DISABLED)

def open_decoder_window():
    decoder_window = tk.Toplevel(root)
    decoder_window.title("QR Code Decoder")

    browse_button = tk.Button(decoder_window, text="Browse Image", command=browse_image)
    browse_button.pack()

    global image_path_label
    image_path_label = tk.Label(decoder_window, text="", wraplength=400)
    image_path_label.pack()

    global result_text
    result_text = tk.Text(decoder_window, height=10, width=40)
    result_text.pack()
    result_text.config(state=tk.DISABLED)

root = tk.Tk()
root.title("QR Code Generator and Decoder")

text_label = tk.Label(root, text="Text to Encode:")
text_label.pack()

text_entry = tk.Entry(root)
text_entry.pack()

version_label = tk.Label(root, text="QR Version:")
version_label.pack()

version_var = tk.StringVar()
version_dropdown = tk.OptionMenu(root, version_var, *range(1, 41))
version_var.set(3)
version_dropdown.pack()

error_correction_label = tk.Label(root, text="Error Correction Level:")
error_correction_label.pack()

error_correction_var = tk.StringVar()
error_correction_dropdown = tk.OptionMenu(root, error_correction_var, "L", "M", "Q", "H")
error_correction_var.set("M")
error_correction_dropdown.pack()

fill_color_label = tk.Label(root, text="Fill Color (Hex):")
fill_color_label.pack()

fill_color_entry = tk.Entry(root)
fill_color_entry.pack()

box_size_label = tk.Label(root, text="Module Size:")
box_size_label.pack()

box_size_combobox = ttk.Combobox(root, values=["3", "6", "9"])
box_size_combobox.set("6")
box_size_combobox.pack()

border_size_label = tk.Label(root, text="Border Size:")
border_size_label.pack()

border_size_combobox = ttk.Combobox(root, values=["0", "2", "4", "8"])
border_size_combobox.set("4")
border_size_combobox.pack()

save_image_var = tk.BooleanVar()
save_image_checkbox = tk.Checkbutton(root, text="Save Image", variable=save_image_var, command=toggle_dropdown_state)
save_image_checkbox.pack()

image_format_label = tk.Label(root, text="Image Format:")
image_format_label.pack()

image_format_var = tk.StringVar()
image_format_dropdown = tk.OptionMenu(root, image_format_var, "BMP", "JPEG", "PNG")
image_format_var.set("BMP")
image_format_dropdown.pack()

toggle_dropdown_state()

generate_button = tk.Button(root, text="Generate QR Code", command=generate_qr_code)
generate_button.pack()

open_decoder_button = tk.Button(root, text="Open Decoder", command=open_decoder_window)
open_decoder_button.pack()

root.mainloop()
