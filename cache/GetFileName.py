import os
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QListWidget, QLabel, QLineEdit, QErrorMessage
import subprocess
import locale

class Stream:
    """Redirects console output to text widget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        try:
            self.text_widget.append(text.decode(locale.getpreferredencoding()))
        except UnicodeDecodeError:
            # Handle decoding error
            error_message = QErrorMessage()
            error_message.showMessage("Error decoding output")
            error_message.exec()

class GetFileNameGUI(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.current_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../tools")
        self.get_subdirectories()

        self.label = QLabel("选择的目录:")
        self.directory_label = QLabel(self.current_directory)

        self.subdirectories_listbox = QListWidget()
        self.files_listbox = QListWidget()

        self.display_current_directory()

        self.switch_button = QPushButton("切换目录")
        self.parent_button = QPushButton("返回上一级")
        self.open_terminal_button = QPushButton("打开终端")
        self.clear_output_button = QPushButton("清空输出")
        self.quit_button = QPushButton("退出")

        self.command_line = QLineEdit()
        self.execute_button = QPushButton("执行")

        self.init_ui()

        # Custom output stream.
        self.stream = Stream(self.output_text)
        sys.stdout = self.stream

    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        sys.stdout = sys.__stdout__
        super().closeEvent(event)

    def init_ui(self):
        """Creates UI window on launch."""
        layout = QVBoxLayout()

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.switch_button)
        button_layout.addWidget(self.parent_button)
        button_layout.addWidget(self.open_terminal_button)
        button_layout.addWidget(self.clear_output_button)
        button_layout.addWidget(self.quit_button)

        # Directory layout
        directory_layout = QHBoxLayout()
        directory_layout.addWidget(self.label)
        directory_layout.addWidget(self.directory_label)

        # List layout
        list_layout = QHBoxLayout()
        list_layout.addWidget(self.subdirectories_listbox)
        list_layout.addWidget(self.files_listbox)

        layout.addLayout(button_layout)
        layout.addLayout(directory_layout)
        layout.addLayout(list_layout)

        self.output_text = QTextEdit()
        layout.addWidget(self.output_text)

        # Command line layout
        command_line_layout = QHBoxLayout()
        command_line_layout.addWidget(self.command_line)
        command_line_layout.addWidget(self.execute_button)

        layout.addLayout(command_line_layout)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.switch_button.clicked.connect(self.switch_directory)
        self.parent_button.clicked.connect(self.parent_directory)
        self.open_terminal_button.clicked.connect(self.open_terminal)
        self.clear_output_button.clicked.connect(self.clear_output)
        self.quit_button.clicked.connect(self.close)
        self.execute_button.clicked.connect(self.execute_command)

    def get_subdirectories(self):
        self.subdirectories = [name for name in os.listdir(self.current_directory)
                               if os.path.isdir(os.path.join(self.current_directory, name))]

    def list_files(self):
        return [name for name in os.listdir(self.current_directory)
                if os.path.isfile(os.path.join(self.current_directory, name))]

    def display_current_directory(self):
        self.directory_label.setText("选择的目录: " + self.current_directory)

        self.subdirectories_listbox.clear()
        for subdir in self.subdirectories:
            self.subdirectories_listbox.addItem(subdir)

        self.files_listbox.clear()
        for file in self.list_files():
            self.files_listbox.addItem(file)

    def switch_directory(self):
        try:
            choice = self.subdirectories_listbox.currentRow()
            if choice != -1:
                subdir_name = self.subdirectories[choice]
                self.current_directory = os.path.join(self.current_directory, subdir_name)
                self.get_subdirectories()
                self.display_current_directory()
                print("切换成功")
            else:
                print("请选择一个目录")
        except Exception as e:
            print("切换目录时出错:", e)

    def parent_directory(self):
        try:
            self.current_directory = os.path.dirname(self.current_directory)
            self.get_subdirectories()
            self.display_current_directory()
            print("切换成功")
        except Exception as e:
            print("返回上一级时出错:", e)

    def open_terminal(self):
        if os.environ.get("DISPLAY"):
            print("当前运行在GUI环境中，打开GUI窗口")
        else:
            print("当前运行在终端环境中，执行终端命令")

    def clear_output(self):
        self.output_text.clear()

    def execute_command(self):
        command = self.command_line.text().strip()
        if command:
            try:
                completed_process = subprocess.run(command, shell=True, check=True, text=False, capture_output=True)
                output = completed_process.stdout
                error = completed_process.stderr
                if output:
                    print(output.decode(locale.getpreferredencoding()))
                if error:
                    print(error.decode(locale.getpreferredencoding()))
            except subprocess.CalledProcessError as e:
                print(f"执行命令时出错: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GetFileNameGUI()
    window.show()
    sys.exit(app.exec())
