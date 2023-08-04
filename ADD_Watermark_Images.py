import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt, QRunnable, QThreadPool, pyqtSignal, pyqtSlot
from PIL import Image


class WatermarkApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Watermark Application")
        self.setGeometry(100, 100, 500, 300)

        self.watermark_image_path = None
        self.images_directory = None

        self.central_widget = QLabel(self)
        self.central_widget.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.central_widget)

        self.watermark_label = QLabel("Watermark Image:", self)
        self.watermark_label.setGeometry(20, 20, 200, 30)

        self.watermark_button = QPushButton("Select Watermark Image", self)
        self.watermark_button.setGeometry(220, 20, 200, 30)
        self.watermark_button.clicked.connect(self.select_watermark)

        self.images_label = QLabel("Select Images Directory:", self)
        self.images_label.setGeometry(20, 60, 200, 30)

        self.images_button = QPushButton("Select Images Directory", self)
        self.images_button.setGeometry(220, 60, 200, 30)
        self.images_button.clicked.connect(self.select_images_directory)

        self.process_button = QPushButton("Process Images", self)
        self.process_button.setGeometry(180, 100, 140, 30)
        self.process_button.clicked.connect(self.process_images)

        self.threadpool = QThreadPool()

    def select_watermark(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Watermark Image", "", "Image Files (*.png *.jpg *.jpeg);;All Files (*)", options=options
        )
        if file_path:
            self.watermark_image_path = file_path
            self.watermark_image = QPixmap(file_path)
            self.central_widget.setPixmap(self.watermark_image)

    def select_images_directory(self):
        options = QFileDialog.Options()
        dir_path = QFileDialog.getExistingDirectory(self, "Select Images Directory", "", options=options)
        if dir_path:
            self.images_directory = dir_path

    def add_watermark_to_image(self, image_path):
        try:
            image = QImage(image_path)
            watermark = self.watermark_image.toImage()
            painter = QPainter(image)
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            painter.drawImage(image.width() - watermark.width(), image.height() - watermark.height(), watermark)
            painter.end()

            output_directory = os.path.join(self.images_directory, "watermarked_images")
            os.makedirs(output_directory, exist_ok=True)
            image.save(os.path.join(output_directory, os.path.basename(image_path)))

        except Exception as e:
            print(f"Error processing {image_path}: {e}")

    def process_images(self):
        if not self.watermark_image_path or not self.images_directory:
            QMessageBox.critical(self, "Error", "Please select both watermark image and images directory.")
            return

        images_list = [os.path.join(self.images_directory, filename) for filename in os.listdir(self.images_directory) if filename.lower().endswith((".png", ".jpg", ".jpeg"))]

        if not images_list:
            QMessageBox.critical(self, "Error", "No valid images found in the selected directory.")
            return

        for image_path in images_list:
            runnable = ImageProcessingRunnable(image_path, self.watermark_image_path)
            runnable.signals.finished.connect(self.image_processing_finished)
            self.threadpool.start(runnable)

    @pyqtSlot()
    def image_processing_finished(self):
        pass  # You can implement any actions after the image processing is completed


class ImageProcessingRunnable(QRunnable):
    def __init__(self, image_path, watermark_image_path):
        super().__init__()
        self.image_path = image_path
        self.watermark_image_path = watermark_image_path
        self.signals = WorkerSignals()

    def run(self):
        self.process_image()

    def process_image(self):
        try:
            watermark = Image.open(self.watermark_image_path).convert("RGBA")
            image = Image.open(self.image_path).convert("RGBA")
            image_width, image_height = image.size
            watermark_width, watermark_height = watermark.size

            # Calculate the position to center the watermark on the image
            x = (image_width - watermark_width) // 2
            y = (image_height - watermark_height) // 2

            watermarked = Image.alpha_composite(image, watermark.resize((image_width, image_height)))

            output_directory = os.path.join(os.path.dirname(self.image_path), "watermarked_images")
            os.makedirs(output_directory, exist_ok=True)

            # Save the watermarked image
            watermarked.save(os.path.join(output_directory, os.path.basename(self.image_path)))

        except Exception as e:
            print(f"Error processing {self.image_path}: {e}")

        finally:
            self.signals.finished.emit()


class WorkerSignals:
    finished = pyqtSignal()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WatermarkApp()
    window.show()
    sys.exit(app.exec_())
