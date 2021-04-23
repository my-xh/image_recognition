# -*- coding: utf-8 -*-

"""
@File    : main.py
@Time    : 2021/4/23 19:09
@Author  : my-xh
@Version : 1.0
@Software: PyCharm
@Desc    : 
"""

import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QSize
from main_window import Ui_MainWindow
from recognition import RecognizerManager


class MyUi(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()

    def setup(self):
        self.btn_select.clicked.connect(self.select_image)
        self.cb_type.currentIndexChanged.connect(self.select_type)
        self.btn_copy.clicked.connect(self.copy_result)

        self.select_type()  # 选择初始图片类型

        self.recg_mgr = RecognizerManager()  # 创建识别器管理者

    def select_image(self):
        """打开文件选择框进行图片选择"""
        self.image_name, _ = QFileDialog.getOpenFileName(self, '选择要识别的图片', directory='./image', filter='(*.jpg *.png)')
        if self.image_name:
            # 显示图片名
            self.edit_file.setText(os.path.basename(self.image_name))
            pixmap = QPixmap(self.image_name)
            # 等比例缩放图片
            scaled_pixmap = pixmap.scaled(QSize(411, 421), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            # 显示图片
            self.lb_image.setPixmap(scaled_pixmap)
            # 识别图像
            self.recognize()

    def select_type(self):
        """选择识别的图像类别"""
        self.image_type = self.cb_type.currentIndex()

    def recognize(self):
        """图像识别"""
        result = self.recg_mgr.recognize(self.image_name, self.image_type)
        self.lb_result.setText(result)

    def copy_result(self):
        """将识别结果复制到剪切板中"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.lb_result.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyUi()
    window.show()
    sys.exit(app.exec_())
