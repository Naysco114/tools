# -*- coding: utf-8 -*-

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QTextCursor, QDesktopServices
from PyQt6.QtCore import Qt, QUrl


class AboutPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        label_title = QLabel("关于本程序")
        label_title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(label_title)

        label_description = QLabel(
            "这个程序是一个示例应用，用于演示如何使用 PyQt6 创建一个简单的多页面应用。<br>"
            "它包含了一个主窗口和多个子页面，可以通过菜单或按钮进行导航。<br>"
            "您可以根据自己的需求进行修改和扩展，创建出适合您应用的多页面界面。<br>"
            "更多信息，请访问 <a href='https://github.com/Naysco114/tools'>https://github.com/Naysco114/tools</a>"
        )
        label_description.setTextFormat(Qt.TextFormat.RichText)
        label_description.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        label_description.setOpenExternalLinks(True)
        label_description.setWordWrap(True)
        layout.addWidget(label_description)

        self.setLayout(layout)
