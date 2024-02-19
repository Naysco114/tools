# -*- coding: utf-8 -*-
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView


class TwoWindow(QWidget):
    """Second application window."""

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Add URL input field and execute button
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        url_layout.addWidget(self.url_input)
        self.execute_button = QPushButton("执行")
        url_layout.addWidget(self.execute_button)
        layout.addLayout(url_layout)

        # Add browser widget
        self.browser = QWebEngineView()
        layout.addWidget(self.browser)

        self.setLayout(layout)

        self.execute_button.clicked.connect(self.load_url)

    def load_url(self):
        url = self.url_input.text()
        if not (url.startswith("http://") or url.startswith("https://")):
            url = "http://" + url
        self.browser.load(QUrl(url))
