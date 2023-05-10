import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from one_day_a_tool import Ui_MainWindow
from datetime import datetime
import time
from PIL import Image
import os
import traceback


def current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# exception handle
def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(tb)
    # error popout
    QMessageBox.critical(None, "error", tb)


# include image
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, os.path.basename(relative_path))
    return os.path.join(os.path.abspath("."), relative_path)


# 处理图片
class Thread(QThread):
    trigger = pyqtSignal(str)
    image_list, compressed_num, save_folder = None, None, None

    def run(self):
        for image_index in range(len(self.image_list)):
            self.trigger.emit(f'{current_time()} 正在处理:{image_index+1}/{len(self.image_list)} {self.image_list[image_index]}')
            # 打开要压缩的图像
            image = Image.open(self.image_list[image_index])

            # 保存原始大小以进行比较
            original_size = image.size

            # 设置新的宽度和高度（这里将宽度减少50％，并调整高度以保持纵横比）
            new_width = int(original_size[0] * (1 - self.compressed_num))
            new_height = int((float(new_width) / original_size[0]) * original_size[1])

            # 使用抗锯齿算法重新采样图像并保存结果
            resized_image = image.resize((new_width, new_height), resample=Image.LANCZOS)
            resized_image.save(f'{self.save_folder}/{os.path.basename(self.image_list[image_index])}')

        time.sleep(1)
        self.trigger.emit(f'{current_time()} 处理完成')
        self.trigger.emit('-'*100)


class MyMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        image_size = ['原始比例', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%']
        self.image_list = []
        # add image to label
        self.label.setPixmap(QPixmap(resource_path('static/wechat.jpg')))
        # 上传
        self.pushButton_2.clicked.connect(self.upload_images)
        # tab1
        self.comboBox.addItems(image_size)
        self.pushButton.clicked.connect(self.run_thread)
        # 实例化线程
        self.thread = Thread()
        # 建立线程与槽函数连接
        self.thread.trigger.connect(self.image_processing)

    # 重写关闭窗口方法
    def closeEvent(self, event):
        if self.thread.isRunning():
            result = QMessageBox.question(self, '提示',
                                          '还有任务正在进行中，是否仍然退出？',
                                          QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                self.thread.terminate()  # 结束线程
                event.accept()
            else:
                event.ignore()
        else:
            # confirm exit
            result = QMessageBox.question(self, '提示',
                                            '是否退出程序？',
                                            QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

    def upload_images(self):
        self.image_list = QFileDialog.getOpenFileNames(self, "上传图片", "", "*.jpg;*.png")[0]
        if self.image_list:
            self.textBrowser.append(f'{current_time()} 已上传{len(self.image_list)}张图片')

    def run_thread(self):
        if self.image_list:
            self.textBrowser.append(f'{current_time()} 开始处理...')
            self.thread.image_list = self.image_list
            self.thread.compressed_num = 0 if self.comboBox.currentText() == '原始比例' else float(self.comboBox.currentText().strip('%'))/100
            self.thread.save_folder = f'{int(time.time())}_{"原始比例" if self.comboBox.currentText() == "原始比例" else "压缩" + self.comboBox.currentText()}'
            # 创建文件夹
            os.makedirs(self.thread.save_folder)
            # 启用线程
            self.thread.start()

    def image_processing(self, content):
        self.textBrowser.append(content)


if __name__ == "__main__":
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    mainwindow = MyMainWindow()
    mainwindow.setWindowTitle('图片压缩工具')
    mainwindow.setMinimumSize(960, 800)
    mainwindow.show()
    sys.exit(app.exec())




