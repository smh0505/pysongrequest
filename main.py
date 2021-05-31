from PyQt5.QtWidgets import *
import sys
from pytube import YouTube


class window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedWidth(300)

        # labels
        l1 = QLabel()
        l2 = QLabel()
        l3 = QLabel()
        self.l4 = QLabel()
        l1.setText('유튜브 URL')
        l2.setText('시작 시간')
        l3.setText('종료 시간')
        self.l4.setText('유튜브 URL을 입력해주세요.')

        # textbox
        self.tb1 = QLineEdit()
        self.tb2 = QLineEdit()
        self.tb2.setReadOnly(True)
        self.tb1.returnPressed.connect(self.output)

        # checkboxes & spinboxes
        self.cb1 = QCheckBox()
        self.cb2 = QCheckBox()

        self.sp1 = QSpinBox()
        self.sp2 = QSpinBox()
        self.sp1.setMinimum(0)
        self.sp2.setMinimum(0)

        self.cb1.setEnabled(False)
        self.cb2.setEnabled(False)
        self.sp1.setEnabled(False)
        self.sp2.setEnabled(False)

        self.cb1.stateChanged.connect(self.defaultTime)
        self.cb2.stateChanged.connect(self.defaultTime)

        self.sp1.valueChanged.connect(self.checkTime)
        self.sp2.valueChanged.connect(self.checkTime)

        # buttons
        # b1 = QPushButton()
        b2 = QPushButton()
        # b1.setText('확인')
        b2.setText('종료')
        # b1.clicked.connect(self.output)
        b2.clicked.connect(self.close)

        # layout
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.cb1)
        hbox1.addWidget(self.sp1, 250)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.cb2)
        hbox2.addWidget(self.sp2, 250)

        hbox3 = QHBoxLayout()
        # hbox3.addWidget(b1)
        hbox3.addStretch()
        hbox3.addWidget(b2)

        fbox = QFormLayout()
        fbox.addRow(l1, self.tb1)
        fbox.addRow(l2, hbox1)
        fbox.addRow(l3, hbox2)
        fbox.addRow(self.l4)
        fbox.addRow(self.tb2)
        fbox.addRow(hbox3)
        self.setLayout(fbox)

        self.setWindowTitle("PySR")
        self.show()

    def defaultTime(self):
        self.sp1.setEnabled(self.cb1.isChecked())
        self.sp2.setEnabled(self.cb2.isChecked())
        if not self.sp1.isEnabled():
            self.sp1.setValue(self.sp1.minimum())
        if not self.sp2.isEnabled():
            self.sp2.setValue(self.sp2.maximum())

    def output(self):
        try:
            self.yt = YouTube(self.tb1.text())
            self.cb1.setEnabled(True)
            self.cb2.setEnabled(True)
            self.sp1.setMaximum(self.yt.length)
            self.sp2.setMaximum(self.yt.length)
            self.sp2.setValue(self.yt.length)
            self.checkTime()
        except:
            self.l4.setText('유튜브 URL을 입력해주세요.')
            self.cb1.setEnabled(False)
            self.cb2.setEnabled(False)
            self.tb2.setText('')

    def checkTime(self):
        if self.sp1.value() >= self.sp2.value():
            self.l4.setText('영상 길이가 너무 짧습니다.')
            self.sp2.setValue(self.sp1.value())
            self.tb2.setText('')
        elif (self.sp2.value() - self.sp1.value()) > 150:
            self.l4.setText('영상 길이가 너무 깁니다.')
            self.tb2.setText('')
        else:
            self.l4.setText('유튜브 URL을 발견했습니다.')
            self.printLink()

    def printLink(self):
        link = '!sr ' + self.tb1.text()
        if self.sp1.isEnabled():
            link += '&start=' + str(self.sp1.value())
        if self.sp2.isEnabled():
            link += '&end=' + str(self.sp2.value())
        self.tb2.setText(link)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = window()
    sys.exit(app.exec_())
