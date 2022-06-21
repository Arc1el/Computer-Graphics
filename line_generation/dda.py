
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
