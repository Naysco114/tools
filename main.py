import os
import sys
import platform
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QListWidget, QLabel, QPushButton, QLineEdit
)
from PyQt6.QtCore import pyqtSignal, QIODevice, pyqtSlot
from PyQt6.QtGui import QTextCursor, QAction
from PyQt6.QtCore import QProcess


class Stream:
    """Redirects console output to text widget."""

    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.append(text)

    def flush(self):
        pass  # No-op for flush


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
            self.process.start("cmd", [], QIODevice.OpenModeFlag.ReadWrite)
        elif sys.platform.startswith("linux"):
            self.process.start("bash", [], QIODevice.OpenModeFlag.ReadWrite)

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


class GetFileNameGUI(QWidget):
    """Main application window."""

    def __init__(self):
        super().__init__()

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
        button_layout.addWidget(self.get_system_info_button)  # 添加获取系统信息按钮

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

        self.execute_button.clicked.connect(self.execute_command)
        self.get_system_info_button.clicked.connect(self.get_system_info)  # 连接获取系统信息功能

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


class TwoWindow(QWidget):
    """Second application window."""

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        label = QLabel("这是功能2页面")
        layout.addWidget(label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.get_file_name_gui = GetFileNameGUI()
        self.two_window = TwoWindow()
        self.setCentralWidget(self.get_file_name_gui)
        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&文件")

        exit_action = QAction("&退出", self)
        exit_action.triggered.connect(self.close)  # 退出窗口
        file_menu.addAction(exit_action)

        function_menu = menu_bar.addMenu("&功能")
        function_one_action = QAction("功能1", self)
        function_one_action.triggered.connect(self.show_get_file_name_gui)
        function_menu.addAction(function_one_action)

        function_two_action = QAction("功能2", self)
        function_two_action.triggered.connect(self.show_two_window)
        function_menu.addAction(function_two_action)

        function_two_menu = menu_bar.addMenu("&系统功能")
        open_terminal_action = QAction("&打开终端", self)
        open_terminal_action.triggered.connect(self.open_terminal)
        function_two_menu.addAction(open_terminal_action)

    def show_get_file_name_gui(self):
        self.get_file_name_gui = GetFileNameGUI()  # Create a new instance
        self.setCentralWidget(self.get_file_name_gui)

    def show_two_window(self):
        self.two_window = TwoWindow()
        self.setCentralWidget(self.two_window)

    def open_terminal(self):
        current_path = self.get_file_name_gui.current_path  # 获取GetFileNameGUI实例的current_path属性
        if platform.system() == "Windows":
            os.system(f"start cmd /K cd {current_path}")
            self.get_file_name_gui.output_text.append("成功打开终端")
        elif platform.system() == "Linux":
            os.system(f"x-terminal-emulator --working-directory={current_path}")
            self.get_file_name_gui.output_text.append("成功打开终端")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
