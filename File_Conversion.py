import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap
from pdf2docx import Converter


class PDFToDocConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PDF to DOC Converter')
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.upload_button = QPushButton('Upload PDF')
        self.upload_button.clicked.connect(self.upload_pdf)
        self.layout.addWidget(self.upload_button)

        self.pdf_label = QLabel()
        self.layout.addWidget(self.pdf_label)

        self.convert_button = QPushButton('Convert to DOC')
        self.convert_button.clicked.connect(self.convert_to_doc)
        self.convert_button.setEnabled(False)
        self.layout.addWidget(self.convert_button)

        self.central_widget.setLayout(self.layout)

    def upload_pdf(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if file_name:
            self.pdf_path = file_name
            self.display_pdf()

    def display_pdf(self):
        pixmap = QPixmap('pdf_icon.png')  # Replace 'pdf_icon.png' with an image of your choice
        self.pdf_label.setPixmap(pixmap.scaledToHeight(100))
        self.convert_button.setEnabled(True)

    def convert_to_doc(self):
        output_file = self.pdf_path.replace('.pdf', '.docx')
        try:
            with Converter(self.pdf_path) as converter:
                converter.convert(output_file)
            self.show_conversion_success_message(output_file)
        except Exception as e:
            error_message = f"Error occurred during conversion:\n{str(e)}"
            self.show_conversion_error_message(error_message)

    def show_conversion_error_message(self, error_message):
        self.convert_button.setEnabled(False)
        self.pdf_label.clear()
        self.pdf_label.setText(error_message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PDFToDocConverter()
    window.show()
    sys.exit(app.exec_())

