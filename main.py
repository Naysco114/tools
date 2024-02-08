import platform
import os
import subprocess
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem, QLineEdit, QTextEdit, QLabel,
    QMainWindow, QApplication, QFileDialog
)
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QProcess, QIODevice
from PyQt6.QtGui import QTextCursor, QAction


class TerminalWidget(QWidget):
    def __init__(self, tool_dir, current_dir=None):
        super().__init__()

        self.tool_dir = tool_dir
        self.current_dir = current_dir

        self.command_line = QLineEdit()
        self.execute_button = QPushButton("执行")
        self.switch_drive_button = QPushButton("切换盘")
        # 添加与功能1页面相同的按钮
        self.switch_button = QPushButton("切换文件夹")
        self.open_button = QPushButton("打开当前文件夹")
        self.back_button = QPushButton("返回上一级")
        self.execute_file_button = QPushButton("执行选中文件")

        self.files_list_label = QLabel("当前文件夹:")
        self.current_folder_label = QLabel()

        self.list_widget = QListWidget()

        self.output_text = QTextEdit()

        self.process = QProcess()
        self.process.readyReadStandardOutput.connect(self.on_ready_read_standard_output)
        self.process.readyReadStandardError.connect(self.on_ready_read_standard_error)

        self.current_dir = current_dir
        self.start_terminal()

        self.init_ui()
        self.bind_buttons()

        self.update_list_widget()

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

    def switch_drive(self):
        if platform.system() == "Windows":
            drive = QFileDialog.getExistingDirectory(self, "选择驱动器", "C:/")
            if drive:
                os.chdir(drive)
                self.current_folder_label.setText(drive)
                self.current_dir = drive  # 更新当前目录
                self.update_list_widget()
                print("切换盘符成功")
            else:
                print("未选择盘符")
        else:
            print("非Windows系统，无法切换盘符")

    def update_list_widget(self):
        self.list_widget.clear()
        self.current_dir = os.getcwd() if self.current_dir is None else self.current_dir  # 设置 current_dir
        os.chdir(self.current_dir)
        self.start_terminal()  # 在更新列表小部件时启动终端
        for item in os.listdir("."):
            full_path = os.path.join(self.current_dir, item)
            if os.path.isdir(full_path):
                self.add_list_item(item + "/")
            else:
                self.add_list_item(item)

    def add_list_item(self, name):
        item = QListWidgetItem(name)
        item.setFlags(
            item.flags() | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
        self.list_widget.addItem(item)

    def go_to_directory(self, dirname):
        if os.path.isdir(dirname):  # 检查是否是一个目录
            self.current_dir = dirname
            self.update_list_widget()
        else:
            return f"{dirname} 不是一个有效的目录"

    def go_back(self):
        if self.current_dir != self.tool_dir:
            self.current_dir = os.path.dirname(self.current_dir)
            self.update_list_widget()

    def open_current_directory(self):
        subprocess.Popen(["explorer", self.current_dir])
        self.update_list_widget()

    def switch_to_selected_folder(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            selected_item_text = selected_items[0].text()
            full_path = os.path.join(self.current_dir, selected_item_text.rstrip("/"))
            return full_path  # 返回新的当前文件夹路径

    def execute_selected_file(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            selected_item_text = selected_items[0].text()
            full_path = os.path.join(self.current_dir, selected_item_text)
            self.execute_file(full_path)

    def execute_file(self, filename):
        if os.path.isfile(filename):
            if filename.endswith(".py"):
                subprocess.Popen(["python", filename])
            elif filename.endswith(".jar"):
                subprocess.Popen(["java", "-jar", filename])
            elif filename.endswith(".exe"):
                subprocess.Popen([filename])

    def init_ui(self):
        layout = QVBoxLayout()

        # 添加顶部按钮布局
        top_button_layout = QHBoxLayout()
        top_button_layout.addWidget(self.switch_drive_button)
        top_button_layout.addWidget(self.switch_button)  # 新添加的按钮
        top_button_layout.addWidget(self.open_button)  # 新添加的按钮
        top_button_layout.addWidget(self.back_button)  # 新添加的按钮
        top_button_layout.addWidget(self.execute_file_button)  # 新添加的按钮
        top_button_layout.addStretch(1)
        layout.addLayout(top_button_layout)

        # 添加命令行输入框和执行按钮
        layout.addWidget(self.command_line)
        layout.addWidget(self.execute_button)

        # 添加当前文件夹标签和文件列表标签
        layout.addWidget(self.files_list_label)
        layout.addWidget(self.current_folder_label)

        # 添加文件列表
        layout.addWidget(self.list_widget)

        # 添加输出文本框
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def bind_buttons(self):
        self.execute_button.clicked.connect(self.execute_command)
        self.switch_drive_button.clicked.connect(self.switch_drive)
        self.switch_button.clicked.connect(self.switch_to_selected_folder_and_refresh)
        self.open_button.clicked.connect(self.open_current_directory_and_refresh)
        self.back_button.clicked.connect(self.go_back_and_refresh)
        self.execute_file_button.clicked.connect(self.execute_selected_file_and_refresh)

    def switch_to_selected_folder_and_refresh(self):
        new_dir = self.switch_to_selected_folder()
        if new_dir:
            self.current_dir = new_dir  # 更新当前文件夹路径
            self.update_current_folder_label()  # 更新当前文件夹标签
            self.update_list_widget()

    def open_current_directory_and_refresh(self):
        self.open_current_directory()
        self.update_list_widget()

    def go_back_and_refresh(self):
        self.go_back()
        self.update_list_widget()
        self.update_current_folder_label()

    def execute_selected_file_and_refresh(self):
        self.execute_selected_file()
        self.update_list_widget()

    def update_current_folder_label(self):  # 修正此方法名
        self.current_folder_label.setText(self.current_dir)  # 更新当前文件夹标签


class Functionality(QWidget):
    def __init__(self, tool_dir):
        super().__init__()
        self.tool_dir = tool_dir
        self.current_dir = self.tool_dir  # 使用传递的当前目录作为初始工具目录
        print("当前目录:", self.current_dir)  # 打印当前目录
        self.setup_ui()

    def setup_ui(self):
        self.layout = QVBoxLayout(self)

        # 添加当前文件夹标签
        self.files_list_label = QLabel("当前文件夹:")
        self.current_folder_label = QLabel()  # 添加用于显示当前文件夹的标签
        self.current_folder_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.layout.addWidget(self.files_list_label)
        self.layout.addWidget(self.current_folder_label)

        # 添加按钮布局
        button_layout = QHBoxLayout()
        self.layout.addLayout(button_layout)

        self.switch_button = QPushButton("切换文件夹")
        self.open_button = QPushButton("打开当前文件夹")
        self.back_button = QPushButton("返回上一级")

        button_layout.addWidget(self.switch_button)
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.back_button)

        self.list_widget = QListWidget()
        self.layout.addWidget(self.list_widget)

        self.update_list_widget()
        self.update_current_folder_label()  # 更新当前文件夹标签

        # 绑定按钮点击事件
        self.switch_button.clicked.connect(self.switch_to_selected_folder_and_refresh)
        self.open_button.clicked.connect(self.open_current_directory_and_refresh)
        self.back_button.clicked.connect(self.go_back_and_refresh)

    def update_current_folder_label(self):
        self.current_folder_label.setText(self.current_dir)

    def update_list_widget(self):
        if self.current_dir and os.path.isdir(self.current_dir):
            self.list_widget.clear()
            os.chdir(self.current_dir)
            for item in os.listdir("."):
                full_path = os.path.join(self.current_dir, item)
                if os.path.isdir(full_path):
                    self.add_list_item(item + "/")
                else:
                    self.add_list_item(item)
        else:
            print("当前目录为空或无效")

    def add_list_item(self, name):
        item = QListWidgetItem(name)
        item.setFlags(
            item.flags() | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
        self.list_widget.addItem(item)

    def switch_to_selected_folder_and_refresh(self):
        new_dir = self.switch_to_selected_folder()
        if new_dir:
            self.current_dir = new_dir  # 更新当前文件夹路径
            self.update_current_folder_label()  # 更新当前文件夹标签
            self.update_list_widget()

    def go_back_and_refresh(self):
        self.go_back()
        self.update_list_widget()

    def open_current_directory_and_refresh(self):
        self.open_current_directory()
        self.update_list_widget()

    def switch_to_selected_folder(self):
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            selected_item_text = selected_items[0].text()
            full_path = os.path.join(self.current_dir, selected_item_text.rstrip("/"))
            if os.path.isdir(full_path):  # 检查是否是目录
                return full_path  # 返回新的当前文件夹路径
        return self.current_dir  # 如果没有有效的文件夹被选中，返回原始当前文件夹路径

    def go_back(self):
        self.current_dir = os.path.dirname(self.current_dir)
        self.update_list_widget()
        self.update_current_folder_label()

    def open_current_directory(self):
        if os.path.isdir(self.current_dir):
            subprocess.Popen(["explorer", self.current_dir])
        else:
            print("当前目录为空或无效")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("启动工具")
        self.setGeometry(100, 100, 400, 400)

        self.tool_dir = os.path.abspath("./")
        self.current_page = None

        self.setup_ui()

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.switch_to_main_page()

        self.menu_bar = self.menuBar()
        file_menu = self.menu_bar.addMenu("功能")

        self.func1_action = QAction("功能1", self)
        self.func1_action.triggered.connect(self.switch_to_main_page)
        file_menu.addAction(self.func1_action)

        self.func2_action = QAction("功能2", self)
        self.func2_action.triggered.connect(self.switch_to_sub_page)
        file_menu.addAction(self.func2_action)

    def switch_to_main_page(self):
        if self.current_page:
            self.current_page.setParent(None)
            self.current_page = None

        current_dir = os.getcwd()  # 获取当前目录
        self.current_page = Functionality(current_dir)  # 将当前目录传递给 Functionality 类
        self.layout.addWidget(self.current_page)

    def switch_to_sub_page(self):
        if self.current_page:
            self.current_page.setParent(None)
            self.current_page = None

        self.current_page = TerminalWidget(os.getcwd())
        self.layout.addWidget(self.current_page)

        self.current_page.update_list_widget()
        self.current_page.current_folder_label.setText(os.getcwd())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
