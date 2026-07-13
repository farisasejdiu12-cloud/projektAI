from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

from prediction import predict_flower


APP_TITLE = "Flower Classification App"
UPLOAD_BUTTON_TEXT = "Choose Flower Image"
EMPTY_IMAGE_TEXT = "Upload a flower image"
RESULT_EMPTY_TEXT = "Flower result will appear here"

PREVIEW_SIZE = (320, 240)


class FlowerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("520x520")
        self.preview_image = None

        self.title_label = tk.Label(
            root,
            text=APP_TITLE,
            font=("Segoe UI", 18, "bold"),
        )
        self.title_label.pack(pady=(18, 8))

        self.image_label = tk.Label(
            root,
            text=EMPTY_IMAGE_TEXT,
            width=42,
            height=14,
            relief="solid",
            borderwidth=1,
        )
        self.image_label.pack(pady=12)

        self.choose_button = tk.Button(
            root,
            text=UPLOAD_BUTTON_TEXT,
            command=self.choose_image,
            font=("Segoe UI", 11),
        )
        self.choose_button.pack(pady=8)

        self.result_label = tk.Label(
            root,
            text=RESULT_EMPTY_TEXT,
            font=("Segoe UI", 14, "bold"),
        )
        self.result_label.pack(pady=(20, 4))

        self.confidence_label = tk.Label(
            root,
            text="Confidence: -",
            font=("Segoe UI", 12),
        )
        self.confidence_label.pack()

        self.path_label = tk.Label(
            root,
            text="",
            font=("Segoe UI", 9),
            wraplength=460,
            fg="#555555",
        )
        self.path_label.pack(pady=(18, 0))

    def choose_image(self):
        image_path = filedialog.askopenfilename(
            title="Choose Flower Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.webp"),
                ("All files", "*.*"),
            ],
        )

        if not image_path:
            return

        self.show_preview(image_path)
        self.predict(image_path)

    def show_preview(self, image_path):
        image = Image.open(image_path).convert("RGB")
        image.thumbnail(PREVIEW_SIZE)
        self.preview_image = ImageTk.PhotoImage(image)
        self.image_label.configure(image=self.preview_image, text="")
        self.path_label.configure(text=str(Path(image_path)))

    def predict(self, image_path):
        try:
            result = predict_flower(image_path)
        except Exception as error:
            messagebox.showerror("Prediction Error", str(error))
            return

        self.result_label.configure(
            text=f"Flower: {result['flower_class']}"
        )

        self.confidence_label.configure(
            text=f"Confidence: {result['confidence']:.2%}"
        )


def main():
    root = tk.Tk()
    app = FlowerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
