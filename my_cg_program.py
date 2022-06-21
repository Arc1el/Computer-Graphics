"""
컴퓨터그래픽스 - IPE (computer_graphics_IPE.py)

작성자          : 20197125 김현민
최초 작성일     : 2022. 04. 04.
마지막 수정일   : 2022. 06. 21.
작성 환경       : python 3.9.4 + PyQt5(GUI) + numpy
작성 목적       : 컴퓨터그래픽스 알고리즘의 이해 및 실습
이력사항        : 2022. 04. 04. 최초작성
                 2022. 04. 05. GUI환경 구현 및 DDA 알고리즘 추가
                 2022. 04. 06. Bresenham's line 알고리즘 추가
                 2022. 04. 11. Cartesian, Polar Coordinate Circle 알고리즘 추가
                 2022. 04. 12. Bresenham's Circle 알고리즘 추가
                 2022. 04. 13. Midpoint Circle 알고리즘 추가
                 2022. 04. 14. Polar Coordinate Ellipse 알고리즘 추가
                 2022. 04. 15. Bresenham's Ellipse 알고리즘 추가
                 2022. 04. 26. Y-X 다각형 주사선 채우기(Scanline filling) 알고리즘 구현
                 2022. 05. 11. 원점/임의의 점을 중심으로하는 3가지 기본변환 구현
                 2022. 05. 12. y=x 반사 구현
                 2022. 06. 02. Cohen-Sutherland 알고리즘 구현
                 2022. 06. 21. 알고리즘 파일 분리 및 마무리
"""

from re import T
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtTest
import math
import numpy as np

class MyApp(QMainWindow):

    # 프로그램 생성자
    def __init__(self):
        super().__init__()
        self.image = QImage(QSize(1000, 600), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawing = False
        self.brush_size = 1
        self.brush_color = Qt.black

        self.transform_points = []
        self.transform_qpoints = []
        self.transform_qpoints2 = []
        self.transform_qpoints3 = []
        self.wheel_points = []
        self.wheel_qpoints = []
        self.transform_x_value = 0
        self.transform_y_value = 0
        self.theta_value = 0

        # 모드 설정에 따른 플래그
        self.draw_mode = "None"
        # 클릭횟수를 저장, mod연산을통해 point1, point2를 구별
        self.counter = 0
        # 클릭이벤트를 통해서 point1, point2를 저장
        self.x1y1_point = QPoint()
        self.x2y2_point = QPoint()

        self.initUI()
        

    # 프로그램 UI 설정
    def initUI(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('Commands')
        linemenu = menubar.addMenu('Line Drawing')
        circlemenu = menubar.addMenu('Circle Drawing')
        ellipsemenu = menubar.addMenu('Ellipse Drawing')
        fillmenu = menubar.addMenu('Polygon Filling')
        transformmenu = menubar.addMenu('Transfrom')
        clippingmenu = menubar.addMenu('Line Clipping')
        
        # file menu
        clear_action = QAction('Clear All', self)
        clear_action.setShortcut('Ctrl+C')
        clear_action.triggered.connect(self.clear)
        save_action = QAction('Save as File', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save)
        quit_action = QAction('Quit', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.triggered.connect(QCoreApplication.instance().quit)
        
        # line menu
        dda_action = QAction('DDA Algorithm', self)
        dda_action.triggered.connect(self.dda_mode)
        cartesian_action = QAction('Cartesian Algorithm', self)
        cartesian_action.triggered.connect(self.cartesian_mode)
        polar_action = QAction('Polar Coordinate Algorithm', self)
        polar_action.triggered.connect(self.polar_mode)

        #circle menu
        bresenham_circle_action = QAction('Bresenham Algorithm', self)
        bresenham_circle_action.triggered.connect(self.bresenham_circle_mode)
        midpoint_circle_action = QAction('Midpoint Algorithm', self)
        midpoint_circle_action.triggered.connect(self.midpoint_circle_mode)
        bresenham_action = QAction('Bresenham Algorithm', self)
        bresenham_action.triggered.connect(self.bresenham_mode)

        # ellipse menu
        polar_ellipse_action = QAction('Polar ellipse Algorithm', self)
        polar_ellipse_action.triggered.connect(self.polar_ellipse_mode)
        bresenham_ellipse_action = QAction('Bresenham ellipse Algorithm', self)
        bresenham_ellipse_action.triggered.connect(self.bresenham_ellipse_mode)

        # y-x scanline menu
        x_y_scanning_fill_heptagon_action = QAction('Y-X Scan line fill Algorithm (heptagon shape)', self)
        x_y_scanning_fill_heptagon_action.triggered.connect(self.x_y_scanning_fill_heptagon_mode)
        x_y_scanning_fill_triangle_action = QAction('Y-X Scan line fill Algorithm (triangle shape)', self)
        x_y_scanning_fill_triangle_action.triggered.connect(self.x_y_scanning_fill_triangle_mode)
        x_y_scanning_fill_heart_action = QAction('Y-X Scan line fill Algorithm (heart shape)', self)
        x_y_scanning_fill_heart_action.triggered.connect(self.x_y_scanning_fill_heart_mode)

        # transform menu
        transform_translation_origin_action = QAction('Translation', self)
        transform_translation_origin_action.triggered.connect(self.transform_translation_origin_mode)
        transform_scaling_origin_action = QAction('Scaling (Origin Point)', self)
        transform_scaling_origin_action.triggered.connect(self.transform_scaling_origin_mode)
        transform_rotation_origin_action = QAction('Rotation (Origin Point)', self)
        transform_rotation_origin_action.triggered.connect(self.transform_rotation_origin_mode)
        transform_scaling_selected_action = QAction('Scaling (Selected Point)', self)
        transform_scaling_selected_action.triggered.connect(self.transform_scaling_selected_mode)
        transform_rotation_selected_action = QAction('Rotation (Selected Point)', self)
        transform_rotation_selected_action.triggered.connect(self.transform_rotation_selected_mode)
        transform_reflection_action = QAction('Reflection (y = x)', self)
        transform_reflection_action.triggered.connect(self.transform_reflection_mode)

        # clipping menu
        cohen_sutherland_action = QAction('Cohen-Sutherland Algorithm', self)
        cohen_sutherland_action.triggered.connect(self.cohen_sutherland_mode)

        # 메뉴에 액션 추가
        filemenu.addAction(clear_action)
        filemenu.addAction(save_action)
        filemenu.addAction(quit_action)
        linemenu.addAction(dda_action)
        linemenu.addAction(bresenham_action)
        circlemenu.addAction(cartesian_action)
        circlemenu.addAction(polar_action)
        circlemenu.addAction(bresenham_circle_action)
        circlemenu.addAction(midpoint_circle_action)
        ellipsemenu.addAction(polar_ellipse_action)
        ellipsemenu.addAction(bresenham_ellipse_action)
        fillmenu.addAction(x_y_scanning_fill_heptagon_action)
        fillmenu.addAction(x_y_scanning_fill_triangle_action)
        fillmenu.addAction(x_y_scanning_fill_heart_action)
        transformmenu.addAction(transform_translation_origin_action)
        transformmenu.addAction(transform_scaling_origin_action)
        transformmenu.addAction(transform_scaling_selected_action)
        transformmenu.addAction(transform_rotation_origin_action)
        transformmenu.addAction(transform_rotation_selected_action)
        transformmenu.addAction(transform_reflection_action)
        clippingmenu.addAction(cohen_sutherland_action)

        self.setWindowTitle('My CG Program - 20197125 김현민')
        self.setGeometry(300, 300, 400, 400)
        self.setFixedSize(1000, 600)
        self.statusBar().showMessage('좌표가 여기에 출력됩니다.')
        self.show()

    # 저장된 변수들을 모두 초기화하는 함수
    def del_all(self):
        self.transform_points = []
        self.transform_qpoints = []
        self.transform_qpoints2 = []
        self.transform_qpoints3 = []
        self.wheel_points = []
        self.wheel_qpoints = []
        self.transform_x_value = 0
        self.transform_y_value = 0
        self.theta_value = 0   

    # 점그리기, 선그리기를 위한 페인트 이벤트 설정
    def paintEvent(self, e):
        canvas = QPainter(self)
        canvas.drawImage(self.rect(), self.image, self.image.rect())
    
    #화면 지우기
    def clear(self):
        self.counter = 0
        self.image.fill(Qt.white)
        self.transform_points = []
        self.transform_qpoints = []
        self.update()

    # 마우스 관련된 이벤트
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = True
            self.counter += 1

            # 좌표를 얻어와서 point1, point2를 설정
            if self.counter%2 == 1:
                self.x1y1_point = e.pos()
            else:
                self.x2y2_point = e.pos()  

            if (self.draw_mode == "translate_origin" or 
                self.draw_mode == "scaling_origin" or 
                self.draw_mode == "rotation_origin" or
                self.draw_mode == "scaling_selected" or
                self.draw_mode == "rotation_selected" or
                self.draw_mode == "reflection"):

                self.transform_points.append([e.pos().x(), e.pos().y()])
                self.transform_qpoints.append(e.pos())
                self.mydrawPoint(Qt.blue, e.pos().x(), e.pos().y())
        
        if e.button() == Qt.RightButton:
            if self.draw_mode == "translate_origin":
                self.transform_translation_origin_function()
            elif self.draw_mode == "scaling_origin":
                self.transform_scaling_origin_function()
            elif self.draw_mode == "rotation_origin":
                self.transform_rotation_origin_function()
            elif self.draw_mode == "scaling_selected":
                self.transform_scaling_selected_function()
            elif self.draw_mode == "rotation_selected":
                self.transform_rotation_selected_function()
            elif self.draw_mode == "reflection":
                self.transform_reflection_function()

        if e.button() == Qt.MidButton:
            if (self.draw_mode == "scaling_selected" or
                self.draw_mode == "rotation_selected"):

                self.wheel_points.append([e.pos().x(), e.pos().y()])
                self.wheel_qpoints.append(e.pos())
                self.mydrawPoint(Qt.magenta, e.pos().x(), e.pos().y())


    def mouseMoveEvent(self, e):
        if (e.buttons() & Qt.LeftButton) & self.drawing:
            return

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.drawing = False

            # 마우스클릭(릴리즈)시에 설정된 모드에따라 function을 실행
            if self.draw_mode == "dda":
                if self.counter%2 != 1:
                    self.dda_function()
            
            if self.draw_mode == "bresenham":
                if self.counter%2 != 1:
                    self.bresenham_function()
            
            if self.draw_mode == "polar":
                if self.counter%2 != 1:
                    self.polar_function()

            if self.draw_mode == "cartesian":
                if self.counter%2 != 1:
                    self.cartesian_function()

            if self.draw_mode == "bresenham_circle":
                if self.counter%2 != 1:
                    self.bresenham_circle_function()

            if self.draw_mode == "midpoint":
                if self.counter%2 != 1:
                    self.midpoint_circle_function()

            if self.draw_mode == "polar_ellipse":
                if self.counter%2 != 1:
                    self.polar_ellipse_function()

            if self.draw_mode == "bresenham_ellipse":
                if self.counter%2 != 1:
                    self.bresenham_ellipse_function()
            
            if self.draw_mode == "cohen_sutherland":
                if self.counter%2 != 1:
                    self.cohen_sutherland_function()

    # 파일로 저장
    def save(self):
        self.counter = 0
        fpath, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")
        if fpath:
            self.image.save(fpath)
    
    # DDA 알고리즘을 활용한 라인드로잉
    def dda_mode(self):
        self.draw_mode = "dda"
        self.counter = 0
    def dda_function(self):
        print("DDA 알고리즘 start")
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))

        # 알고리즘 START
        x1, y1 = self.x1y1_point.x(), self.x1y1_point.y()
        x2, y2 = self.x2y2_point.x(), self.x2y2_point.y()
        x, y = x1, y1

        painter.drawPoint(int(x), int(y))

        dx = x2 - x1
        dy = y2 - y1

        steps = abs(dx) if abs(dx) > abs(dy) else abs(dy)

        x_inc = float(dx / steps)
        y_inc = float(dy / steps)

        for i in range(0, int(steps + 1)):
            painter.drawPoint(int(x1), int(y1))
            x1 += x_inc
            y1 += y_inc
            self.update()
            QtTest.QTest.qWait(1)
            

        # 스테이터스바에 출력, (left-top corner 형식이기때문에 보기좋게 값을 수정해주었음.)
        msg1 = "DDA 알고리즘 - (" + str(x) + ", " + str(-1*(y-600))+ ") -> (" + str(int(x1)) + ", " + str(int(-1*(y1-600))) + ")"
        msg2 = "  / 기울기 : " + str(round(((-1*(y1-600))-(-1*(y-600)))/(x1-x), 2))
        self.statusBar().showMessage(msg1 + msg2)
        self.update()

    # Bresenham 알고리즘을 활용한 라인드로잉
    def bresenham_mode(self):
        self.draw_mode = "bresenham"
        self.counter = 0
    def bresenham_function(self):
        print("Bresenham 알고리즘 start")
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))

        # 알고리즘 START
        x1, y1 = int(self.x1y1_point.x()), int(self.x1y1_point.y())
        x2, y2 = int(self.x2y2_point.x()), int(self.x2y2_point.y())
        gradient = (y2-y1) / (x2-x1)
        tmp_x, tmp_y = x1, y1

        x, y = x1, y1
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        slope = dy/float(dx)

        swap = False
        
        if slope > 1:
            dx, dy = dy, dx
            x, y = y, x
            x1, y1 = y1, x1
            x2, y2 = y2, x2
            swap = True

        p = 2*dy - dx

        painter.drawPoint(x, y)

        for i in range(2, dx):
            if p > 0:
                y = y + 1 if y < y2 else y - 1
                p = p + 2*(dy - dx)
            else:
                p = p + 2*dy

            x = x + 1 if x < x2 else x -1

            if swap == False:
                painter.drawPoint(x, y)
                msg1 = "Bresenham 알고리즘 - (" + str(tmp_x) + ", " + str(-1*(tmp_y-600))+ ") -> (" + str(int(x)) + ", " + str(int(-1*(y-600))) + ")"
            else:
                painter.drawPoint(y, x)
                msg1 = "Bresenham 알고리즘 - (" + str(tmp_x) + ", " + str(-1*(tmp_y-600))+ ") -> (" + str(600-int(x)) + ", " + str(int(y)) + ")"
            self.update()
            QtTest.QTest.qWait(1)
            

        # 스테이터스바에 출력
        msg2 = "  / 기울기 : " + str(round(-1*gradient, 2))
        self.statusBar().showMessage(msg1 + msg2)
        self.update()

    def cartesian_mode(self):
        self.draw_mode = "cartesian"
        self.counter = 0
    def cartesian_function(self):
        print("Cartesian circle 알고리즘 start")
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))

        # 알고리즘 START
        xc, yc = int(self.x1y1_point.x()), int(self.x1y1_point.y())
        x2, y2 = int(self.x2y2_point.x()), int(self.x2y2_point.y())


        delta_x = math.pow(x2 - xc, 2)
        delta_y = math.pow(y2 - yc , 2)
        radius = int(math.sqrt(delta_x + delta_y))

        for x in range(xc - radius, xc + radius):
            pow_r = math.pow(radius, 2)
            pow_xminc = math.pow(x-xc, 2)
            y = yc + math.sqrt(abs(pow_r - pow_xminc))
            painter.drawPoint(x, y)
            y = yc - math.sqrt(abs(pow_r - pow_xminc))
            painter.drawPoint(x, y)
            x = x + 1
            self.update()
            QtTest.QTest.qWait(1)

        # 스테이터스바에 출력
        msg1 = "Cartesian Circle 알고리즘 - 중심점 : (" + str(xc) + "," +  str(-1*(yc-600)) + ")"
        msg2 = "  x2y2점 : (" + str(x2) + "," + str(-1*(y2-600)) + ") 반지름 : " + str(radius)
        self.statusBar().showMessage(msg1 + msg2)
        self.update()


    def polar_mode(self):
        self.draw_mode = "polar"
        self.counter = 0
    def polar_function(self):
        print("Polar circle 알고리즘 start")
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))

        # 알고리즘 START
        x2, y2 = int(self.x1y1_point.x()), int(self.x1y1_point.y())
        x1, y1 = int(self.x2y2_point.x()), int(self.x2y2_point.y())

        delta_x = math.pow((x2-x1), 2)
        delta_y = math.pow((y2-y1), 2)

        radius = int(math.sqrt(delta_x + delta_y))

        for i in range(0, 45):
            radian = i * math.pi / 180
            x = int(radius * math.cos(radian))
            y = int(radius * math.sin(radian))

            painter.drawPoint(x2+x, y2+y)
            painter.drawPoint(x2+y, y2+x)
            painter.drawPoint(x2+y, y2-x)
            painter.drawPoint(x2+x, y2-y)
            painter.drawPoint(x2-x, y2-y)
            painter.drawPoint(x2-y, y2-x)
            painter.drawPoint(x2-y, y2+x)
            painter.drawPoint(x2-x, y2+y)
            self.update()
            QtTest.QTest.qWait(2)

        # 스테이터스바에 출력
        msg1 = "Polar Coordinates Circle 알고리즘 - 중심점 : (" + str(x2) + "," +  str(-1*(y2-600)) + ")"
        msg2 = "  x2y2점 : (" + str(x1) + "," + str(-1*(y1-600)) + ") 반지름 : " + str(radius)
        self.statusBar().showMessage(msg1 + msg2)
        self.update()

    
    def bresenham_circle_mode(self):
        self.draw_mode = "bresenham_circle"
        self.counter = 0
    def bresenham_circle_function(self):
        print("Bresenham circle 알고리즘 start")
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))

        
        # 알고리즘 START
        xc, yc = int(self.x1y1_point.x()), int(self.x1y1_point.y())
        x2, y2 = int(self.x2y2_point.x()), int(self.x2y2_point.y())

        delta_x = math.pow(x2 - xc, 2)
        delta_y = math.pow(y2 - yc , 2)
        r = int(math.sqrt(delta_x + delta_y))

        x, y = 0, r
        d = 3 - 2 * r
        painter.drawPoint(xc+x, yc+y)
        painter.drawPoint(xc-x, yc+y)
        painter.drawPoint(xc+x, yc-y)
        painter.drawPoint(xc-x, yc-y)
        painter.drawPoint(xc+y, yc+x)
        painter.drawPoint(xc-y, yc+x)
        painter.drawPoint(xc+y, yc-x)
        painter.drawPoint(xc-y, yc-x)
        self.update()
        QtTest.QTest.qWait(1)

        while y >= x :
            x += 1
            
            if d > 0:
                y -= 1
                d = d+4 * (x - y) + 10
            else:
                d = d+ 4 * x + 6
            painter.drawPoint(xc+x, yc+y)
            painter.drawPoint(xc-x, yc+y)
            painter.drawPoint(xc+x, yc-y)
            painter.drawPoint(xc-x, yc-y)
            painter.drawPoint(xc+y, yc+x)
            painter.drawPoint(xc-y, yc+x)
            painter.drawPoint(xc+y, yc-x)
            painter.drawPoint(xc-y, yc-x)
            self.update()
            QtTest.QTest.qWait(1)
        
        # 스테이터스바에 출력
        msg1 = "Bresenham Circle 알고리즘 - 중심점 : (" + str(xc) + "," +  str(-1*(yc-600)) + ")"
        msg2 = "  x2y2점 : (" + str(x2) + "," + str(-1*(y2-600)) + ") 반지름 : " + str(r)
        self.statusBar().showMessage(msg1 + msg2)
        self.update()

    def midpoint_circle_mode(self):
        self.draw_mode = "midpoint"
        self.counter = 0
    def midpoint_circle_function(self):
        print("Midpoint circle 알고리즘 start")
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))

        
        # 알고리즘 START
        xc, yc = int(self.x1y1_point.x()), int(self.x1y1_point.y())
        x2, y2 = int(self.x2y2_point.x()), int(self.x2y2_point.y())

        delta_x = math.pow(x2 - xc, 2)
        delta_y = math.pow(y2 - yc , 2)
        r = int(math.sqrt(delta_x + delta_y))
        x, y, d = r, 0, 0

        while x >= y:
            painter.drawPoint(xc+x, yc+y)
            painter.drawPoint(xc-x, yc+y)
            painter.drawPoint(xc+x, yc-y)
            painter.drawPoint(xc-x, yc-y)
            painter.drawPoint(xc+y, yc+x)
            painter.drawPoint(xc-y, yc+x)
            painter.drawPoint(xc+y, yc-x)
            painter.drawPoint(xc-y, yc-x)
            self.update()
            QtTest.QTest.qWait(1)

            if d <= 0:
                y += 1
                d = d + 2 * y + 1
            else:
                x -= 1
                d = d - 2 * x + 1

        # 스테이터스바에 출력
        msg1 = "MidPoint Circle 알고리즘 - 중심점 : (" + str(xc) + "," +  str(-1*(yc-600)) + ")"
        msg2 = "  x2y2점 : (" + str(x2) + "," + str(-1*(y2-600)) + ") 반지름 : " + str(r)
        self.statusBar().showMessage(msg1 + msg2)
        self.update()


    def polar_ellipse_mode(self):
        self.draw_mode = "polar_ellipse"
        self.counter = 0
    def polar_ellipse_function(self):
        print("Polar ellipse circle 알고리즘 start")
        
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))
        
        # 알고리즘 START
        x1, y1 = int(self.x1y1_point.x()), int(self.x1y1_point.y())
        x2, y2 = int(self.x2y2_point.x()), int(self.x2y2_point.y())
        xc, yc = int((x1 + x2)/2), int((y1 + y2)/2)

        rad_x = abs(x2 - xc)
        rad_y = abs(y2 - yc)

        for i in range(0, 90):
            radian = i * math.pi / 180
            p_x = int(xc + rad_x * math.cos(radian))
            p_y = int(yc + rad_y * math.sin(radian))

            m_x = int(xc - rad_x * math.cos(radian))
            m_y = int(yc - rad_y * math.sin(radian))

            painter.drawPoint(p_x, p_y)
            painter.drawPoint(p_x, m_y)
            painter.drawPoint(m_x, p_y)
            painter.drawPoint(m_x, m_y)
            self.update()
            QtTest.QTest.qWait(1)

        # 스테이터스바에 출력
        msg1 = "Polar Coordinate Ellipse 알고리즘 - 중심점 : (" + str(xc) + "," +  str(-1*(yc-600)) + ")"
        msg2 = "  x2y2점 : (" + str(x2) + "," + str(-1*(y2-600)) + ")   rx, ry : " + str(rad_x) + ", " + str(rad_y)
        self.statusBar().showMessage(msg1 + msg2)
        self.update()

    
    def bresenham_ellipse_mode(self):
        self.draw_mode = "bresenham_ellipse"
        self.counter = 0
    def bresenham_ellipse_function(self):
        print("Bresenham circle 알고리즘 start")
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))

        
        # 알고리즘 START
        xc, yc = int(self.x1y1_point.x()), int(self.x1y1_point.y())
        x2, y2 = int(self.x2y2_point.x()), int(self.x2y2_point.y())
        
        a = abs(x2 - xc)
        b = abs(y2 - yc)
        rx, ry = a, b
        b1 = b&1
        dx = 4 * (1 - a) * b * b
        dy = 4 * (b1 + 1) * a * a
        d = dx + dy + b1 + a * a
        d2 = 0

        if xc > x2:
            xc = x2
            x2 += a

        if yc > y2:
            yc = y2

        yc += (b + 1) / 2
        y2  = yc - b1
        a *= 8 * a
        b1 = 8 * b * b

        while xc <= x2:
            painter.drawPoint(x2, yc)
            painter.drawPoint(xc, yc)
            painter.drawPoint(xc, y2)
            painter.drawPoint(x2, y2)
            QtTest.QTest.qWait(1)

            d2 = 2 * d
            if d2 <= dy:
                yc += 1
                y2 -= 1
                d += dy
                dy += a
            if (d2 >= dx) | (2*d > dy):
                xc += 1
                x2 -= 1
                d += dx
                dx += b1

            self.update()

        while yc - y2 < b:
            painter.drawPoint(xc-1, yc)
            painter.drawPoint(x2+1, yc)
            yc += 1
            painter.drawPoint(xc-1, y2)
            painter.drawPoint(x2+1, y2)
            y2 -= 1
            QtTest.QTest.qWait(1)
            self.update()
        
        # 스테이터스바에 출력
        msg1 = "Bresenham's Ellipse 알고리즘 - 중심점 : (" + str(xc) + "," +  str(-1*(yc-600)) + ")"
        msg2 = "  x2y2점 : (" + str(x2) + "," + str(-1*(y2-600)) + ")   rx, ry : " + str(rx) + ", " + str(ry)
        self.statusBar().showMessage(msg1 + msg2)
        self.update()

    def mydrawline(self, p1, p2, color):
        # 해당 코드는 left-top 코너 방식이기때문에 이를 편하게 하기위해서 
        # canvas 사이즈인 600에서 y값을 빼주는 방식으로 라인을 그리는 함수
        painter = QPainter(self.image)
        painter.setPen(QPen(color, self.brush_size, Qt.SolidLine, Qt.RoundCap))

        # y좌표대신 600-y가 들어가기때문에 left-bottom corner 방식으로 동작가능
        painter.drawLine(p1[0], abs(600-p1[1]), p2[0], abs(600-p2[1]))
        self.update()

    def find_all_edges(self, p1, p2):
        x1, y1, x2, y2 = p1[0], p1[1], p2[0], p2[1]
        # Y-min : Pn과 Pn+1중 작은 y값
        # Y-max : Pn과 Pn+1중 큰 y값
        # X-val : y값이 가장 높은 정점과 연관된 x값
        # slope(1/m) : (x2-x1) / (y2 - y1)
        # ymin, ymax
        if y1 <= y2:
            ymin = y1
            ymax = y2
        else:
            ymin = y2
            ymax = y1

        # xval
        # y1, y2가 각각 ymin인경우 해당 y값에대한 x값이 xval임
        if y1 == ymin:
            xval = x1
        else:
            xval = x2

        # slope(1/m)
        # 점2의 y좌표에서 점1의 y좌표를 빼주었을때 0이면 inf로 설정해주었음
        if y2 - y1 == 0:
            slope = "INF"
        # 그 외에는 1/m을 slope로 설정해주었음
        else:
            slope = (x2 - x1) / (y2 - y1)

        return ymin, ymax, xval, slope
    
    def find_global_edges(self, edgelist):
        edge = []
        # slope가 inf가 아니고 ymin과 xval을 비교하여 edge들을 초기화
        for i in range(0, len(edgelist)):
            # inf가 아니라면
            if edgelist[i][3] != "INF":
                # 해당부분은 sorting시 sequence를 위해 분리한 코드임. +0.1을 활용하여 sorting시 순서를 정해줌
                if(edgelist[i][2] == edgelist[i+1][2]):
                    edge.append((edgelist[i][0], edgelist[i][1], edgelist[i][2]+0.1, edgelist[i][3]))
                else:
                    edge.append((edgelist[i][0], edgelist[i][1], edgelist[i][2], edgelist[i][3]))

        # sorting을 사용하여 재정렬
        edge = sorted(edge, key=lambda x : (x[0], x[2]))
        
        # sequence때문에 붙인 0.1를 다시 int화 시켜주어 제거해주었음
        for i in range(0, len(edge)):
            if isinstance(edge[i][2], int) == False:
                tmp = int(edge[i][2])
                edge[i] = (edge[i][0], edge[i][1], tmp, edge[i][3])
        return edge

    def init_active_global_edges(self, scanline, edgelist):
        # active와 global edge를 초기화
        active_edge = []
        global_edge = []
        # y좌표와 scanline이 같다면 active edge에 추가
        for i in range(0, len(edgelist)):
            if(edgelist[i][0] == scanline):
                active_edge.append(edgelist[i])
            # 아니라면 golbal edge(강의에서는 edge list)에 추가
            else:
                global_edge.append(edgelist[i])
        # active엣지의 xval값을 slope를 더해줘 update
        for i in range(0, len(active_edge)):
            active_edge[i] = (active_edge[i][0], active_edge[i][1],
             active_edge[i][2] + active_edge[i][3], active_edge[i][3])
        # 다시 재정렬
        active_edge = sorted(active_edge, key = lambda x : (x[0], x[2]))

        return active_edge, global_edge
    
    def mydrawlinescan(self, edgelist, scanline):
        # 패리티(홀짝여부 판단) 플래그를 활용하여 패리티를 mod 2연산하여
        # 해당값이 1인경우에만 점을찍어 색칠 (반복문을 활용하므로 색칠)
        painter = QPainter(self.image)
        painter.setPen(QPen(Qt.red, self.brush_size, Qt.SolidLine, Qt.RoundCap))
        parity = 0
        list_size = len(edgelist)

        # 액티브엣지에서 x값들을 따로 담을 배열
        x_arr = []
        # x값들을 저장
        for i in range(0, list_size):
            x_arr.append(int(edgelist[i][2]))
        # 엣지리스트의 x값 범위만큼을 for문을 활용하여 검사 및 점을 찍음
        for i in range(int(edgelist[0][2]), int(edgelist[list_size-1][2])) :
            # 변화하는 i값을 활용하여 j와 같다면(active edge의 x값과 같다면)
            for j in x_arr:
                if i == j:
                    # 패리티를 1증가시킴
                    parity += 1
                    #print("intersection", parity, "j값 : ", j)
            # 모듈러 연산으로 패리티비트의 홀짝여부 판단
            if parity % 2 == 1:
                painter.drawPoint(i, 600-scanline)
            # 색을 칠할때 너무 빨리칠해지기때문에 딜레이를 주어 칠해주었음
            if i % 40 == 0:
                QtTest.QTest.qWait(0)

            self.update()
        self.update()
    
    def update_active_global_edges(self, scanline, active_edges, global_edges):
        temp_active_edge = []
        active_edge = active_edges

        # gobal edge에 있던 엣지가 스캔라인이 변하여 사용되어야하는경우
        # append 해주어 acitve edge를 업데이트
        for i in range(0, len(global_edges)):
            if global_edges[i][0] == scanline:
                temp_active_edge.append(global_edges[i])
        
        # active edge에 있던 엣지가 스캔라인이 변화하여 더이상 사용되지 않는경우
        # y좌표가 더이상 scanline에 해당되지 않는경우는 제외해주었음
        for i in range(0, len(active_edge)):
            if active_edge[i][1] != scanline:
                temp_active_edge.append(active_edge[i])

        # 업데이트된 (temp)active_edge를 slope만큼 x값에 누적하여 x_val값을 업데이트
        for i in range(0, len(temp_active_edge)):
            if temp_active_edge[i][1] > scanline:
                temp_active_edge[i] = (temp_active_edge[i][0], temp_active_edge[i][1],
                temp_active_edge[i][2] + temp_active_edge[i][3], temp_active_edge[i][3])

        # (temp)active_edge를 다시 sorting 하여 xval, ymin순서로 정렬주었음
        temp_active_edge = sorted(temp_active_edge, key = lambda x : (x[2], x[0]))
                
        return temp_active_edge, global_edges

    def x_y_scanning_fill_mode(self, mode):
        self.draw_mode = "x_y_scanning_fill"
        self.counter = 0
        print("x-y scanning fill start")

        # 매개변수로 mode를 받기때문에 받아온 mode에 따라서 점 p가 결정되는 형태
        if mode == "heptagon":
            #점 7개
            p = [(100, 100), (100, 300), (200,200), (300, 400), (400,50), (500, 330), (600, 100)]
            # 선 그려 다각형 출력(외곽선)
            self.mydrawline(p[0], p[1], Qt.red)
            self.mydrawline(p[1], p[2], Qt.blue)
            self.mydrawline(p[2], p[3], Qt.magenta)
            self.mydrawline(p[3], p[4], Qt.green)
            self.mydrawline(p[4], p[5], Qt.cyan)
            self.mydrawline(p[5], p[6], Qt.darkGray)
            self.mydrawline(p[6], p[0], Qt.darkBlue)

        if mode == "triangle":
            #점 3개
            p = [(100, 100), (200, 300), (300, 100)]
            # 선 그려 다각형 출력(외곽선)
            self.mydrawline(p[0], p[1], Qt.red)
            self.mydrawline(p[1], p[2], Qt.blue)
            self.mydrawline(p[2], p[0], Qt.magenta)

        if mode == "heart":
            #점 7개
            p = [(400, 100), (600, 400), (500, 500), (400, 400), (300, 500), (200, 400), (400,100)]
            # 선 그려 다각형 출력(외곽선)
            self.mydrawline(p[0], p[1], Qt.red)
            self.mydrawline(p[1], p[2], Qt.blue)
            self.mydrawline(p[2], p[3], Qt.magenta)
            self.mydrawline(p[3], p[4], Qt.green)
            self.mydrawline(p[4], p[5], Qt.cyan)
            self.mydrawline(p[5], p[6], Qt.darkGray)
            self.mydrawline(p[6], p[0], Qt.darkBlue)

        # 모든 엣지 구하기
        # all_edges = [(ymin, ymax, xval, slope), ... ()]
        all_edges = []
        for i in range(0, len(p)):
            if i == len(p)-1:
                value = self.find_all_edges(p[i], p[0])
            else :
                value = self.find_all_edges(p[i], p[i+1])
            all_edges.append(value)

        # 글로벌 엣지 구하기
        # global_edges = [(ymin, ymax, xval, slope), ... ()]
        global_edges = self.find_global_edges(all_edges)

        # 스캔라인 초기화. 가장 작은 ymin을 가져오면 됨
        scanline = global_edges[0][0]
        sorted_line = sorted(global_edges, key=lambda x: (x[1]))

        # 루프돌릴 y구간 할당
        loop_scanline = sorted_line[len(sorted_line)-1][1] - scanline

        # active_edge, global_edge 초기화
        active_edges, global_edges = self.init_active_global_edges(scanline, global_edges)

        # 루프돌면서 scanline을 중가시키며 다각선을 filling
        for i in range(0, loop_scanline-1):
            scanline += 1
            # 엑티브, 글로벌 엣지 업데이트
            active_edges, global_edges = self.update_active_global_edges(scanline, active_edges, global_edges)

            # 업데이트된 글로벌엣지를 활용하여 색을 칠함
            self.mydrawlinescan(active_edges, scanline)
        self.update()

    def x_y_scanning_fill_heptagon_mode(self):
        mode = "heptagon"
        self.x_y_scanning_fill_mode(mode)
    def x_y_scanning_fill_triangle_mode(self):
        mode = "triangle"
        self.x_y_scanning_fill_mode(mode)
    def x_y_scanning_fill_heart_mode(self):
        mode = "heart"
        self.x_y_scanning_fill_mode(mode)

    # x, y값 입력 다이얼로그 출력
    def showDialog(self):
        x, ok1 = QInputDialog.getText(self, "X", "Enter X value")
        y, ok2 = QInputDialog.getText(self, "Y", "Enter Y value")
        if ok1:
            self.transform_x_value = float(x)
        if ok2:
            self.transform_y_value = float(y)
            
    def showDialogTheta(self):
        theta, ok3 = QInputDialog.getText(self, "Theta : ", "Enter Theta value")
        if ok3:
            self.theta_value = int(theta)

    # 좌표평면 출력
    def draw_coordinate(self):
        painter = QPainter(self.image)
        painter.setPen(QPen(Qt.red, self.brush_size, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(0, 300, 1000, 300)
        painter.drawLine(500, 600, 500, 0)
        self.update()
    
    def draw_y_x_line(self):
        painter = QPainter(self.image)
        painter.setPen(QPen(Qt.red, self.brush_size, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(200, 600, 800, 0)
        self.update()

    # 점찍는 유저정의함수 mydrawPoint
    def mydrawPoint(self, color, x, y):
        painter = QPainter(self.image)
        painter.setPen(QPen(color, 5, Qt.SolidLine, Qt.RoundCap))
        painter.drawPoint(x, y)
        self.update()

    # 마우스이벤트로 입력한 좌표를 사용하여 폴리곤을 그리는 함수
    def mydrawPoligon(self, color):
        painter = QPainter(self.image)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine, Qt.RoundCap))
        poligon = QPolygon(self.transform_qpoints)
        print("transfrom qpoints : ", self.transform_qpoints)
        painter.setBrush(QBrush(color))
        painter.drawPolygon(poligon)
        self.draw_coordinate()
        self.update()
        
    def mydrawPoligonQpoint(self, color, point):
        painter = QPainter(self.image)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine, Qt.RoundCap))
        poligon = QPolygon(point)
        painter.setBrush(QBrush(color))
        painter.drawPolygon(poligon)
        self.draw_coordinate()
        self.update()

    # 이동 함수
    def transform_translation_origin_mode(self):
        self.draw_mode = "translate_origin"
        self.draw_coordinate()
        self.counter = 0
    def transform_translation_origin_function(self):
        print("Translate_origin start")
        self.mydrawPoligon(Qt.green)

        if self.draw_mode != "None" :
            self.showDialog()
        self.draw_mode = "None"

        self.transform_qpoints = []
        for i in range(0, len(self.transform_points)):
            self.transform_points[i][0] = self.transform_points[i][0] + self.transform_x_value
            self.transform_points[i][1] = self.transform_points[i][1] + -1 * self.transform_y_value
            self.transform_qpoints.append(QPoint(self.transform_points[i][0], self.transform_points[i][1]))

        self.mydrawPoligon(Qt.red)
        self.update()
        self.del_all()

    # 신축(원점) 함수
    def transform_scaling_origin_mode(self):
        self.draw_mode = "scaling_origin"
        self.draw_coordinate()
        self.counter = 0
    def transform_scaling_origin_function(self):
        print("Scaling_origin start")
        self.mydrawPoligon(Qt.green)

        if self.draw_mode != "None" :
            self.showDialog()
        self.draw_mode = "None"

        # 대각행렬 생성
        self.transform_qpoints = []
        for i in range(0, len(self.transform_points)):
            matrix_origin = np.matrix([[1, 0, 500],
                                       [0, 1, 300],
                                       [0, 0,   1]])

            matrix_origin2 = np.matrix([[1, 0, -500],
                                        [0, 1, -300],
                                        [0, 0,    1]])

            matrix_s = np.matrix([[self.transform_x_value,                      0, 0],
                                  [0,                      self.transform_y_value, 0],
                                  [0,                                           0, 1]])   

            [matrix_x, matrix_y] = self.transform_points[i]
            matrix_xy = np.matrix([[matrix_x],
                                   [matrix_y],
                                   [       1]])

            final_matrix = matrix_origin @ matrix_s @ matrix_origin2 @ matrix_xy

            [point_x] = final_matrix.tolist()[0]
            [point_y] = final_matrix.tolist()[1]
            self.transform_qpoints.append(QPoint(point_x, point_y))
            del matrix_x, matrix_y, matrix_xy, final_matrix, point_x, point_y
    
        self.mydrawPoligon(Qt.red)
        
        self.update()
        self.del_all()

    # 회전(원점) 함수
    def transform_rotation_origin_mode(self):
        self.draw_mode = "rotation_origin"
        self.draw_coordinate()
        self.counter = 0
    def transform_rotation_origin_function(self):
        print("Scaling_origin start")
        self.mydrawPoligon(Qt.green)

        if self.draw_mode != "None" :
            self.showDialogTheta()
        self.draw_mode = "None"

        # 대각행렬 생성
        self.transform_qpoints = []
        for i in range(0, len(self.transform_points)):
            matrix_origin = np.matrix([[1, 0, 500],
                                       [0, 1, 300],
                                       [0, 0,   1]])

            matrix_origin2 = np.matrix([[1, 0, -500],
                                        [0, 1, -300],
                                        [0, 0,    1]])
            
            matrix_r = np.matrix([[math.cos(math.radians(self.theta_value)), -1*math.sin(math.radians(self.theta_value)), 0],
                                  [math.sin(math.radians(self.theta_value)),    math.cos(math.radians(self.theta_value)), 0],
                                  [                                       0,                                           0, 1]])

            [matrix_x, matrix_y] = self.transform_points[i]
            matrix_xy = np.matrix([[matrix_x],
                                   [matrix_y],
                                   [       1]])

            final_matrix = matrix_origin @ matrix_r @ matrix_origin2 @ matrix_xy

            [point_x] = final_matrix.tolist()[0]
            [point_y] = final_matrix.tolist()[1]
            self.transform_qpoints.append(QPoint(point_x, point_y))
        
        self.mydrawPoligon(Qt.red)
        self.update()
        self.del_all()

    # 신축(임의의 점) 함수
    def transform_scaling_selected_mode(self):
        self.draw_mode = "scaling_selected"
        self.draw_coordinate()
        self.counter = 0
    def transform_scaling_selected_function(self):
        print("Scaling_selected start")
        self.mydrawPoligon(Qt.green)

        if self.draw_mode != "None" :
            self.showDialog()
        self.draw_mode = "None"

        # 대각행렬 생성
        self.transform_qpoints = []
        for i in range(0, len(self.transform_points)):
            [wheel_x, wheel_y] = self.wheel_points[0]
            print(wheel_x, wheel_y)
            matrix_origin = np.matrix([[1, 0, wheel_x],
                                       [0, 1, wheel_y],
                                       [0, 0,   1]])

            matrix_origin2 = np.matrix([[1, 0, -1 * wheel_x],
                                        [0, 1, -1 * wheel_y],
                                        [0, 0,            1]])

            matrix_s = np.matrix([[self.transform_x_value,                      0, 0],
                                  [0,                      self.transform_y_value, 0],
                                  [0,                                           0, 1]])   

            [matrix_x, matrix_y] = self.transform_points[i]
            matrix_xy = np.matrix([[matrix_x],
                                   [matrix_y],
                                   [       1]])

            final_matrix = matrix_origin @ matrix_s @ matrix_origin2 @ matrix_xy
            [point_x] = final_matrix.tolist()[0]
            [point_y] = final_matrix.tolist()[1]
            print("point_x: ", point_x, "point_y: ", point_y)
            self.transform_qpoints.append(QPoint(int(point_x), int(point_y)))
            
        self.mydrawPoligon(Qt.red)
        self.update()
        self.del_all()

    # 회전(임의의 점)) 함수
    def transform_rotation_selected_mode(self):
        self.draw_mode = "rotation_selected"
        self.draw_coordinate()
        self.counter = 0
    def transform_rotation_selected_function(self):
        print("Scaling_selected start")
        self.mydrawPoligon(Qt.green)

        if self.draw_mode != "None" :
            self.showDialogTheta()
        self.draw_mode = "None"

        print(self.theta_value)

        # 대각행렬 생성
        self.transform_qpoints = []
        for i in range(0, len(self.transform_points)):
            [wheel_x, wheel_y] = self.wheel_points[0]
            matrix_origin = np.matrix([[1, 0, wheel_x],
                                       [0, 1, wheel_y],
                                       [0, 0,   1]])

            matrix_origin2 = np.matrix([[1, 0, -1 * wheel_x],
                                        [0, 1, -1 * wheel_y],
                                        [0, 0,            1]])
            
            matrix_r = np.matrix([[math.cos(math.radians(self.theta_value)), -1*math.sin(math.radians(self.theta_value)), 0],
                                  [math.sin(math.radians(self.theta_value)),    math.cos(math.radians(self.theta_value)), 0],
                                  [                                       0,                                           0, 1]])

            [matrix_x, matrix_y] = self.transform_points[i]
            matrix_xy = np.matrix([[matrix_x],
                                   [matrix_y],
                                   [       1]])

            final_matrix = matrix_origin @ matrix_r @ matrix_origin2 @ matrix_xy

            [point_x] = final_matrix.tolist()[0]
            [point_y] = final_matrix.tolist()[1]
            self.transform_qpoints.append(QPoint(point_x, point_y))
        
        self.mydrawPoligon(Qt.red)
        self.update()
        self.del_all()

    # 반사 함수
    def transform_reflection_mode(self):
        self.draw_mode = "reflection"
        self.draw_coordinate()
        self.draw_y_x_line()
        self.counter = 0
    def transform_reflection_function(self):
        print("Reflection start")
        self.mydrawPoligon(Qt.green)

        theta_value = 45
        # 대각행렬 생성
        self.transform_qpoints = []
        self.transform_qpoints2 = []
        temp = []
        for i in range(0, len(self.transform_points)):
            matrix_origin = np.matrix([[1, 0, 500],
                                       [0, 1, 300],
                                       [0, 0,   1]])

            matrix_origin2 = np.matrix([[1, 0, -500],
                                        [0, 1, -300],
                                        [0, 0,    1]])
            
            matrix_r = np.matrix([[math.cos(math.radians(theta_value)), -1*math.sin(math.radians(theta_value)), 0],
                                  [math.sin(math.radians(theta_value)),    math.cos(math.radians(theta_value)), 0],
                                  [                                  0,                                      0, 1]])

            [matrix_x, matrix_y] = self.transform_points[i]
            matrix_xy = np.matrix([[matrix_x],
                                   [matrix_y],
                                   [       1]])

            final_matrix = matrix_origin @ matrix_r @ matrix_origin2 @ matrix_xy

            [point_x] = final_matrix.tolist()[0]
            [point_y] = final_matrix.tolist()[1]
            self.transform_qpoints.append(QPoint(point_x, point_y))
            self.transform_qpoints2.append(QPoint(point_x, 600 - (point_y)))
            temp.append([point_x, 600 - (point_y)])
        
        QtTest.QTest.qWait(300)
        self.mydrawPoligon(QColor(0, 0, 0, 0))
        tqpoint = self.transform_qpoints2
        QtTest.QTest.qWait(300)
        self.mydrawPoligonQpoint(QColor(0, 0, 0, 0), tqpoint)

        theta_value = -45
        for i in range(0, len(self.transform_points)):
            matrix_origin = np.matrix([[1, 0, 500],
                                       [0, 1, 300],
                                       [0, 0,   1]])

            matrix_origin2 = np.matrix([[1, 0, -500],
                                        [0, 1, -300],
                                        [0, 0,    1]])
            
            matrix_r = np.matrix([[math.cos(math.radians(theta_value)), -1*math.sin(math.radians(theta_value)), 0],
                                  [math.sin(math.radians(theta_value)),    math.cos(math.radians(theta_value)), 0],
                                  [                                  0,                                      0, 1]])

            [matrix_x, matrix_y] = temp[i]
            matrix_xy = np.matrix([[matrix_x],
                                   [matrix_y],
                                   [       1]])

            final_matrix = matrix_origin @ matrix_r @ matrix_origin2 @ matrix_xy

            [point_x] = final_matrix.tolist()[0]
            [point_y] = final_matrix.tolist()[1]
            self.transform_qpoints3.append(QPoint(point_x, point_y))

        tqpoint = self.transform_qpoints3
        QtTest.QTest.qWait(300)
        self.mydrawPoligonQpoint(Qt.blue, tqpoint)
        self.update()
        self.del_all()
    
    # 코드계산
    def where_point(self, x, y):
        # 영역
        bit_in = 0      #0000
        bit_left = 1    #0001
        bit_right = 2   #0010
        bit_bottom = 4  #0100
        bit_top = 8     #1000

        # 윈도우 사이즈(max, min값 설정)
        wx_max = 750
        wx_min = 250
        wy_max = 450
        wy_min = 150

        where = bit_in
        if x < wx_min:
            where = bit_left
        elif x > wx_max:
            where = bit_right
        elif y < wy_min:
            where = bit_bottom
        elif y > wy_max:
            where = bit_top
        
        return where

    # Cohen-Sutherland 알고리즘을 활용한 line Clipping
    def cohen_sutherland_mode(self):
        self.draw_mode = "cohen_sutherland"
        self.counter = 0
        # window 그리기
        painter = QPainter(self.image)
        painter.setPen(QPen(Qt.red, self.brush_size, Qt.SolidLine, Qt.RoundCap))
        window = []
        window.append(QPoint(250, 150))
        window.append(QPoint(250, 450))
        window.append(QPoint(750, 450))
        window.append(QPoint(750, 150))
        poligon = QPolygon(window)
        painter.drawPolygon(poligon)
        self.update()
    def cohen_sutherland_function(self):
        print("Cohen-sutherland 알고리즘 start")
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brush_color, self.brush_size, Qt.SolidLine, Qt.RoundCap))

        # 위치
        bit_in = 0      #0000
        bit_left = 1    #0001
        bit_right = 2   #0010
        bit_bottom = 4  #0100
        bit_top = 8     #1000

        # 윈도우 사이즈(max, min값 설정)
        wx_max = 750
        wx_min = 250
        wy_max = 450
        wy_min = 150

        x1, y1, x2, y2 = self.x1y1_point.x(), self.x1y1_point.y(), self.x2y2_point.x(), self.x2y2_point.y()

        p1_bit = self.where_point(x1, y1)
        p2_bit = self.where_point(x2, y2)

        draw = False
        while True:
            if p1_bit == 0 and p2_bit == 0:
                draw = True
                break
            
            elif (p1_bit & p2_bit) != 0:
                break

            else:
                x, y = 1, 1
                if p1_bit != 0:
                    bit_out = p1_bit
                else:
                    bit_out = p2_bit

                # 교차점 구하기
                if bit_out & bit_top:
                    x = x1 + (x2 - x1) * (wy_max - y1) / (y2 - y1)
                    y = wy_max
                elif bit_out & bit_bottom:
                    x = x1 + (x2 - x1) * (wy_min - y1) / (y2 - y1)
                    y = wy_min
                elif bit_out & bit_right:
                    y = y1 + (y2 - y1) * (wx_max - x1) / (x2 - x1)
                    x = wx_max
                elif bit_out & bit_left:
                    y = y1 + (y2 - y1) * (wx_min - x1) / (x2 - x1)
                    x = wx_min

                if bit_out == p1_bit:
                    x1 = x
                    y1 = y
                    p1_bit = self.where_point(x1, y1)
                else:
                    x2 = x
                    y2 = y
                    p2_bit = self.where_point(x2, y2)

        if draw == True:
            print(x1, y1, x2, y2)
            print(p1_bit, p2_bit)
            painter.drawLine(x1, y1, x2, y2)
            self.update()
    
        self.del_all()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
