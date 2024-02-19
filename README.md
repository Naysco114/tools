实现了一个简单的文件浏览和命令执行工具
-
安装环境python3.11
在终端输入以下指令安装依赖

~~~
pip install -r requirements.txt
~~~

具体功能如下：

> 文件浏览功能:
>
>显示当前文件夹下的所有文件和文件夹列表。
> 可以通过按钮切换到其他盘符或文件夹。
> 提供返回上一级和打开当前文件夹的功能。
>
>命令执行功能：
>
>提供一个命令行界面，用户可以在其中输入命令。
> 可以执行常见的命令，例如在 Windows 下执行命令时可以切换盘符、列出文件夹内容等。
>
>执行文件功能：
>
>可以执行当前文件夹下选中的文件。
> 对于 Python 脚本、Java 可执行文件、Windows 可执行文件等，可以直接执行。
> 对于 Windows 的快捷方式（.lnk 文件），使用 Windows PowerShell 启动快捷方式。
>
>界面切换功能：
>
>可以通过菜单栏切换到不同的功能页面。
> 提供了两个功能页面：Functionality 页面和 TerminalWidget 页面，分别用于不同的使用场景。
> 总体来说，这个工具提供了基本的文件浏览和命令执行功能，方便用户在界面上进行文件管理和简单的命令操作。