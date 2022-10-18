# coding:utf8
import os
import time
import re
import subprocess
from getpass import getuser
if os.environ.get('DEV'):
    from init_hrpyc import hou
else:
    import hou
# 如果houdini是以GUI方式打开的
if hou.isUIAvailable():
    # 导入Qt 多线程 信号
    from PySide2.QtCore import Qt, QThread, Signal
    # 导入进度条和GUI后台控制流
    #from PySide2.QtGui import QProgressDialog, QApplication
    from PySide2.QtWidgets import QApplication
    from PySide2.QtWidgets import QProgressDialog
    # 构建抛出线程的类
    class BackgroundRender(QThread):
        # 用于抓取完成百分比的正则
        pattern = re.compile(r'ALF_PROGRESS\s(\d+)%')
        # 定义一个信号
        progress = Signal(int)
        # 初始化类
        def __init__(self, cmd):
            # 初始化父类
            super(BackgroundRender, self).__init__()
            self.cmd = cmd
            self.process = None
            # 没有被取消
            self._canceled = False
        # 已经被取消
        def cancel(self):
            self._canceled = True

        def run(self):
            # 启动hython来输出缓存
            # 这里把stdout设置为PIPE是为了下面可以使用readline方法来读取文件数据
            # 这里把stdeer设置为PIPE是为了忽略一些错误。不至于直接输出到display上。
            sf = subprocess.STARTUPINFO
            sf.wShowWindow = subprocess.SW_HIDE
            sf.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
            self.process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            startupinfo = sf)
            # 如果没有被停止
            while not self._canceled:
                # 获得输出的数据每一行
                line = self.process.stdout.readline().strip()
                # 如果啥都没有就退出
                if not line:
                    break
                else:
                    # 匹配alfred德数据格式最后的百分比
                    match = self.pattern.match(line)
                    # 如果合法
                    if match:
                        # 获得已经输出的百分比
                        progress = int(match.group(1))
                        # 将百分比信号发送给进度条的setvalue槽
                        self.progress.emit(progress)
                # 设置刷新频率
                time.sleep(0.005)
            # 全部读取结束后结束掉打开的hython
            self.process.terminate()

# 初始化全局变量，新线程，进度条控件
BG_PROCESS = None
PROGRESS_DLG = None

# 后台渲染的窗口类
def find_parend_widget():
    # 获得houdini的app实例
    app = QApplication.instance()
    # 获得houdini的所有Widgets
    all_w = app.allWidgets()
    # 迭代每一个widgets
    for w in all_w:
        # 如果窗口是激活的
        if w.isActiveWindow():
            # 返回该窗口
            return w

def execute_in_background(node):
    # 首先存一下文件
    hou.hipFile.save()
    # 获得那个渲染按钮的完整路径,这里不支持mdd的后台。因为mdd本身就没有后台
    py = "hou.node('%s').node('render').render()" % node.path()
    # 这个是用于PySide启动另一个进程的解释器，传递完整的文件路径和内建内部节点的渲染render按钮的路径
    # hip相当于启动exe拖拽进去的文件。-c代表附加参数。
    cmd = 'hython.exe "{hip}" -c "{py}"'.format(hip=hou.hipFile.path(), py=py)

    global BG_PROCESS
    global PROGRESS_DLG
    # 创建一个进度条实例并制定父对象,父对象其实是当前激活的窗口
    PROGRESS_DLG = QProgressDialog(labelText="Rendering", parent=find_parend_widget())
    # 设置最大宽度
    PROGRESS_DLG.setMinimumWidth(100)
    # 设置style 文字居中，黑颜色，背景颜色是EBAC59，参数的写法好奇怪。貌似是QT的写法？
    PROGRESS_DLG.setStyleSheet("QProgressBar { text-align: center; color: black; } "
                                  "QProgressBar::chunk { background-color: #EBAC59; }")
    # 创建进程实例
    BG_PROCESS = BackgroundRender(cmd)
    # 关联新线程的刷新和控件的setvalue的信号槽
    BG_PROCESS.progress.connect(PROGRESS_DLG.setValue)
    # 关联关闭进度条和新进程状态的信号槽
    PROGRESS_DLG.canceled.connect(BG_PROCESS.cancel)
    # 关联新进程结束和更改版本的信号槽
    # 关联新进程结束和关闭进度条的信号槽
    BG_PROCESS.finished.connect(PROGRESS_DLG.close)
    # 开始新新线程（负责刷新百分比）
    BG_PROCESS.start()
    # 显示进度条
    PROGRESS_DLG.show()
