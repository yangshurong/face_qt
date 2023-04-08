from PIL import Image
from MyControl import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import *
from PySide2.QtCore import *
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
import threading
import cv2
import sys
import os
import PySide2
import datetime
import firstSource
import matplotlib
import matplotlib.pyplot as plt
import secondSource
from PySide2.QtGui import QMovie
import sys
matplotlib.use('agg')
sys.path.append('deploy')


dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
os.environ['PYTHON_EXE'] = sys.executable

TEST_IP = '172.20.215.217:8000'
INTERVAL_SECOND = 20
ALL_NUM_FRAME = 300

INIT_SHOW_INFO = '请将人脸置于屏幕中央'
WAIT_RESULT_BACK = '正在检测中，请稍后'
ERROR_READ_CAMERA = '摄像头读取失败'


class status():
    def __init__(self):
        # self.handleCalc()
        # 正常情况下应该是先跳转到主页menu，现在主页还没完善好，因此先跳转到行人单目标检测
        self.id_num = 0
        self.handleCalc()

    def show_ui(self, location):
        loca = "ui/"+location
        qfile_staus = QFile(loca)
        qfile_staus.open(QFile.ReadOnly)
        qfile_staus.close()
        self.ui = QUiLoader().load(qfile_staus)
        self.ui.setWindowTitle("安全人脸检测")
        appIcon = QIcon("source/first/logo.jpg")
        self.ui.setWindowIcon(appIcon)

    def help_set_shadow(self, x_offset, y_offset, radius, color, *control):
        for x in control:
            tempEffect = QGraphicsDropShadowEffect(self.ui)
            tempEffect.setOffset(x_offset, y_offset)
            tempEffect.setBlurRadius(radius)  # 阴影半径
            tempEffect.setColor(color)
            x.setGraphicsEffect(tempEffect)

    def handleCalc(self):
        self.show_ui("main_menu.ui")
        self.have_show_video = 0
        self.is_tracking = '--draw_center_traj'
        self.is_enter_surely = 0
        self.help_set_shadow(0, 0, 50, QColor(
            0, 0, 0, 0.06 * 255), self.ui.widget1, self.ui.widget1_2)
        self.help_set_shadow(-10, 10, 30, QColor(0, 0, 0, 0.06 * 255), self.ui.widget, self.ui.widget_3,
                             self.ui.widget_4, self.ui.widget_5, self.ui.widget_6, self.ui.widget_7, self.ui.widget_8)
        test_video = r"C:\Users\Administrator\Desktop\university\d4199e42f744cbe3be7f5ac262cd9056.mp4"
        label1 = MyMenuVideoLabel(
            "source/second/menu_car.PNG", 360+(578-360), 228, 320, 180, test_video, self.ui)
        label2 = MyMenuVideoLabel(
            "source/second/menu_pedestrian.PNG", 800+(578-360), 228, 320, 180, test_video, self.ui)

        self.ui.show()
        self.ui.pushButton.clicked.connect(self.save_person)
        self.ui.pushButton_2.clicked.connect(self.detect_person)

    def save_person(self):
        self.page_id = 2
        self.universe_for_one_small("car_one_photo.ui")
        self.is_draw_line = ''
        self.come_back = self.handleCalc
        self.ui.pushButton_13.clicked.connect(self.come_back)

    def detect_person(self):
        self.page_id = 2
        self.universe_for_one_small("car_one_photo.ui")
        self.is_draw_line = ''
        self.come_back = self.handleCalc
        self.ui.pushButton_13.clicked.connect(self.come_back)

    def universe_for_one_small(self, first_ui):
        self.show_ui(first_ui)
        self.file_path = []
        self.is_draw_line = ''
        # 先设置shadow
        self.have_show_video = 1
        self.help_set_shadow(0, 4, 0, QColor(
            221, 221, 221, 0.3 * 255), self.ui.label_3)
        self.help_set_shadow(0, 0, 50, QColor(
            221, 221, 221, 0.3 * 255), self.ui.widget_2, self.ui.widget_3)
        # self.ui.pushButton_addVideo.clicked.connect(
        #     lambda: self.load_video(self.ui.label_24)
        # )
        self.ui.pushButton_addVideo.clicked.connect(self.load_video)
        self.ui.pushButton_3.clicked.connect(self.stop_video)
        self.ui.show()
        self.ui.label_34.setAlignment(Qt.AlignCenter)
        self.ui.label_34.setFont(QFont("Roman times", 20, QFont.Bold))
        self.ui.label_34.setText(INIT_SHOW_INFO)

    def stop_video(self):
        try:
            self.timer_camera.stop()
            self.cap.release()
            self.ui.label_7.clear()
            self.ui.pushButton_addVideo.setVisible(True)
            self.ui.label_24.setVisible(True)
        except:
            pass

    def init_video_show(self):
        self.frame_list = []
        self.ui.label_7.clear()
        try:
            self.cap.release()
        except:
            self.cap = None

        try:
            self.timer_camera.stop()
        except:
            self.timer_camera = None

    def load_video(self):
        self.init_video_show()
        self.have_show_time = 0
        self.cap = cv2.VideoCapture(0)
        self.ui.label_7.setFixedSize(
            self.ui.label_7.width(), self.ui.label_7.height())
        self.frame_count = 0
        self.timer_camera = QTimer()
        self.timer_camera.timeout.connect(self.OpenFrame)
        self.timer_camera.start(INTERVAL_SECOND)
        self.ui.pushButton_addVideo.setVisible(False)
        self.ui.label_24.setVisible(False)

    def OpenFrame(self):
        ret, frame = self.cap.read()
        if ret:
            self.frame_list.append(frame)
            self.Display_Image(frame, self.ui.label_7)
            self.frame_count = self.frame_count + 1
        else:
            print("视频获取读取错误")
            self.cap.release()
            self.timer_camera.stop()
            self.ui.label_34.setText(ERROR_READ_CAMERA)

        if len(self.frame_list) == ALL_NUM_FRAME:
            print("视频读取结束")
            self.cap.release()
            self.timer_camera.stop()
            self.ui.label_34.setText(WAIT_RESULT_BACK)
            self.deal_result()

    def Display_Image(self, image, controller):
        """
        ！！！！！！！！！！！！！！！！！！这里一定要看
        最关键的是这个函数
        参数image就是要展示在页面里的视频

        除此之外，对各种展示信息的更新，直接在这个函数里对相应控件进行更新就可以

        然后所有需要手动设置的参数，阙值和时间长度，只要在页面上设置好，这里就能知道
        阙值：self.confi
        时间: self.time
        :param image:
        :param controller:
        :return:
        """
        self.have_show_time = self.have_show_time + 1
        if (len(image.shape) == 3):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            Q_img = QImage(image.data,
                           image.shape[1],
                           image.shape[0],
                           QImage.Format_RGB888)
        elif (len(image.shape) == 1):
            Q_img = QImage(image.data,
                           image.shape[1],
                           image.shape[0],
                           QImage.Format_Indexed8)
        else:
            Q_img = QImage(image.data,
                           image.shape[1],
                           image.shape[0],
                           QImage.Format_RGB888)
        controller.setPixmap(QtGui.QPixmap(Q_img))
        controller.setScaledContents(True)

    def get_result(self, model_name, img):
        with ModelClient(TEST_IP, model_name) as client:
            result_dict = client.infer_batch(img)
        return result_dict    

    def deal_result(self):
        # self.get_result('')
        
        pass


if __name__ == '__main__':

    app = QApplication([])
    MainWindow = QMainWindow()
    statu = status()
    statu.ui.show()
    app.exec_()
