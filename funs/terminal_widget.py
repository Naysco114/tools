# -*- coding: utf-8 -*-
import sys

from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QLineEdit
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QProcess


# , QTextCursor, QProcess
class TerminalWidget(QWidget):
    command_executed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.command_line = QLineEdit()
        self.execute_button = QPushButton("执行")

        layout = QVBoxLayout()
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        layout.addWidget(self.output_text)

        terminal_layout = QVBoxLayout()
        terminal_layout.addWidget(self.command_line)
        terminal_layout.addWidget(self.execute_button)

        layout.addLayout(terminal_layout)
        self.setLayout(layout)

        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.on_ready_read_standard_output)
        self.process.readyReadStandardError.connect(self.on_ready_read_standard_error)

        self.start_terminal()
        self.execute_button.clicked.connect(self.execute_command)

    def start_terminal(self):
        if sys.platform == "win32":
            self.process.start("cmd", [])
        elif sys.platform.startswith("linux"):
            self.process.start("bash", [])

    def execute_command(self):
        command = self.command_line.text().strip()
        if command:
            if sys.platform == "win32":
                self.process.write(f"{command}\r\n".encode())
            elif sys.platform.startswith("linux"):
                self.process.write(f"{command}\n".encode())

    @pyqtSlot()
    def on_ready_read_standard_output(self):
        data = self.process.readAllStandardOutput().data()
        try:
            text = data.decode('gbk')
        except UnicodeDecodeError:
            text = data.decode('utf-8', errors='ignore')
        self.append_output(text)

    @pyqtSlot()
    def on_ready_read_standard_error(self):
        data = self.process.readAllStandardError().data()
        try:
            text = data.decode('gbk')
        except UnicodeDecodeError:
            text = data.decode('utf-8', errors='ignore')
        self.append_output(text, error=True)

    def append_output(self, text, error=False):
        cursor = self.output_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        if error:
            cursor.insertHtml(f"<font color='red'>{text}</font>")
        else:
            cursor.insertText(text)
        self.output_text.setTextCursor(cursor)
