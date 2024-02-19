# -*- coding: utf-8 -*-
import os
import platform
import subprocess
import sys

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QPushButton, QLineEdit, QTextEdit
from PyQt6.QtCore import pyqtSignal
from funs.stream import Stream
from win32com.client import Dispatch

from funs.terminal_widget import TerminalWidget


class GetFileNameGUI(QWidget):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.drives = None
        self.current_path = os.getcwd()
        self.get_drives()

        self.label = QLabel("当前目录: " + self.current_path)
        self.directory_label = QLabel("")

        self.drive_listbox = QListWidget()
        self.files_listbox = QListWidget()

        self.display_current_drive()

        self.refresh_button = QPushButton("刷新")
        self.parent_button = QPushButton("返回上一级")
        self.clear_output_button = QPushButton("清空输出")
        self.change_dir_button = QPushButton("切换目录")
        self.change_drive_button = QPushButton("切换盘")
        self.get_system_info_button = QPushButton("获取系统信息")

        self.command_line = QLineEdit()
        self.execute_button = QPushButton("执行")

        self.output_text = QTextEdit()

        self.init_ui()

        self.stream = Stream(self.output_text)
        sys.stdout = self.stream

    def init_ui(self):
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.parent_button)
        button_layout.addWidget(self.clear_output_button)
        button_layout.addWidget(self.change_dir_button)
        button_layout.addWidget(self.change_drive_button)
        button_layout.addWidget(self.get_system_info_button)  # Make sure this line is correct
        button_layout.addWidget(self.execute_button)  # Add this line to include the execute button

        directory_layout = QHBoxLayout()
        directory_layout.addWidget(self.label)
        directory_layout.addWidget(self.directory_label)

        list_layout = QHBoxLayout()
        list_layout.addWidget(self.drive_listbox)
        list_layout.addWidget(self.files_listbox)

        layout.addLayout(button_layout)
        layout.addLayout(directory_layout)
        layout.addLayout(list_layout)

        layout.addWidget(self.output_text)

        terminal_widget = TerminalWidget()
        layout.addWidget(terminal_widget)

        self.setLayout(layout)

        self.refresh_button.clicked.connect(self.refresh)
        self.parent_button.clicked.connect(self.parent_directory)
        self.clear_output_button.clicked.connect(self.clear_output)
        self.change_dir_button.clicked.connect(self.change_directory)
        self.change_drive_button.clicked.connect(self.change_drive)
        self.execute_button.clicked.connect(self.execute_selected_file)
        self.get_system_info_button.clicked.connect(self.get_system_info)

    def execute_selected_file(self):
        selected_items = self.files_listbox.selectedItems()  # Corrected line
        if selected_items:
            selected_item_text = selected_items[0].text()
            full_path = os.path.join(self.current_path, selected_item_text)
            self.execute_file(full_path)

    def execute_file(self, filename):
        if os.path.isfile(filename):
            if filename.endswith(".py"):
                subprocess.Popen(["python", filename])
            elif filename.endswith(".jar"):
                subprocess.Popen(["java", "-jar", filename])
            elif filename.endswith(".exe"):
                subprocess.Popen([filename])
            elif filename.endswith(".lnk"):  # Handle shortcut files
                # Resolve the target of the shortcut
                shell = Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(filename)
                target_path = shortcut.TargetPath

                # Execute the resolved target
                os.startfile(target_path)
            elif filename.endswith(".txt"):  # Handle text files
                subprocess.Popen(["notepad", filename])

    def get_drives(self):
        if platform.system() == "Windows":
            self.drives = [f"{chr(drive)}:" for drive in range(ord("A"), ord("Z") + 1)
                           if os.path.exists(f"{chr(drive)}:")]
        else:
            self.drives = ["/"]

    def display_current_drive(self):
        self.drive_listbox.clear()
        for drive in self.drives:
            self.drive_listbox.addItem(drive)

        self.directory_label.setText("当前目录: " + self.current_path)

        self.files_listbox.clear()
        for file in os.listdir(self.current_path):
            self.files_listbox.addItem(file)

    def refresh(self):
        self.display_current_drive()
        self.label.setText("当前目录: " + self.current_path)

    def parent_directory(self):
        try:
            self.current_path = os.path.dirname(self.current_path)
            self.refresh()
            print("返回上一级成功")
        except Exception as e:
            print("返回上一级时出错:", e)

    def get_system_info(self):
        if platform.system() == "Windows":
            try:
                completed_process = subprocess.run(["Systeminfo"], capture_output=True, text=True)
                output = completed_process.stdout
                self.output_text.append(output)
            except subprocess.CalledProcessError as e:
                self.output_text.append(f"执行命令时出错: {e}")
        elif platform.system() == "Linux":
            try:
                completed_process = subprocess.run(["uname", "-a"], capture_output=True, text=True)
                output = completed_process.stdout
                self.output_text.append(output)
            except subprocess.CalledProcessError as e:
                self.output_text.append(f"执行命令时出错: {e}")

    def clear_output(self):
        self.output_text.clear()

    def execute_command(self):
        command = self.command_line.text().strip()
        if command:
            try:
                subprocess.run(command.split(), check=True)
            except subprocess.CalledProcessError as e:
                self.output_text.append(f"执行命令时出错: {e}")

    def change_directory(self):
        try:
            selected_item = self.files_listbox.currentItem()
            if selected_item:
                new_dir = selected_item.text()
                new_path = os.path.join(self.current_path, new_dir)
                if os.path.isdir(new_path):
                    self.current_path = new_path
                    self.refresh()
                    print("切换目录成功")
                else:
                    print("所选项目不是目录")
            else:
                print("未选择目录")
        except Exception as e:
            print("切换目录时出错:", e)

    def change_drive(self):
        try:
            selected_item = self.drive_listbox.currentItem()
            if selected_item:
                drive = selected_item.text()
                if platform.system() == "Windows":
                    drive += "\\"
                self.current_path = drive
                self.refresh()
                print("切换盘符成功")
            else:
                print("未选择盘符")
        except Exception as e:
            print("切换盘符时出错:", e)
