#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Author: HUANG Jingyi
File: qt_test.py
Date:  2025-02-17 23:20:24
Email: pierrehuang1998@gmail.com
Description: 
"""

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PyQt6 示例窗口")
        self.setGeometry(100, 100, 300, 200)

        self.button = QPushButton("点击我", self)
        self.button.clicked.connect(self.show_message)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def show_message(self):
        QMessageBox.information(self, "消息", "你点击了按钮！")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

