import os
import tkinter as tk
import platform

class GetFileNameGUI:
    def __init__(self, root):
        self.root = root
        self.current_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../tools")
        self.get_subdirectories()

        self.label = tk.Label(root, text="选择的目录:")
        self.label.pack()

        self.directory_label = tk.Label(root, text=self.current_directory)
        self.directory_label.pack()

        self.lists_frame = tk.Frame(root)
        self.lists_frame.pack()

        self.subdirectories_listbox = tk.Listbox(self.lists_frame)
        self.subdirectories_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.files_listbox = tk.Listbox(self.lists_frame)
        self.files_listbox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.display_current_directory()

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.switch_button = tk.Button(self.button_frame, text="切换目录", command=self.switch_directory)
        self.switch_button.pack(side=tk.LEFT)

        self.parent_button = tk.Button(self.button_frame, text="返回上一级", command=self.parent_directory)
        self.parent_button.pack(side=tk.LEFT)

        self.open_terminal_button = tk.Button(self.button_frame, text="打开终端", command=self.open_terminal)
        self.open_terminal_button.pack(side=tk.LEFT)

        self.quit_button = tk.Button(self.button_frame, text="退出", command=root.quit)
        self.quit_button.pack(side=tk.LEFT)

    def get_subdirectories(self):
        """
        获取当前目录下的子目录列表
        """
        self.subdirectories = [name for name in os.listdir(self.current_directory)
                               if os.path.isdir(os.path.join(self.current_directory, name))]
        self.subdirectories_with_index = {i + 1: subdir for i, subdir in enumerate(self.subdirectories)}

    def list_files(self):
        """
        获取当前目录下的文件列表
        """
        return [name for name in os.listdir(self.current_directory)
                if os.path.isfile(os.path.join(self.current_directory, name))]

    def display_current_directory(self):
        """
        显示当前目录、子目录和文件列表
        """
        self.directory_label.config(text="选择的目录: " + self.current_directory)

        self.subdirectories_listbox.delete(0, tk.END)
        for subdir in self.subdirectories_with_index.values():
            self.subdirectories_listbox.insert(tk.END, subdir)

        self.files_listbox.delete(0, tk.END)
        for file in self.list_files():
            self.files_listbox.insert(tk.END, file)

    def switch_directory(self):
        """
        切换到选择的目录
        """
        choice = self.subdirectories_listbox.curselection()
        if choice:
            subdir_index = choice[0] + 1
            self.current_directory = os.path.join(self.current_directory, self.subdirectories_with_index[subdir_index])
            self.get_subdirectories()
            self.display_current_directory()

    def parent_directory(self):
        """
        返回上一级目录
        """
        self.current_directory = os.path.dirname(self.current_directory)
        self.get_subdirectories()
        self.display_current_directory()

    def open_terminal(self):
        """
        打开终端
        """
        if platform.system() == "Windows":
            os.system("start cmd /K cd " + self.current_directory)
        elif platform.system() == "Linux":
            os.system("x-terminal-emulator --working-directory=" + self.current_directory)

# 创建 Tkinter 应用程序
root = tk.Tk()
root.title("文件浏览器")

# 创建 GetFileNameGUI 实例
app = GetFileNameGUI(root)

# 运行 Tkinter 主循环
root.mainloop()
