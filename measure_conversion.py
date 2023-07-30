# import os
# import sys
# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit, QMessageBox, QProgressBar, QMenu
# from PyQt5.QtCore import QBuffer, QIODevice, Qt
# import shutil
# import fitz
# from PIL import Image
# from PyQt5.QtGui import QFont, QPalette, QColor

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("Image Conversion and Compression")
#         self.setGeometry(100, 100, 400, 400)
#         # Set the background color of the main window
#         palette = self.palette()
#         palette.setColor(QPalette.Window, QColor(255, 255, 255))  # Set the color to red
#         self.setPalette(palette)

#         self.layout = QVBoxLayout()

#         self.label = QLabel("Image Paths:")
#         self.layout.addWidget(self.label)

#         self.path_text = QTextEdit()
#         self.layout.addWidget(self.path_text)

#         self.browse_button = QPushButton("Browse Images")
#         self.browse_button.clicked.connect(self.browse_images)
#         self.layout.addWidget(self.browse_button)
#         self.browse_button.setStyleSheet("QPushButton { background-color: #3F00FF; color: white; font-size: 10px; font-weight: bold; font-family: Ubuntu;}")
#         self.browse_button.setFixedSize(86, 30)  # Set width = 100, height = 50
        
#         self.convert_button = QPushButton("Convert to WebP")
#         self.convert_button.clicked.connect(self.convert_to_webp)
#         self.layout.addWidget(self.convert_button)
#         self.convert_button.setStyleSheet("QPushButton { background-color: #3F00FF; color: white; font-size: 10px; font-weight: bold; font-family: Ubuntu;}")
#         self.convert_button.setFixedSize(86, 30)  # Set width = 100, height = 50

#         self.compress_webp_button = QPushButton("Compress WebP")
#         self.compress_webp_button.clicked.connect(self.compress_webp_images)
#         self.layout.addWidget(self.compress_webp_button)
#         self.compress_webp_button.setStyleSheet("QPushButton { background-color: #3F00FF; color: white; font-size: 10px; font-weight: bold; font-family: Ubuntu;}")
#         self.compress_webp_button.setFixedSize(86, 30)  # Set width = 100, height = 50

#         self.setLayout(self.layout)

#         self.image_paths = []
#         self.output_folder = "webp"
#         self.webp_folder_label = QLabel("WebP Folder Path: ")
#         self.layout.addWidget(self.webp_folder_label)

#         self.file_path = None

#         self.btn_open = QPushButton("Open PDF", self)
#         self.btn_open.setGeometry(100, 300, 200, 30)
#         self.btn_open.clicked.connect(self.open_pdf)
#         self.btn_open.setStyleSheet("QPushButton { background-color: #3F00FF; color: white; font-size: 10px; font-weight: bold; font-family: Ubuntu;}")
#         self.btn_open.setFixedSize(86, 30)  # Set width = 100, height = 50
#         self.btn_open.setGeometry(100, 547, 86, 30)

#         self.btn_extract = QPushButton("Extract Images", self)
#         self.btn_extract.setGeometry(100, 350, 200, 30)
#         self.btn_extract.clicked.connect(self.extract_images)
#         self.btn_extract.setEnabled(False)
#         self.btn_extract.setStyleSheet("QPushButton { background-color: #3F00FF; color: white; font-size: 10px; font-weight: bold; font-family: Ubuntu;}")
#         self.btn_extract.setFixedSize(86, 30)  # Set width = 100, height = 50
#         self.btn_extract.setGeometry(190, 547, 86, 30)

#         self.clear_button = QPushButton("Clear")
#         self.clear_button.clicked.connect(self.clear_image_paths)
#         self.layout.addWidget(self.clear_button)
#         self.clear_button.setStyleSheet("QPushButton { background-color: #3F00FF; color: white; font-size: 10px; font-weight: bold; font-family: Ubuntu;}")
#         self.clear_button.setFixedSize(86, 30)  # Set width = 100, height = 50
#         self.clear_button.setGeometry(90, 547, 86, 30)

#         self.progress_bar = QProgressBar()
#         self.layout.addWidget(self.progress_bar)

#     def browse_images(self):
#         file_dialog = QFileDialog()
#         image_paths, _ = file_dialog.getOpenFileNames(
#             self, "Open Image files", filter="Image Files (*.jpg *.jpeg)"
#         )
#         if image_paths:
#             self.image_paths = image_paths
#             self.display_image_paths()

#     def display_image_paths(self):
#         self.path_text.clear()
#         for path in self.image_paths:
#             self.path_text.append(path)

#     def convert_to_webp(self):
#         if self.image_paths:
#             try:
#                 # Prompt the user to select the output folder
#                 file_dialog = QFileDialog()
#                 output_folder = file_dialog.getExistingDirectory(
#                     self, "Select Output Folder"
#                 )
#                 if output_folder:
#                     # Create the output folder if it doesn't exist
#                     os.makedirs(output_folder, exist_ok=True)
#                     webp_folder_path = os.path.abspath(output_folder)
#                     self.webp_folder_label.setText("WebP Folder Path: " + webp_folder_path)

#                     total_images = len(self.image_paths)
#                     self.progress_bar.setMaximum(total_images)
#                     self.progress_bar.setValue(0)

#                     for i, image_path in enumerate(self.image_paths):
#                         img = Image.open(image_path)

#                         # Construct the output file path with a '.webp' extension
#                         file_name = os.path.splitext(os.path.basename(image_path))[0]
#                         output_path = os.path.join(output_folder, file_name + ".webp")

#                         # Convert JPG to WebP
#                         img.save(output_path, "WEBP")

#                         # Copy the converted WebP file to the original image's folder within the 'webp' folder
#                         original_folder = os.path.dirname(image_path)
#                         webp_output_path = os.path.join(original_folder, file_name + ".webp")
#                         os.makedirs(os.path.dirname(webp_output_path), exist_ok=True)
#                         shutil.copy(output_path, webp_output_path)

#                         self.progress_bar.setValue(i + 1)

#                     QMessageBox.information(
#                         self,
#                         "Conversion Successful",
#                         "Images converted to WebP and stored in the respective folders successfully.",
#                     )
#             except Exception as e:
#                 QMessageBox.critical(self, "Conversion Error", str(e))
#         else:
#             QMessageBox.warning(self, "No Images Selected", "Please select one or more JPG images.")


#     def compress_webp_images(self):
#         if self.image_paths:
#             try:
#                 # Prompt the user to select the output folder
#                 file_dialog = QFileDialog()
#                 output_folder = file_dialog.getExistingDirectory(
#                     self, "Select Output Folder"
#                 )
#                 if output_folder:
#                     total_images = len(self.image_paths)
#                     self.progress_bar.setMaximum(total_images)
#                     self.progress_bar.setValue(0)

#                     for i, image_path in enumerate(self.image_paths):
#                         img = Image.open(image_path)

#                         # Construct the output file path with a '_compressed.webp' extension
#                         file_name = os.path.splitext(os.path.basename(image_path))[0]
#                         output_path = os.path.join(output_folder, file_name + "_compressed.webp")

#                         self.compress_webp(image_path, output_path, max_size_kb=100)

#                         self.progress_bar.setValue(i+1)

#                     QMessageBox.information(
#                         self,
#                         "Compression Successful",
#                         "WebP images compressed successfully.",
#                     )
#             except Exception as e:
#                 QMessageBox.critical(self, "Compression Error", str(e))
#         else:
#             QMessageBox.warning(self, "No Images Selected", "Please select one or more WebP images.")


#     def compress_webp(self, input_path, output_path, max_size_kb=100, quality=80):
#         image = Image.open(input_path)

#         # Compress the image with the specified quality
#         image.save(output_path, "webp", quality=quality)

#         # Loop until the compressed image size is less than the maximum size limit
#         while os.path.getsize(output_path) > max_size_kb * 1024 and quality > 10:
#             quality -= 10
#             image.save(output_path, "webp", quality=quality)

#         # Check the final file size
#         file_size = os.path.getsize(output_path)
#         if file_size <= max_size_kb * 1024:
#             print(f"Image {output_path} compressed successfully. File size: {file_size} bytes.")
#         else:
#             print(f"Image {output_path} could not be compressed within the size limit.")

#     def open_pdf(self):
#         file_dialog = QFileDialog()
#         file_dialog.setFileMode(QFileDialog.ExistingFile)
#         file_dialog.setNameFilter("PDF Files (*.pdf)")

#         if file_dialog.exec_():
#             selected_files = file_dialog.selectedFiles()
#             self.file_path = selected_files[0]
#             self.btn_extract.setEnabled(True)
    
#     def clear_image_paths(self):
#         self.image_paths = []
#         self.path_text.clear()
    
#     def extract_images(self):
#         if not self.file_path:
#             QMessageBox.critical(self, "Error", "No PDF file selected.")
#             return

#         try:
#             doc = fitz.open(self.file_path)
#             pdf_folder = os.path.dirname(self.file_path)
#             images_folder = os.path.splitext(self.file_path)[0] + "_images"
#             os.makedirs(images_folder, exist_ok=True)

#             total_images = 0
#             for i in range(len(doc)):
#                 for img in doc.get_page_images(i):
#                     total_images += 1

#             self.progress_bar.setMaximum(total_images)
#             self.progress_bar.setValue(0)

#             image_count = 0
#             for i in range(len(doc)):
#                 for img in doc.get_page_images(i):
#                     xref = img[0]
#                     base_image = doc.extract_image(xref)
#                     image_data = base_image["image"]
#                     image_format = base_image["ext"]

#                     image_path = os.path.join(images_folder, f"image_{i}.{image_format}")
#                     with open(image_path, "wb") as f:
#                         f.write(image_data)

#                     # Convert the image to JPG format
#                     jpg_path = os.path.join(images_folder, f"image_{i}.jpg")
#                     with Image.open(image_path) as img:
#                         img.save(jpg_path, "JPEG")

#                     # Optionally, remove the original image file
#                     os.remove(image_path)

#                     image_count += 1
#                     self.progress_bar.setValue(image_count)

#             QMessageBox.information(self, "Success", "Images extracted and converted successfully.")
#         except Exception as e:
#             QMessageBox.critical(self, "Error", str(e))

# def main():
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()

# #give me a functionality to ask where to save Compress to webp


import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit, QMessageBox, QProgressBar, QMenuBar, QAction
from PyQt5.QtCore import QBuffer, QIODevice, Qt
import shutil
import fitz
from PIL import Image
from PyQt5.QtGui import QFont, QPalette, QColor

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Conversion and Compression")
        self.setGeometry(100, 100, 400, 400)
        # Set the background color of the main window
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))  # Set the color to red
        self.setPalette(palette)

        self.layout = QVBoxLayout()

        self.label = QLabel("Image Paths:")
        self.layout.addWidget(self.label)

        self.path_text = QTextEdit()
        self.layout.addWidget(self.path_text)

        self.browse_button = QPushButton("Browse Images")
        self.browse_button.clicked.connect(self.browse_images)
        self.layout.addWidget(self.browse_button)
        self.browse_button.setStyleSheet("QPushButton { background-color: #3F00FF; color: white; font-size: 10px; font-weight: bold; font-family: Ubuntu;}")
        self.browse_button.setFixedSize(86, 30)  # Set width = 100, height = 50
        
        self.convert_button = QPushButton("Convert to WebP")
        self.convert_button.clicked.connect(self.convert_to_webp)
        self.layout.addWidget(self.convert_button)
        self.convert_button.setStyleSheet("QPushButton { background-color: #3F00FF; color: white; font-size: 10px; font-weight: bold; font-family: Ubuntu;}")
        self.convert_button.setFixedSize(86, 30)  # Set width = 100, height = 50

        self.compress_webp_button = QPushButton("Compress WebP")
        self.compress_webp_button.clicked.connect(self.compress_webp_images)
        self.layout.addWidget(self.compress_webp_button)
        self.compress_webp_button.setStyleSheet("QPushButton { background-color: #3F00FF; color: white; font-size: 10px; font-weight: bold; font-family: Ubuntu;}")
        self.compress_webp_button.setFixedSize(86, 30)  # Set width = 100, height = 50

        self.setLayout(self.layout)

        self.image_paths = []
        self.output_folder = "webp"
        self.webp_folder_label = QLabel("WebP Folder Path: ")
        self.layout.addWidget(self.webp_folder_label)

        self.file_path = None

        self.btn_open = QPushButton("Open PDF", self)
        self.btn_open.setGeometry(100, 300, 200, 30)
        self.btn_open.clicked.connect(self.open_pdf)
        self.btn_open.setStyleSheet("QPushButton { background-color: #3F00FF; color: white; font-size: 10px; font-weight: bold; font-family: Ubuntu;}")
        self.btn_open.setFixedSize(86, 30)  # Set width = 100, height = 50
        self.btn_open.setGeometry(100, 547, 86, 30)

        self.btn_extract = QPushButton("Extract Images", self)
        self.btn_extract.setGeometry(100, 350, 200, 30)
        self.btn_extract.clicked.connect(self.extract_images)
        self.btn_extract.setEnabled(False)
        self.btn_extract.setStyleSheet("QPushButton { background-color: #3F00FF; color: white; font-size: 10px; font-weight: bold; font-family: Ubuntu;}")
        self.btn_extract.setFixedSize(86, 30)  # Set width = 100, height = 50
        self.btn_extract.setGeometry(190, 547, 86, 30)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_image_paths)
        self.layout.addWidget(self.clear_button)
        self.clear_button.setStyleSheet("QPushButton { background-color: #3F00FF; color: white; font-size: 10px; font-weight: bold; font-family: Ubuntu;}")
        self.clear_button.setFixedSize(86, 30)  # Set width = 100, height = 50
        self.clear_button.setGeometry(90, 547, 86, 30)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.create_menu_bar()

    def create_menu_bar(self):
        menubar = QMenuBar(self)

        # Create "File" menu
        file_menu = menubar.addMenu("File")

        # Add actions to "File" menu
        browse_action = QAction("Browse Images", self)
        browse_action.triggered.connect(self.browse_images)
        file_menu.addAction(browse_action)

        convert_action = QAction("Convert to WebP", self)
        convert_action.triggered.connect(self.convert_to_webp)
        file_menu.addAction(convert_action)

        compress_action = QAction("Compress WebP", self)
        compress_action.triggered.connect(self.compress_webp_images)
        file_menu.addAction(compress_action)

        open_action = QAction("Open PDF", self)
        open_action.triggered.connect(self.open_pdf)
        file_menu.addAction(open_action)

        extract_action = QAction("Extract Images", self)
        extract_action.triggered.connect(self.extract_images)
        extract_action.setEnabled(False)
        file_menu.addAction(extract_action)

        # Create "Edit" menu
        edit_menu = menubar.addMenu("Edit")

        # Add "Clear" action to "Edit" menu
        clear_action = QAction("Clear", self)
        clear_action.triggered.connect(self.clear_image_paths)
        edit_menu.addAction(clear_action)

        self.layout.setMenuBar(menubar)


    def browse_images(self):
        file_dialog = QFileDialog()
        image_paths, _ = file_dialog.getOpenFileNames(
            self, "Open Image files", filter="Image Files (*.jpg *.jpeg)"
        )
        if image_paths:
            self.image_paths = image_paths
            self.display_image_paths()

    def display_image_paths(self):
        self.path_text.clear()
        for path in self.image_paths:
            self.path_text.append(path)

    def convert_to_webp(self):
        if self.image_paths:
            try:
                # Prompt the user to select the output folder
                file_dialog = QFileDialog()
                output_folder = file_dialog.getExistingDirectory(
                    self, "Select Output Folder"
                )
                if output_folder:
                    # Create the output folder if it doesn't exist
                    os.makedirs(output_folder, exist_ok=True)
                    webp_folder_path = os.path.abspath(output_folder)
                    self.webp_folder_label.setText("WebP Folder Path: " + webp_folder_path)

                    total_images = len(self.image_paths)
                    self.progress_bar.setMaximum(total_images)
                    self.progress_bar.setValue(0)

                    for i, image_path in enumerate(self.image_paths):
                        img = Image.open(image_path)

                        # Construct the output file path with a '.webp' extension
                        file_name = os.path.splitext(os.path.basename(image_path))[0]
                        output_path = os.path.join(output_folder, file_name + ".webp")

                        # Convert JPG to WebP
                        img.save(output_path, "WEBP")

                        # Copy the converted WebP file to the original image's folder within the 'webp' folder
                        original_folder = os.path.dirname(image_path)
                        webp_output_path = os.path.join(original_folder, file_name + ".webp")
                        os.makedirs(os.path.dirname(webp_output_path), exist_ok=True)
                        shutil.copy(output_path, webp_output_path)

                        self.progress_bar.setValue(i + 1)

                    QMessageBox.information(
                        self,
                        "Conversion Successful",
                        "Images converted to WebP and stored in the respective folders successfully.",
                    )
            except Exception as e:
                QMessageBox.critical(self, "Conversion Error", str(e))
        else:
            QMessageBox.warning(self, "No Images Selected", "Please select one or more JPG images.")


    def compress_webp_images(self):
        if self.image_paths:
            try:
                # Prompt the user to select the output folder
                file_dialog = QFileDialog()
                output_folder = file_dialog.getExistingDirectory(
                    self, "Select Output Folder"
                )
                if output_folder:
                    total_images = len(self.image_paths)
                    self.progress_bar.setMaximum(total_images)
                    self.progress_bar.setValue(0)

                    for i, image_path in enumerate(self.image_paths):
                        img = Image.open(image_path)

                        # Construct the output file path with a '_compressed.webp' extension
                        file_name = os.path.splitext(os.path.basename(image_path))[0]
                        output_path = os.path.join(output_folder, file_name + "_compressed.webp")

                        self.compress_webp(image_path, output_path, max_size_kb=100)

                        self.progress_bar.setValue(i+1)

                    QMessageBox.information(
                        self,
                        "Compression Successful",
                        "WebP images compressed successfully.",
                    )
            except Exception as e:
                QMessageBox.critical(self, "Compression Error", str(e))
        else:
            QMessageBox.warning(self, "No Images Selected", "Please select one or more WebP images.")


    def compress_webp(self, input_path, output_path, max_size_kb=100, quality=80):
        image = Image.open(input_path)

        # Compress the image with the specified quality
        image.save(output_path, "webp", quality=quality)

        # Loop until the compressed image size is less than the maximum size limit
        while os.path.getsize(output_path) > max_size_kb * 1024 and quality > 10:
            quality -= 10
            image.save(output_path, "webp", quality=quality)

        # Check the final file size
        file_size = os.path.getsize(output_path)
        if file_size <= max_size_kb * 1024:
            print(f"Image {output_path} compressed successfully. File size: {file_size} bytes.")
        else:
            print(f"Image {output_path} could not be compressed within the size limit.")

    def open_pdf(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("PDF Files (*.pdf)")

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            self.file_path = selected_files[0]
            self.btn_extract.setEnabled(True)
    
    def clear_image_paths(self):
        self.image_paths = []
        self.path_text.clear()
    
    def extract_images(self):
        if not self.file_path:
            QMessageBox.critical(self, "Error", "No PDF file selected.")
            return

        try:
            doc = fitz.open(self.file_path)
            pdf_folder = os.path.dirname(self.file_path)
            images_folder = os.path.splitext(self.file_path)[0] + "_images"
            os.makedirs(images_folder, exist_ok=True)

            total_images = 0
            for i in range(len(doc)):
                for img in doc.get_page_images(i):
                    total_images += 1

            self.progress_bar.setMaximum(total_images)
            self.progress_bar.setValue(0)

            image_count = 0
            for i in range(len(doc)):
                for img in doc.get_page_images(i):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_data = base_image["image"]
                    image_format = base_image["ext"]

                    image_path = os.path.join(images_folder, f"image_{i}.{image_format}")
                    with open(image_path, "wb") as f:
                        f.write(image_data)

                    # Convert the image to JPG format
                    jpg_path = os.path.join(images_folder, f"image_{i}.jpg")
                    with Image.open(image_path) as img:
                        img.save(jpg_path, "JPEG")

                    # Optionally, remove the original image file
                    os.remove(image_path)

                    image_count += 1
                    self.progress_bar.setValue(image_count)

            QMessageBox.information(self, "Success", "Images extracted and converted successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()