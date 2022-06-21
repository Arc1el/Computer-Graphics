컴퓨터그래픽스 - 통합실습환경 (IPE : Integrated Practice Environment)
=============
실습환경 (Development Environment)
-------------
* Python 3.9
* pyQt5
* matplotlib

구현 알고리즘 목록 (List of implementation algorithms)
-------------
1. DDA Line generation
2. Bresenham's Line generation
3. Cartesian Circle generation
4. Polar Coordinate Circle generation
5. Bresenham's Circle generation
6. Midpoint Circle geneartion
7. Bresenham's Ellipse Circle generation
8. Polar Coordinate Ellipse Circle generation
9. Y-X Polygon Filling (Scanline Filling)
10. 2D transform Translation
11. 2D transform Scaling (Origin point)
12. 2D transform Scaling (Selected point)
13. 2D transfrom Rotation (Origin point)
14. 2D transfrom Rotation (Selected point)
15. 2D trasnfrom Reflection (y = x)
16. Cohen-Sutherland Line Clipping

이벤트 처리 및 사용법 (Event handling and usage)
------------
- 파일메뉴로 알고리즘을 선택하면 프로그램내의 mode가 설정됨.<br/>
- 설정된 모드에 따라 마우스 이벤트가 동작<br/>
- 좌/중앙 클릭시 좌표값을 가져오며, 우클릭시 알고리즘함수가 동작.<br/>
- 동작 완료후 초기화 (화면 유지)
###### If you select an algorithm from the file menu, the mode in the program is set.<br/>Mouse events behave according to the set mode<br/>Gets the coordinate value when left/center clicked, and algorithm function when right clicked.<br/>Initialize after completion of operation (hold screen)<br/>
1. 메인화면의 파일메뉴를 사용하여 원하는 알고리즘 선택<br/>
2. 점을 찍는 “좌푯값”이 필요한 모든 알고리즘에 대해서 “좌클릭”을 사용하여 점을 추가<br/>
3. “기준점”이 필요한 모든 알고리즘에 대하여 “중앙클릭”을 사용하여 기준점을 추가<br/>
4. “우클릭”을 활용하여 좌표를 추가하는 행위를 멈추고 알고리즘 동작<br/>
5. x, y, scale, theta 값이 필요한 알고리즘의 경우 발생하는 다이얼로그 창에 값을 입력<br/>
6. 화면에 결과물이 출력됨<br/>
###### 1. Select the desired algorithm using the file menu on the main screen<br/>2. For all algorithms that require a "coordinate value" to mark points, use "left click" to add points<br/>3. For all algorithms that require a "reference point", add a reference point using "central click"<br/>4. Stop adding coordinates using "right-click" and use algorithmic behavior<br/>5. Enter values in the dialog window that occurs for algorithms that require x, y, scale, and theta values<br/>6. Results are printed on the screen<br/>

실행예시 (Example of execution)
------------
![2d_rotation](https://user-images.githubusercontent.com/8403172/174779778-58ba589d-ffc5-4896-ad40-38426c5967c0.gif)
