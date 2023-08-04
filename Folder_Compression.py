# import os
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QLabel, QWidget
# from PIL import Image

# class ImageCompressor(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle("Image Compressor")
#         self.setGeometry(100, 100, 400, 200)

#         layout = QVBoxLayout()

#         self.label = QLabel("Select a folder to compress images:")
#         layout.addWidget(self.label)

#         self.compress_button = QPushButton("Compress Images")
#         self.compress_button.clicked.connect(self.compressImages)
#         layout.addWidget(self.compress_button)

#         central_widget = QWidget()
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)

#     def compressImages(self):
#         options = QFileDialog.Options()
#         folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)

#         if folder_path:
#             output_folder = os.path.join(folder_path, "compressed_images")
#             os.makedirs(output_folder, exist_ok=True)

#             for file_name in os.listdir(folder_path):
#                 if file_name.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
#                     image_path = os.path.join(folder_path, file_name)
#                     output_path = os.path.join(output_folder, file_name)
#                     self.compressImage(image_path, output_path)

#             self.label.setText("Images compressed successfully!")

#     def compressImage(self, input_path, output_path):
#         compress_ratio = 0.8  # Adjust this value based on your compression needs
#         image = Image.open(input_path)
#         compressed_image = image.resize((int(image.width * compress_ratio), int(image.height * compress_ratio)), Image.ANTIALIAS)
#         compressed_image.save(output_path)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = ImageCompressor()
#     window.show()
#     sys.exit(app.exec_())







# import os
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QLabel, QWidget, QProgressDialog
# from PIL import Image

# class ImageCompressor(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle("Image Compressor")
#         self.setGeometry(100, 100, 400, 200)

#         layout = QVBoxLayout()

#         self.label = QLabel("Select a folder to compress images:")
#         layout.addWidget(self.label)

#         self.compress_button = QPushButton("Compress Images")
#         self.compress_button.clicked.connect(self.compressImages)
#         layout.addWidget(self.compress_button)

#         central_widget = QWidget()
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)

#     def compressImages(self):
#         options = QFileDialog.Options()
#         folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)

#         if folder_path:
#             output_folder = os.path.join(folder_path, "compressed_images")
#             os.makedirs(output_folder, exist_ok=True)

#             image_list = [file_name for file_name in os.listdir(folder_path) if file_name.lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))]

#             progress_dialog = QProgressDialog("Compressing Images...", None, 0, len(image_list), self)
#             progress_dialog.setWindowTitle("Progress")
#             progress_dialog.setWindowModality(2)  # ApplicationModal
#             progress_dialog.setAutoReset(False)
#             progress_dialog.setAutoClose(False)
#             progress_dialog.setValue(0)
#             progress_dialog.show()

#             compressed_images_count = 0
#             for index, file_name in enumerate(image_list):
#                 image_path = os.path.join(folder_path, file_name)
#                 output_path = os.path.join(output_folder, file_name)
#                 self.compressImage(image_path, output_path)

#                 compressed_images_count += 1
#                 progress_dialog.setValue(compressed_images_count)

#             progress_dialog.close()

#             self.label.setText("Images compressed successfully!")

#     def compressImage(self, input_path, output_path):
#         compress_ratio = 0.8  # Adjust this value based on your compression needs
#         image = Image.open(input_path)
#         compressed_image = image.resize((int(image.width * compress_ratio), int(image.height * compress_ratio)), Image.ANTIALIAS)
#         compressed_image.save(output_path)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = ImageCompressor()
#     window.show()
#     sys.exit(app.exec_())

# OSError cannot write mode RGBA as JPEG


# import os
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QLabel, QWidget, QProgressDialog
# from PIL import Image, ImageEnhance

# class ImageCompressor(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle("Image Compressor")
#         self.setGeometry(100, 100, 500, 200)

#         layout = QVBoxLayout()

#         self.label = QLabel("Select a folder to compress images:")
#         layout.addWidget(self.label)

#         self.compress_button = QPushButton("Compress Images")
#         self.compress_button.clicked.connect(self.compressImages)
#         layout.addWidget(self.compress_button)

#         self.watermark_label = QLabel("Select a watermark image:")
#         layout.addWidget(self.watermark_label)

#         self.watermark_button = QPushButton("Browse Watermark")
#         self.watermark_button.clicked.connect(self.selectWatermark)
#         layout.addWidget(self.watermark_button)

#         central_widget = QWidget()
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)

#         self.watermark_image_path = ""

#     def selectWatermark(self):
#         options = QFileDialog.Options()
#         file_path, _ = QFileDialog.getOpenFileName(self, "Select Watermark Image", "", "Image Files (*.jpg *.jpeg *.png *.bmp);;All Files (*)", options=options)

#         if file_path:
#             self.watermark_image_path = file_path
#             self.watermark_label.setText("Watermark image selected: " + os.path.basename(file_path))

#     def compressImages(self):
#         options = QFileDialog.Options()
#         folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)

#         if folder_path:
#             output_folder = os.path.join(folder_path, "compressed_images")
#             os.makedirs(output_folder, exist_ok=True)

#             image_list = [file_name for file_name in os.listdir(folder_path) if file_name.lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))]

#             progress_dialog = QProgressDialog("Compressing Images...", None, 0, len(image_list), self)
#             progress_dialog.setWindowTitle("Progress")
#             progress_dialog.setWindowModality(2)  # ApplicationModal
#             progress_dialog.setAutoReset(False)
#             progress_dialog.setAutoClose(False)
#             progress_dialog.setValue(0)
#             progress_dialog.show()

#             compressed_images_count = 0
#             for index, file_name in enumerate(image_list):
#                 image_path = os.path.join(folder_path, file_name)
#                 output_path = os.path.join(output_folder, file_name)
#                 self.compressImage(image_path, output_path)

#                 if self.watermark_image_path:
#                     self.addWatermark(output_path)

#                 compressed_images_count += 1
#                 progress_dialog.setValue(compressed_images_count)

#             progress_dialog.close()

#             self.label.setText("Images compressed successfully!")

#     def compressImage(self, input_path, output_path):
#         compress_ratio = 0.8  # Adjust this value based on your compression needs
#         image = Image.open(input_path)
#         compressed_image = image.resize((int(image.width * compress_ratio), int(image.height * compress_ratio)), Image.ANTIALIAS)
#         compressed_image.save(output_path)

#     def addWatermark(self, image_path):
#         image = Image.open(image_path)
#         watermark = Image.open(self.watermark_image_path)
#         watermark = watermark.resize(image.size, Image.ANTIALIAS)

#         alpha = 0.6  # Adjust this value to control the opacity of the watermark

#         # Blend the images using alpha blending
#         blended_image = Image.blend(image.convert("RGBA"), watermark.convert("RGBA"), alpha)

#         # Save the final watermarked image
#         enhanced_image = ImageEnhance.Brightness(blended_image).enhance(0.8)  # Adjust brightness
#         enhanced_image.save(image_path)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = ImageCompressor()
#     window.show()
#     sys.exit(app.exec_())




# import os
# import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QLabel, QWidget, QProgressDialog
# from PIL import Image, ImageEnhance, UnidentifiedImageError

# class ImageCompressor(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle("Image Compressor")
#         self.setGeometry(100, 100, 500, 200)

#         layout = QVBoxLayout()

#         self.label = QLabel("Select a folder to compress images:")
#         layout.addWidget(self.label)

#         self.compress_button = QPushButton("Compress Images")
#         self.compress_button.clicked.connect(self.compressImages)
#         layout.addWidget(self.compress_button)

#         self.watermark_label = QLabel("Select a watermark image:")
#         layout.addWidget(self.watermark_label)

#         self.watermark_button = QPushButton("Browse Watermark")
#         self.watermark_button.clicked.connect(self.selectWatermark)
#         layout.addWidget(self.watermark_button)

#         central_widget = QWidget()
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)

#         self.watermark_image_path = ""

#     def selectWatermark(self):
#         options = QFileDialog.Options()
#         file_path, _ = QFileDialog.getOpenFileName(self, "Select Watermark Image", "", "Image Files (*.jpg *.jpeg *.png *.bmp);;All Files (*)", options=options)

#         if file_path:
#             self.watermark_image_path = file_path
#             self.watermark_label.setText("Watermark image selected: " + os.path.basename(file_path))

#     def compressImages(self):
#         options = QFileDialog.Options()
#         folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)

#         if folder_path:
#             output_folder = os.path.join(folder_path, "compressed_images")
#             os.makedirs(output_folder, exist_ok=True)  # Create the output_folder if it doesn't exist

#             progress_dialog = QProgressDialog("Compressing Images...", None, 0, 0, self)
#             progress_dialog.setWindowTitle("Progress")
#             progress_dialog.setWindowModality(2)  # ApplicationModal
#             progress_dialog.setAutoReset(False)
#             progress_dialog.setAutoClose(False)
#             progress_dialog.show()

#             for root, _, file_names in os.walk(folder_path):
#                 for file_name in file_names:
#                     if file_name.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
#                         image_path = os.path.join(root, file_name)
#                         output_path = os.path.join(output_folder, file_name)
#                         self.compressImage(image_path, output_path)

#                         if self.watermark_image_path:
#                             self.addWatermark(output_path)

#             progress_dialog.close()
#             self.label.setText("Images compressed successfully!")

#     def compressImage(self, input_path, output_path):
#         # Starting compression ratio
#         compress_ratio = 1.0

#         # Target maximum file size in bytes (e.g., 200KB)
#         max_file_size_bytes = 200 * 1024

#         while True:
#             try:
#                 image = Image.open(input_path)
#                 compressed_image = image.resize((int(image.width * compress_ratio), int(image.height * compress_ratio)), Image.ANTIALIAS)

#                 # Save the compressed image to the output path
#                 compressed_image.save(output_path, optimize=True, quality=95)

#                 # Check the file size of the compressed image
#                 file_size_bytes = os.path.getsize(output_path)

#                 if file_size_bytes <= max_file_size_bytes:
#                     # The file size is within the limit, so we can keep the compressed image
#                     break
#                 else:
#                     # The file size is still larger than the limit, so we reduce the compression ratio
#                     compress_ratio -= 0.05
#                     if compress_ratio <= 0:
#                         # In case the compression ratio becomes too small, break the loop
#                         break
#             except UnidentifiedImageError:
#                 # Skip the current file if it cannot be identified as an image
#                 break

#     def addWatermark(self, image_path):
#         image = Image.open(image_path)
#         watermark = Image.open(self.watermark_image_path)
#         watermark = watermark.resize((200, 200), Image.ANTIALIAS)

#         # Calculate the position to center the watermark
#         position_x = (image.width - watermark.width) // 2
#         position_y = (image.height - watermark.height) // 2

#         # Blend the images using alpha blending
#         blended_image = Image.alpha_composite(image.convert("RGBA"), watermark.convert("RGBA"))

#         # Save the final watermarked image
#         enhanced_image = ImageEnhance.Brightness(blended_image).enhance(0.8)  # Adjust brightness
#         enhanced_image.save(image_path)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = ImageCompressor()
#     window.show()
#     sys.exit(app.exec_())





import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QLabel, QWidget, QProgressDialog
from PIL import Image

class ImageCompressor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Compressor")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Select a folder to compress images:")
        layout.addWidget(self.label)

        self.compress_button = QPushButton("Compress Images")
        self.compress_button.clicked.connect(self.compressImages)
        layout.addWidget(self.compress_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def compressImages(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)

        if folder_path:
            output_folder = os.path.join(folder_path, "compressed_images")
            os.makedirs(output_folder, exist_ok=True)

            image_list = [file_name for file_name in os.listdir(folder_path) if file_name.lower().endswith((".jpg", ".jpeg", ".png", ".bmp"))]

            progress_dialog = QProgressDialog("Compressing Images...", None, 0, len(image_list), self)
            progress_dialog.setWindowTitle("Progress")
            progress_dialog.setWindowModality(2)  # ApplicationModal
            progress_dialog.setAutoReset(False)
            progress_dialog.setAutoClose(False)
            progress_dialog.show()

            compressed_images_count = 0
            for index, file_name in enumerate(image_list):
                image_path = os.path.join(folder_path, file_name)
                output_path = os.path.join(output_folder, file_name)
                self.compressImage(image_path, output_path)

                compressed_images_count += 1
                progress_dialog.setValue(compressed_images_count)

            progress_dialog.close()

            self.label.setText("Images compressed successfully!")

    def compressImage(self, input_path, output_path):
        compress_ratio = 0.8  # Adjust this value based on your compression needs
        image = Image.open(input_path)

        # If the image has an alpha channel (transparency), convert it to RGB mode
        if image.mode in ('RGBA', 'LA'):
            image = image.convert('RGB')

        # If the image is in palette mode (mode 'P'), convert it to RGB mode
        if image.mode == 'P':
            image = image.convert('RGB')

        compressed_image = image.resize((int(image.width * compress_ratio), int(image.height * compress_ratio)), Image.ANTIALIAS)
        compressed_image.save(output_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageCompressor()
    window.show()
    sys.exit(app.exec_())
