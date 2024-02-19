# -*- coding: utf-8 -*-
import os
import platform
from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtGui import QAction
from window.get_file_name_gui import GetFileNameGUI
from window.two_window import TwoWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.get_file_name_gui = GetFileNameGUI()
        self.two_window = TwoWindow()

        self.stacked_widget.addWidget(self.get_file_name_gui)
        self.stacked_widget.addWidget(self.two_window)

        self.create_menu()

    def create_menu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&文件")

        exit_action = QAction("&退出", self)
        exit_action.triggered.connect(self.close)  # 退出窗口
        file_menu.addAction(exit_action)

        function_menu = menu_bar.addMenu("&功能")
        function_one_action = QAction("文件管理器", self)
        function_one_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.get_file_name_gui))
        function_menu.addAction(function_one_action)
        function_two_action = QAction("浏览器", self)
        function_two_action.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.two_window))
        function_menu.addAction(function_two_action)

        function_two_menu = menu_bar.addMenu("&系统功能")
        open_terminal_action = QAction("&打开终端", self)
        open_terminal_action.triggered.connect(self.open_terminal)
        function_two_menu.addAction(open_terminal_action)

    def open_terminal(self):
        current_path = self.get_file_name_gui.current_path  # 获取GetFileNameGUI实例的current_path属性
        if platform.system() == "Windows":
            os.system(f"start cmd /K cd {current_path}")
            self.get_file_name_gui.output_text.append("成功打开终端")
        elif platform.system() == "Linux":
            os.system(f"x-terminal-emulator --working-directory={current_path}")
            self.get_file_name_gui.output_text.append("成功打开终端")
