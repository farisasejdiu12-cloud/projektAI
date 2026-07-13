from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

import numpy as np
from PIL import Image, ImageOps, ImageTk
from tensorflow.keras.models import load_model

# ============================================================
# SETTINGS
# ============================================================

APP_TITLE = "AI Flower Classification App"

MODEL_FOLDER = "model"
MODEL_FILE = "keras_model.h5"
LABELS_FILE = "labels.txt"

WINDOW_SIZE = "650x800"
PREVIEW_SIZE = (500, 500)
IMAGE_SIZE = (224, 224)

# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#1E1E2E"
CARD_COLOR = "#2A2A3C"
ACCENT_COLOR = "#00C896"
ACCENT_HOVER = "#00A67E"
TEXT_COLOR = "#FFFFFF"
SECONDARY_TEXT = "#CFCFCF"

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / MODEL_FOLDER / MODEL_FILE
LABELS_PATH = BASE_DIR / MODEL_FOLDER / LABELS_FILE

# ============================================================
# LOAD LABELS
# ============================================================

def load_labels():
    labels = []

    with open(LABELS_PATH, "r", encoding="utf-8") as file:
        for line in file:
            label = line.strip()
            if not label:
                continue

            parts = label.split(" ", 1)

            if len(parts) == 2 and parts[0].isdigit():
                labels.append(parts[1])
            else:
                labels.append(label)

    return labels

# ============================================================
# IMAGE PREPARATION
# ============================================================

def prepare_image(image_path):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    image = Image.open(image_path).convert("RGB")

    image = ImageOps.fit(
        image,
        IMAGE_SIZE,
        Image.Resampling.LANCZOS
    )

    image_array = np.asarray(image)

    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    data[0] = normalized_image_array

    return data

# ============================================================
# PREDICTION
# ============================================================

def classify_flower(image_path):
    data = prepare_image(image_path)

    prediction = model.predict(data, verbose=0)

    index = int(np.argmax(prediction[0]))
    flower = class_names[index]
    confidence = float(prediction[0][index])

    return index, flower, confidence

# ============================================================
# IMAGE PREVIEW
# ============================================================

def show_image_preview(file_path):
    image = Image.open(file_path).convert("RGB")
    image.thumbnail(PREVIEW_SIZE)

    photo = ImageTk.PhotoImage(image)

    image_label.config(image=photo, text="")
    image_label.image = photo

# ============================================================
# HIGHLIGHT LABEL
# ============================================================

def highlight_flower(index):
    for i, label in enumerate(flower_labels):
        if i == index:
            label.config(
                bg=ACCENT_COLOR,
                fg="white",
                font=("Arial", 13, "bold")
            )
        else:
            label.config(
                bg=CARD_COLOR,
                fg=TEXT_COLOR,
                font=("Arial", 12)
            )

# ============================================================
# UPLOAD IMAGE
# ============================================================

def upload_image():
    file_path = filedialog.askopenfilename(
        title="Choose Flower Image",
        filetypes=[
            ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.webp"),
            ("All files", "*.*")
        ]
    )

    if not file_path:
        return

    try:
        show_image_preview(file_path)

        index, flower, confidence = classify_flower(file_path)

    except Exception as error:
        messagebox.showerror("Error", f"Prediction failed:\n{error}")
        return

    result_label.config(
        text=f"Predicted Flower: {flower}\nConfidence: {confidence * 100:.2f}%"
    )

    highlight_flower(index)

# ============================================================
# LOAD MODEL
# ============================================================

try:
    model = load_model(MODEL_PATH, compile=False)
    class_names = load_labels()

except Exception as error:
    messagebox.showerror("Model Error", f"Could not load model:\n{error}")
    raise

# ============================================================
# GUI
# ============================================================

app = tk.Tk()
app.title(APP_TITLE)
app.geometry(WINDOW_SIZE)
app.configure(bg=BG_COLOR)

title_label = tk.Label(
    app,
    text=APP_TITLE,
    font=("Arial", 22, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
title_label.pack(pady=15)

image_label = tk.Label(
    app,
    text="Upload a flower image",
    font=("Arial", 14),
    bg=CARD_COLOR,
    fg=SECONDARY_TEXT,
    width=45,
    height=14
)
image_label.pack(pady=20)

upload_button = tk.Button(
    app,
    text="Upload Image",
    command=upload_image,
    bg=ACCENT_COLOR,
    fg="white",
    font=("Arial", 14, "bold"),
    padx=25,
    pady=12
)
upload_button.pack(pady=10)

result_label = tk.Label(
    app,
    text="Flower prediction will appear here",
    font=("Arial", 16),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
result_label.pack(pady=20)

classes_title = tk.Label(
    app,
    text="Flower Classes",
    font=("Arial", 16, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
classes_title.pack(pady=10)

classes_frame = tk.Frame(app, bg=BG_COLOR)
classes_frame.pack()

flower_labels = []

for flower in class_names:
    lbl = tk.Label(
        classes_frame,
        text=flower,
        width=25,
        bg=CARD_COLOR,
        fg=TEXT_COLOR,
        font=("Arial", 12),
        pady=6
    )
    lbl.pack(pady=3)
    flower_labels.append(lbl)

app.mainloop()
