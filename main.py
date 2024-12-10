import cv2
import numpy as np
from tkinter import Tk, Label, Button, filedialog, OptionMenu, StringVar, Entry, Frame
from PIL import Image, ImageTk

class ImageProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        self.image_path = None
        self.original_image = None
        self.processed_image = None

        self.create_widgets()

    def create_widgets(self):
        self.load_button = Button(self.root, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=10)

        self.sharpen_button = Button(self.root, text="Sharpen Image", command=self.sharpen_image)
        self.sharpen_button.pack(pady=10)

        self.morph_frame = Frame(self.root)
        self.morph_frame.pack(pady=10)

        self.morph_label = Label(self.morph_frame, text="Morphological Operation:")
        self.morph_label.pack(side="left")

        self.morph_options = ["Erosion", "Dilation", "Opening", "Closing"]
        self.morph_var = StringVar(self.root)
        self.morph_var.set(self.morph_options[0])
        self.morph_menu = OptionMenu(self.morph_frame, self.morph_var, *self.morph_options)
        self.morph_menu.pack(side="left")

        self.kernel_label = Label(self.morph_frame, text="Kernel Size:")
        self.kernel_label.pack(side="left")

        self.kernel_entry = Entry(self.morph_frame, width=5)
        self.kernel_entry.pack(side="left")
        self.kernel_entry.insert(0, "3")

        self.morph_button = Button(self.root, text="Apply Morphological Operation", command=self.apply_morphological_operation)
        self.morph_button.pack(pady=10)

        self.image_label = Label(self.root)
        self.image_label.pack(pady=10)

    def load_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.original_image = cv2.imread(self.image_path)
            self.processed_image = self.original_image.copy()
            self.display_image(self.original_image)

    def sharpen_image(self):
        if self.original_image is not None:
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
            self.processed_image = cv2.filter2D(self.original_image, -1, kernel)
            self.display_image(self.processed_image)

    def apply_morphological_operation(self):
        if self.original_image is not None:
            kernel_size = int(self.kernel_entry.get())
            kernel = np.ones((kernel_size, kernel_size), np.uint8)
            operation = self.morph_var.get()

            if operation == "Erosion":
                self.processed_image = cv2.erode(self.original_image, kernel, iterations=1)
            elif operation == "Dilation":
                self.processed_image = cv2.dilate(self.original_image, kernel, iterations=1)
            elif operation == "Opening":
                self.processed_image = cv2.morphologyEx(self.original_image, cv2.MORPH_OPEN, kernel)
            elif operation == "Closing":
                self.processed_image = cv2.morphologyEx(self.original_image, cv2.MORPH_CLOSE, kernel)

            self.display_image(self.processed_image)

    def display_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        self.image_label.config(image=image)
        self.image_label.image = image

if __name__ == "__main__":
    root = Tk()
    app = ImageProcessor(root)
    root.mainloop()
