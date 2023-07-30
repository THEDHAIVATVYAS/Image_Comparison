from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import os
from PIL import Image, ImageDraw, ImageFont
import fitz

class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting title
        self.setWindowTitle("Images and Other File compresions and Operations")

        # setting geometry
        self.setGeometry(100, 100, 500, 400)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

        # Initialize watermark image path to None
        self.watermark_image_path = None

    # method for components
    def UiComponents(self):
        # creating a tool bar
        toolbar = QToolBar(self)

        # setting geometry to the tool bar
        toolbar.setGeometry(10, 10, 300, 35)

        # creating the menu for multiple actions
        menu = QMenu(self)
        menu.addAction("Convert PDF to JPG", self.convert_pdf_to_image)
        menu.addAction("Convert JPG to WEBP", self.convert_jpg_to_webp)
        menu.addAction("Add Watermark", self.add_watermark)
        menu.addAction("Select Watermark Image", self.select_watermark_image)

        # creating a QAction to represent the menu
        action = QAction("Images and File Operations", self)
        action.setMenu(menu)
        toolbar.addAction(action)

        # creating a label
        self.label = QLabel("Image Compression Process", self)
        self.label.setGeometry(20, 50, 200, 50)

        # creating a progress bar
        self.progress = QProgressBar(self)
        self.progress.setGeometry(20, 110, 200, 25)
        self.progress.setVisible(False)

    def convert_pdf_to_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf);;All Files (*)", options=options)

        if file_name:
            # open the selected file
            doc = fitz.open(file_name)
            total_pages = doc.page_count
            self.progress.setMaximum(total_pages)
            self.progress.setValue(0)
            self.progress.setVisible(True)

            # create a folder to save images (if not already present)
            output_folder = os.path.dirname(file_name)
            if not os.path.exists(os.path.join(output_folder, "images")):
                os.makedirs(os.path.join(output_folder, "images"))

            # iterate through the pages of the document and create a JPG image of each page
            for page_num, page in enumerate(doc, 1):
                pix = page.get_pixmap()
                image_path = os.path.join(output_folder, "images", f"page-{page_num}.jpg")
                pix.save(image_path)

                self.progress.setValue(page_num)
                QApplication.processEvents()

            self.progress.setVisible(False)
            self.label.setText("PDF Converted to JPG!")

    def convert_jpg_to_webp(self):
        options = QFileDialog.Options()
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)

        if folder:
            total_files = len([file for file in os.listdir(folder) if file.lower().endswith((".jpg", ".jpeg"))])
            self.progress.setMaximum(total_files)
            self.progress.setValue(0)
            self.progress.setVisible(True)

            for idx, file in enumerate(os.listdir(folder)):
                if file.lower().endswith((".jpg", ".jpeg")):
                    file_path = os.path.join(folder, file)
                    image = Image.open(file_path)

                    # Resize the image to compress it and maintain aspect ratio
                    compress_ratio = 0.8  # You can adjust this value based on your compression needs
                    image = image.resize((int(image.width * compress_ratio), int(image.height * compress_ratio)), Image.ANTIALIAS)

                    # Save the image in WebP format
                    webp_path = os.path.join(folder, f"{os.path.splitext(file)[0]}.webp")
                    image.save(webp_path, "WebP", quality=80)

                    # Check if the image is less than 150 KB
                    if os.path.getsize(webp_path) <= 150 * 1024:  # 150 KB in bytes
                        self.label.setText(f"{file} converted and compressed successfully!")
                    else:
                        self.label.setText(f"{file} compression failed. Image size > 150 KB.")

                    self.progress.setValue(idx + 1)
                    QApplication.processEvents()

            self.progress.setVisible(False)
            self.label.setText("JPG to WebP Conversion and Compression Complete!")

    def select_watermark_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)", options=options)

        if file_name:
            self.watermark_image_path = file_name
            self.label.setText("Watermark Image Selected")

    def add_watermark(self):
        if not self.watermark_image_path:
            self.label.setText("Please select a watermark image first.")
            return

        options = QFileDialog.Options()
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)

        if folder:
            # List the WebP files in the folder
            image_files = [file for file in os.listdir(folder) if file.lower().endswith(".webp")]
            total_files = len(image_files)

            self.progress.setMaximum(total_files)
            self.progress.setValue(0)
            self.progress.setVisible(True)

            watermark = Image.open(self.watermark_image_path).convert("RGBA")
            watermark_width, watermark_height = watermark.size

            for idx, file in enumerate(image_files):
                file_path = os.path.join(folder, file)
                image = Image.open(file_path).convert("RGBA")
                image_width, image_height = image.size

                # Calculate the position to center the watermark on the image
                x = (image_width - watermark_width) // 2
                y = (image_height - watermark_height) // 2

                watermarked = Image.alpha_composite(image, watermark.resize((image_width, image_height)))

                # Dynamically adjust WebP compression quality to achieve target file size
                target_file_size = 150 * 1024  # Target file size between 100 KB and 200 KB in bytes
                quality = 80
                while True:
                    webp_path = os.path.join(folder, f"{os.path.splitext(file)[0]}_watermarked.webp")
                    watermarked.save(webp_path, "WebP", quality=quality)

                    file_size = os.path.getsize(webp_path)
                    if file_size <= target_file_size:
                        break
                    quality -= 5

                self.progress.setValue(idx + 1)
                QApplication.processEvents()

            self.progress.setVisible(False)
            self.label.setText("Watermark added successfully!")


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())
