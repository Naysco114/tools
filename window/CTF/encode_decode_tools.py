# -*- coding: utf-8 -*-
import base64
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit


class EncodeDecodeTools(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("编码解码工具箱")
        layout = QVBoxLayout()

        encode_button = QPushButton("编码")
        encode_button.clicked.connect(self.encode_text)
        layout.addWidget(encode_button)

        decode_button = QPushButton("解码")
        decode_button.clicked.connect(self.decode_text)
        layout.addWidget(decode_button)

        self.input_text = QTextEdit()
        layout.addWidget(self.input_text)

        self.output_text = QTextEdit()
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def encode_text(self):
        text = self.input_text.toPlainText()
        encoded_text = base64.b64encode(text.encode()).decode()
        self.output_text.setPlainText(encoded_text)

    def decode_text(self):
        encoded_text = self.input_text.toPlainText()
        decoded_text = base64.b64decode(encoded_text.encode()).decode()
        self.output_text.setPlainText(decoded_text)
