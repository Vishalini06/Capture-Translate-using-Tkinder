import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import cv2
import pytesseract
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import pyttsx3
import matplotlib.pyplot as plt

def open_image():
    filepath = filedialog.askopenfilename()
    image_path_entry.delete(0, tk.END)
    image_path_entry.insert(0, filepath)

def extract_text():
    image_path = image_path_entry.get()
    if image_path:
        img = cv2.imread(image_path)
        text = pytesseract.image_to_string(img)
        input_box.delete("1.0", "end")
        input_box.insert("1.0", text)
    else:
        input_box.delete("1.0", "end")
        input_box.insert("1.0", "Please select an image")

def capture_image():
    cap = cv2.VideoCapture(0)
    while True:
        ret , frame = cap.read()
        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.show()
        if cv2.waitKey(5) & 0xFF == ord('c'):
            cv2.imwrite('captured_image.jpg', frame)
            break
    cap.release()
    cv2.destroyAllWindows()
    image_path_entry.delete(0, tk.END)
    image_path_entry.insert(0, 'captured_image.jpg')
    extract_text()

def translate_text():
    input_text = input_box.get("1.0", "end-1c")
    selected_language = language_var.get()
    if selected_language == "Tamil":
        translator = GoogleTranslator(source='auto', target='ta')
    elif selected_language == "Telugu":
        translator = GoogleTranslator(source='auto', target='te')
    elif selected_language == "English":
        translator = GoogleTranslator(source='auto', target='en')
    elif selected_language == "Kannada":
        translator = GoogleTranslator(source='auto', target='kn')
    elif selected_language == "Hindi":
        translator = GoogleTranslator(source='auto', target='hi')
    translated_text = translator.translate(input_text)
    output_box.delete("1.0", "end")
    output_box.insert("1.0", translated_text)

def speak_text():
    text = output_box.get("1.0", "end-1c")
    selected_language = language_var.get()
    language_codes = {
        "Tamil": "ta",
        "Telugu": "te",
        "English": "en",
        "Kannada": "kn",
        "Hindi": "hi"
    }
    tts = gTTS(text=text, lang=language_codes[selected_language], slow=False)
    tts.save("output.mp3")
    os.system("start output.mp3")

def speak_text_in_tkinter():
    text = output_box.get("1.0", "end-1c")
    selected_language = language_var.get()
    language_codes = {
        "Tamil": "ta",
        "Telugu": "te",
        "English": "en",
        "Kannada": "kn",
        "Hindi": "hi"
    }
    engine = pyttsx3.init()
    engine.setProperty('voice', language_codes[selected_language])
    engine.say(text)
    engine.runAndWait()

root = tk.Tk()
root.title("Image Translator")
root.configure(bg="#f0f0f0")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=lambda: print("This is an image translator"))
menu_bar.add_cascade(label="Help", menu=help_menu)

input_frame = tk.Frame(root, bg="#e0e0e0", highlightthickness=2, bd=2)
input_frame.pack(pady=10)

image_path_label = tk.Label(input_frame, text="Image Path:", font=("Arial", 12), bg="#e0e0e0")
image_path_label.pack(pady=5)
image_path_entry = tk.Entry(input_frame, width=50, font=("Arial", 12), bg="#ffffff")
image_path_entry.pack(pady=5)
open_button = tk.Button(input_frame, text="Open Image", command=open_image, font=("Arial", 12), bg="#4CAF50", fg="#ffffff", relief="ridge", bd=2)
open_button.pack(pady=5)
capture_button = tk.Button(input_frame, text="Capture Image", command=capture_image, font=("Arial", 12), bg="#4CAF50", fg="#ffffff", relief="ridge", bd=2)
capture_button.pack(pady=5)
extract_button = tk.Button(input_frame, text="Extract Text", command=extract_text, font=("Arial", 12), bg="#4CAF50", fg="#ffffff", relief="ridge", bd=2)
extract_button.pack(pady=5)

input_box_label = tk.Label(input_frame, text="Extracted Text:", font=("Arial", 12), bg="#e0e0e0")
input_box_label.pack(pady=5)
input_box = tk.Text(input_frame, height=10, width=50, font=("Arial", 12), bg="#ffffff")
input_box.pack(pady=5)

translate_button = tk.Button(input_frame, text="Translate Text", command=translate_text, font=("Arial", 12), bg="#4CAF50", fg="#ffffff", relief="ridge", bd=2)
translate_button.pack(pady=5)

language_var = tk.StringVar()
language_var.set("English")
language_option = tk.OptionMenu(input_frame, language_var, "Tamil", "Telugu", "English", "Kannada", "Hindi")
language_option.pack(pady=5)

output_box_label = tk.Label(input_frame, text="Translated Text:", font=("Arial", 12), bg="#e0e0e0")
output_box_label.pack(pady=5)
output_box = tk.Text(input_frame, height=10, width=50, font=("Arial", 12), bg="#ffffff")
output_box.pack(pady=5)

speak_button = tk.Button(input_frame, text="Speak Text", command=speak_text, font=("Arial", 12), bg="#4CAF50", fg="#ffffff", relief="ridge", bd=2)
speak_button.pack(pady=5)

root.mainloop()