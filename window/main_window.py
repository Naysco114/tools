# -*- coding: utf-8 -*-
import os
import platform
from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtGui import QAction

from window.CTF_page import CTFPage
from window.get_file_name_gui import GetFileNameGUI
from window.two_window import TwoWindow
from window.CTF.encode_decode_tools import EncodeDecodeTools
# from window.CTF.network_scanner import NetworkScanner
from window.CTF.cryptography_tools import CryptographyTools
from window.aboutpage import AboutPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.get_file_name_gui = GetFileNameGUI()
        self.two_window = TwoWindow()
        self.about_page = AboutPage()
        self.encodedecodetools = EncodeDecodeTools()
        self.cryptographytools = CryptographyTools()
        # self.networkscanner = NetworkScanner()

        self.stacked_widget.addWidget(self.get_file_name_gui)
        self.stacked_widget.addWidget(self.two_window)
        self.stacked_widget.addWidget(self.about_page)
        self.stacked_widget.addWidget(self.encodedecodetools)
        self.stacked_widget.addWidget(self.cryptographytools)
        # self.stacked_widget.addWidget(self.networkscanner)

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

        ctf_toolbox_menu = menu_bar.addMenu("&CTF工具箱")
        encode_decode_tools = QAction("&编码解码", self)
        encode_decode_tools.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.encodedecodetools))
        ctf_toolbox_menu.addAction(encode_decode_tools)
        encode_decode_tools = QAction("&密码学", self)
        encode_decode_tools.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.cryptographytools))
        ctf_toolbox_menu.addAction(encode_decode_tools)
        # encode_decode_tools = QAction("&网络扫描", self)
        # encode_decode_tools.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.networkscanner))
        # ctf_toolbox_menu.addAction(encode_decode_tools)

        about_action = QAction("&关于", self)
        about_action.triggered.connect(self.show_about_page)
        menu_bar.addAction(about_action)

    def open_terminal(self):
        current_path = self.get_file_name_gui.current_path  # 获取GetFileNameGUI实例的current_path属性
        if platform.system() == "Windows":
            os.system(f"start cmd /K cd {current_path}")
            self.get_file_name_gui.output_text.append("成功打开终端")
        elif platform.system() == "Linux":
            os.system(f"x-terminal-emulator --working-directory={current_path}")
            self.get_file_name_gui.output_text.append("成功打开终端")

    def show_ctf_page(self):
        # 创建 CTF 工具箱页面实例
        ctf_page = CTFPage()
        # 在 stacked_widget 中显示 CTF 工具箱页面
        self.stacked_widget.addWidget(ctf_page)
        self.stacked_widget.setCurrentWidget(ctf_page)

    def show_about_page(self):
        # 创建关于页面实例
        about_page = AboutPage()
        # 在 stacked_widget 中显示关于页面
        self.stacked_widget.addWidget(about_page)
        self.stacked_widget.setCurrentWidget(about_page)
