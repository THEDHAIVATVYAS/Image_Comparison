import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox, QProgressBar, QSlider
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PIL import Image, ImageEnhance

class WatermarkThread(QThread):
    progressChanged = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, images, watermark_image, output_folder, opacity):
        super().__init__()
        self.images = images
        self.watermark_image = watermark_image
        self.output_folder = output_folder
        self.opacity = opacity

    def run(self):
        total_images = len(self.images)
        for i, image_path in enumerate(self.images, 1):
            self.add_watermark_to_image(image_path)
            progress = int((i / total_images) * 100)
            self.progressChanged.emit(progress)
        self.finished.emit()

    def add_watermark_to_image(self, image_path):
        image = Image.open(image_path)
        watermark = Image.open(self.watermark_image)
        watermark = watermark.convert("RGBA")

        if image.mode != "RGBA":
            image = image.convert("RGBA")

        image_width, image_height = image.size
        watermark_width, watermark_height = watermark.size

        # Calculate the position to center the watermark
        x_position = (image_width - watermark_width) // 2
        y_position = (image_height - watermark_height) // 2

        # Apply opacity to the watermark
        watermark = self.apply_opacity(watermark, self.opacity)

        transparent = Image.new("RGBA", image.size, (0, 0, 0, 0))
        transparent.paste(image, (0, 0))
        transparent.paste(watermark, (x_position, y_position), mask=watermark)

        # Convert to RGB mode before saving
        rgb_image = transparent.convert("RGB")

        output_path = os.path.join(self.output_folder, f"watermarked_{os.path.basename(image_path)}")
        rgb_image.save(output_path)
        image.close()
        watermark.close()
        transparent.close()
        rgb_image.close()

        # Emit the progress after saving the image
        self.progressChanged.emit(0)

    def apply_opacity(self, image, opacity):
        alpha = image.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        image.putalpha(alpha)
        return image

class ImageWatermarkerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Watermarker')
        self.setGeometry(100, 100, 800, 600)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(400, 400)

        self.load_button = QPushButton('Load Image', self)
        self.load_button.clicked.connect(self.load_image)

        self.watermark_button = QPushButton('Load Watermark', self)
        self.watermark_button.clicked.connect(self.load_watermark)

        self.start_button = QPushButton('Start Watermarking', self)
        self.start_button.clicked.connect(self.start_watermarking)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)

        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(100)
        self.opacity_slider.valueChanged.connect(self.update_opacity_label)

        self.opacity_label = QLabel("Opacity: 100%")

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.load_button)
        layout.addWidget(self.watermark_button)
        layout.addWidget(self.start_button)
        layout.addWidget(self.opacity_slider)
        layout.addWidget(self.opacity_label)
        layout.addWidget(self.progress_bar)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.image_path = ''
        self.watermark_path = ''
        self.watermark_thread = None

    def load_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)", options=options)
        if file_name:
            self.image_path = file_name
            self.display_image()

    def load_watermark(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Watermark Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)", options=options)
        if file_name:
            self.watermark_path = file_name

    def display_image(self):
        pixmap = QPixmap(self.image_path)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def update_opacity_label(self, value):
        self.opacity_label.setText(f"Opacity: {value}%")

    def start_watermarking(self):
        if not self.watermark_path:
            QMessageBox.warning(self, "Error", "Please select a watermark image.")
            return

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder", "", options=options)

        if folder:
            images = [self.image_path]
            opacity = self.opacity_slider.value() / 100.0
            self.watermark_thread = WatermarkThread(images, self.watermark_path, folder, opacity)
            self.watermark_thread.progressChanged.connect(self.update_progress)
            self.watermark_thread.finished.connect(self.watermarking_finished)
            self.watermark_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def watermarking_finished(self):
        QMessageBox.information(self, "Watermarking Complete", "Watermarking of images is complete!")
        self.progress_bar.setValue(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageWatermarkerApp()
    window.show()
    sys.exit(app.exec_())
