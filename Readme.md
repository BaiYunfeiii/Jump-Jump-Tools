# 跳一跳插件

功能：
1. 自动识别棋子和目标盒子的位置，并计算距离和按压时间
2. 自动按压屏幕，并产生一定的随机误差（模拟手指误差）
3. Parser.py中有绘制识别结果和方法，供调试时使用

使用方法：
1. 电脑安装adb并配置好环境变量
2. 将手机用数据线连接到电脑，并打开手机的USB调试功能
3. 运行Controller.py

项目依赖：
1. python3
2. PIL
3. matplotlib