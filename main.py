import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, QDialog
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QThread, pyqtSignal
from toolbox import Ui_MainWindow
import pandas as pd
from datetime import datetime
import time


def current_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# 处理图片
class Thread1(QThread):
    trigger = pyqtSignal(str)
    image_list = []

    def run(self):
        for image_index in range(len(self.image_list)):
            time.sleep(1)
            self.trigger.emit(f'{current_time()} 正在处理:{image_index+1}/{len(self.image_list)} {self.image_list[image_index]}')
        time.sleep(1)
        self.trigger.emit(f'{current_time()} 处理完成')
        self.trigger.emit('-'*100)


# 处理音频
class Thread2(QThread):
    trigger = pyqtSignal(str)
    audio_list = []

    def run(self):
        for audio_index in range(len(self.audio_list)):
            time.sleep(1)
            self.trigger.emit(f'{current_time()} 正在处理:{audio_index+1}/{len(self.audio_list)} {self.audio_list[audio_index]}')
        time.sleep(1)
        self.trigger.emit(f'{current_time()} 处理完成')
        self.trigger.emit('-'*100)


# 处理pdf
class Thread3(QThread):
    trigger = pyqtSignal(str)
    pdf_list = []

    def run(self):
        for pdf_index in range(len(self.pdf_list)):
            time.sleep(1)
            self.trigger.emit(f'{current_time()} 正在处理:{pdf_index+1}/{len(self.pdf_list)} {self.pdf_list[pdf_index]}')
        time.sleep(1)
        self.trigger.emit(f'{current_time()} 处理完成')
        self.trigger.emit('-'*100)


class MyMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

        image_size = ['默认', '自定义']
        self.image_list, self.audio_list, self.pdf_list = [], [], []
        # 上传
        self.pushButton_2.clicked.connect(self.upload_images)
        self.pushButton_3.clicked.connect(self.upload_audio)
        self.pushButton_5.clicked.connect(self.upload_pdf)
        # tab1
        self.comboBox.addItems(image_size)
        self.comboBox.currentTextChanged.connect(self.size_changed)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setValidator(QIntValidator(1, 9999))
        self.lineEdit.setValidator(QIntValidator(1, 9999))
        self.pushButton.clicked.connect(self.run_thread1)
        # tab2
        self.pushButton_4.clicked.connect(self.run_thread2)
        # tab3
        self.radioButton.setChecked(True)
        self.pushButton_7.clicked.connect(self.run_thread3)
        # tab4
        self.pushButton_6.clicked.connect(self.start_record)
        self.pushButton_8.clicked.connect(self.finish_record)
        # 实例化线程
        self.thread1 = Thread1()
        self.thread2 = Thread2()
        self.thread3 = Thread3()
        # 建立线程与槽函数连接
        self.thread1.trigger.connect(self.image_processing)
        self.thread2.trigger.connect(self.audio_processing)
        self.thread3.trigger.connect(self.pdf_processing)

    # 重写关闭窗口方法
    def closeEvent(self, event):
        if self.thread1.isRunning():
            result = QMessageBox.question(self, '提示',
                                          '还有任务正在进行中，是否仍然退出？',
                                          QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                self.thread1.terminate()  # 结束线程
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def upload_images(self):
        self.image_list = QFileDialog.getOpenFileNames(self, "上传图片", "", "*.jpg;*.png")[0]
        if self.image_list:
            self.textBrowser.append(f'{current_time()} 已上传{len(self.image_list)}张图片')

    def upload_audio(self):
        self.audio_list = QFileDialog.getOpenFileNames(self, "上传音频", "", "*.ncm")[0]
        if self.audio_list:
            self.textBrowser_2.append(f'{current_time()} 已上传{len(self.audio_list)}条音频')

    def upload_pdf(self):
        self.pdf_list = QFileDialog.getOpenFileNames(self, "上传pdf", "", "*.pdf")[0]
        if self.pdf_list:
            self.textBrowser_3.append(f'{current_time()} 已上传{len(self.pdf_list)}个文件')

    def size_changed(self):
        if self.comboBox.currentText() == '默认':
            self.lineEdit_2.clear()
            self.lineEdit.clear()
            self.lineEdit_2.setPlaceholderText('')
            self.lineEdit.setPlaceholderText('')
            self.lineEdit_2.setEnabled(False)
            self.lineEdit.setEnabled(False)
        else:
            self.lineEdit_2.setEnabled(True)
            self.lineEdit.setEnabled(True)
            self.lineEdit_2.setPlaceholderText('请输入不超过四位的正整数')
            self.lineEdit.setPlaceholderText('请输入不超过四位的正整数')

    def run_thread1(self):
        if self.image_list:
            self.textBrowser.append(f'{current_time()} 开始处理...')
            self.thread1.image_list = self.image_list
            # 启用线程
            self.thread1.start()

    def image_processing(self, content):
        self.textBrowser.append(content)

    def run_thread2(self):
        if self.audio_list:
            self.textBrowser_2.append(f'{current_time()} 开始处理...')
            self.thread2.audio_list = self.audio_list
            # 启用线程
            self.thread2.start()

    def audio_processing(self, content):
        self.textBrowser_2.append(content)

    def run_thread3(self):
        print(self.radioButton.isChecked())
        if self.pdf_list:
            self.textBrowser_3.append(f'{current_time()} 开始处理...')
            self.thread3.pdf_list = self.pdf_list
            # 启用线程
            self.thread3.start()

    def pdf_processing(self, content):
        self.textBrowser_3.append(content)

    def start_record(self):
        self.textBrowser_4.append(f'{current_time()} 开始录屏')

    def finish_record(self):
        self.textBrowser_4.append(f'{current_time()} 结束录屏')
        save_path = QFileDialog.getSaveFileName(self, '保存视频', f'{int(time.time())}_录屏.mp4')[0]
        if save_path:
            self.textBrowser_4.append(f'{current_time()} 视频已保存至：{save_path}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MyMainWindow()
    mainwindow.setWindowTitle('ToolBox')
    mainwindow.setMinimumSize(960, 800)
    mainwindow.show()
    sys.exit(app.exec())




