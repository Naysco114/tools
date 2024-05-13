# -*- coding: utf-8 -*-
import hashlib
from urllib.parse import quote, unquote
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit

class CryptographyTools(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("密码学工具箱")
        layout = QVBoxLayout()

        md5_button = QPushButton("MD5")
        md5_button.clicked.connect(self.hash_md5)
        layout.addWidget(md5_button)

        sha256_button = QPushButton("SHA256")
        sha256_button.clicked.connect(self.hash_sha256)
        layout.addWidget(sha256_button)

        url_encode_button = QPushButton("URL 编码")
        url_encode_button.clicked.connect(self.url_encode)
        layout.addWidget(url_encode_button)

        url_decode_button = QPushButton("URL 解码")
        url_decode_button.clicked.connect(self.url_decode)
        layout.addWidget(url_decode_button)

        self.input_text = QTextEdit()
        layout.addWidget(self.input_text)

        self.output_text = QTextEdit()
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def hash_md5(self):
        text = self.input_text.toPlainText()
        hash_result = hashlib.md5(text.encode()).hexdigest()
        self.output_text.setPlainText(hash_result)

    def hash_sha256(self):
        text = self.input_text.toPlainText()
        hash_result = hashlib.sha256(text.encode()).hexdigest()
        self.output_text.setPlainText(hash_result)

    def url_encode(self):
        text = self.input_text.toPlainText()
        encoded_text = quote(text)
        self.output_text.setPlainText(encoded_text)

    def url_decode(self):
        encoded_text = self.input_text.toPlainText()
        decoded_text = unquote(encoded_text)
        self.output_text.setPlainText(decoded_text)
