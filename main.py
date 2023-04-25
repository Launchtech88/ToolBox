import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
from MainWindows import Ui_MainWindow
import pandas as pd


class MyMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)

    def upload_file(self):
        file = QFileDialog.getOpenFileName(self, "上传文件", "", "*.docx;*.pdf")[0]

    # 定义提取方法
    def extract(self):
        # 获取关键词
        keyword = self.lineEdit.text().strip().split('、')
        if self.res:
            # table 构造
            for i, item in enumerate(self.res.items()):
                self.tableWidget.setRowCount(i)
                self.tableWidget.insertRow(i)
                cl0 = QTableWidgetItem(str(item[0]))
                cl1 = QTableWidgetItem(str(item[1]))
                self.tableWidget.setItem(i, 0, cl0)
                self.tableWidget.setItem(i, 1, cl1)
            self.textBrowser.append('提取成功')

    def download(self):
        if self.res:
            save_path = QFileDialog.getSaveFileName(self, 'Save file', '提取结果.xlsx', '*.xlsx')[0]
            if save_path:
                df = pd.DataFrame.from_dict(self.res, orient='index').reset_index()
                df.columns = ['关键词', '提取信息']
                df.to_excel(save_path, index=False)
                self.textBrowser.append('下载成功')

    def run_extract(self):
        try:
            self.extract()
        except Exception as e:
            print(e)
            self.textBrowser.append(str(e))

    def run_download(self):
        try:
            self.download()
        except Exception as e:
            print(e)
            self.textBrowser.append(str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = MyMainWindow()
    mainwindow.showMaximized()
    sys.exit(app.exec())




