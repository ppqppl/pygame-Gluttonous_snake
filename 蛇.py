# -*- coding: utf-8 -*-
# python实现：贪吃蛇
"""
游戏玩法：回车开始游戏；空格暂停游戏/继续游戏；方向键/wsad控制小蛇走向
"""
'''
思路：用列表存储蛇的身体；用浅色表示身体，深色背景将身体凸显出来；
1）
蛇的移动,首先根据方向来判断，这里使用pos变量来记录方向
pos(1, 0) //表示当前蛇向右的方向
pos(-1, 0) //表示当前蛇向左的方向
pos(0, 1) //表示当前蛇向下的方向
pos(0, -1) //表示当前蛇向上的方向
2）
怎么能控制蛇的速度呢？
其实是控制时间来刷新，我们知道所有的动作都在一个循环里面完成的，也就是代码都一直在运行着。
比如我设置速度为1，表示一秒刷新一次，那么蛇的移动也就是一秒一次，我们看到的也是一秒移动一格。
当我们设置速度为0.5,表示0.5秒刷新一次，那我们就看到0.5秒移动一格，速度就相对地看起来快了

蛇的移动：仔细观察，是：身体除头和尾不动、尾部消失，头部增加，所以，新添加的元素放在列表头部、删除尾部元素；
游戏结束判定策略：超出边界；触碰到自己的身体：蛇前进的下一格子为身体的一部分（即在列表中）。
'''
# 注：因为在列表中需要频繁添加和删除元素，所以用deque容器代替列表；是因为deque具有高效的插入和删除效率
# 初始化蛇，长度为3，放置在屏幕左上角；
# 导包
import random
import sys
import time
import pygame
from pygame.locals import *
from collections import deque

# 基础设置
Screen_Height = 480
Screen_Width = 600
Size = 20  # 小方格大小
Line_Width = 1
# 游戏区域的坐标范围
Area_x = (0, Screen_Width // Size - 1)  # 0是左边界，1是右边界 #注：python中//为整数除法；/为浮点数除法
Area_y = (2, Screen_Height // Size - 1)
# 食物的初步设置
# 食物的分值+颜色
Food_Style_List = [(10, (255, 100, 100)), (20, (100, 255, 100)), (30, (100, 100, 255))]
# 整体颜色设置
Light = (100, 100, 100)
Dark = (200, 200, 200)
Black = (0, 0, 0)
Red = (200, 30, 30)
Back_Ground = (40, 40, 60)

if_start = "false"
difficulty = 1

# 文本输出格式设置
def Print_Txt(screen, font, x, y, text, fcolor=(255, 255, 255)):
    # font.render参数意义：.render（内容，是否抗锯齿，字体颜色，字体背景颜色）
    Text = font.render(text, True, fcolor)
    screen.blit(Text, (x, y))


# 初始化蛇
def init_snake():
    snake = deque()
    snake.append((2, Area_y[0]))
    snake.append((1, Area_y[0]))
    snake.append((0, Area_y[0]))
    return snake


# 食物设置
# 注意需要对食物出现在蛇身上的情况进行判断
def Creat_Food(snake):
    """
    注：randint 产生的随机数区间是包含左右极限的，
    也就是说左右都是闭区间的[1, n]，能取到1和n。
    而 randrange 产生的随机数区间只包含左极限，
    也就是左闭右开的[1, n)，1能取到，而n取不到。randint
    产生的随机数是在指定的某个区间内的一个值，
    而 randrange 产生的随机数可以设定一个步长，也就是一个间隔。
    """
    food_x = random.randint(Area_x[0], Area_x[1])  # 此处有疑问
    food_y = random.randint(Area_y[0], Area_y[1])
    # 如果食物出现在蛇上，重来；
    while (food_x, food_y) in snake:
        food_x = random.randint(Area_x[0], Area_x[1])
        food_y = random.randint(Area_y[0], Area_y[1])
    return food_x, food_y


# 食物风格
def Food_Style():
    return Food_Style_List[random.randint(0, 2)]  # 返回随机的分值和颜色

def start_game():
    # 1.初始化操作
    pygame.init()

    # 2.创建游戏窗口
    window_size_width = 600
    window_size_height = 480
    window = pygame.display.set_mode((window_size_width, window_size_height))

    # 设置游戏标题
    pygame.display.set_caption('贪吃蛇')

    font = pygame.font.Font("C:/Windows/Fonts/STXINWEI.TTF", 30)

    window.fill(Back_Ground)
    Print_Txt(window, font, 250, 50, f'贪吃蛇')

    # 1.开始按钮
    bx1, by1, bw1, bh1 = 225, 150, 150, 50
    pygame.draw.rect(window, (0, 255, 0), (bx1, by1, bw1, bh1))
    text1 = font.render("开始游戏", True, (255, 255, 255))
    tw1, th1 = text1.get_size()
    tx1, ty1 = bx1 + bw1 / 2 - tw1 / 2, by1 + bh1 / 2 - th1 / 2
    window.blit(text1, (tx1, ty1))

    # 2.退出按钮
    bx2, by2, bw2, bh2 = 250, 300, 100, 50
    pygame.draw.rect(window, (255, 0, 0), (bx2, by2, bw2, bh2))
    text2 = font.render("退出", True, (255, 255, 255))
    tw2, th2 = text2.get_size()
    tx2, ty2 = bx2 + bw2 / 2 - tw2 / 2, by2 + bh2 / 2 - th2 / 2
    window.blit(text2, (tx2, ty2))
    pygame.display.update()

    # 3.让游戏保持一直运行的状态
    while True:
        # 4.检测事件
        for event in pygame.event.get():
            # 对事件作出相应的响应
            if event.type == pygame.QUIT:  # 如果点击了关闭按钮
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # 如果鼠标按下
                mx, my = event.pos  # 获取鼠标点击的位置
                if bx1 + bw1 >= mx >= bx1 and by1 + bh1 >= my >= by1:
                    pygame.draw.rect(window, (200, 200, 200), (bx1, by1, bw1, bh1))
                    window.blit(text1, (tx1, ty1))
                    pygame.display.update()
                elif bx2 + bw2 >= mx >= bx2 and by2 + bh2 >= my >= by2:
                    pygame.draw.rect(window, (200, 200, 200), (bx2, by2, bw2, bh2))
                    window.blit(text2, (tx2, ty2))
                    pygame.display.update()

            if event.type == pygame.MOUSEBUTTONUP:
                mx, my = event.pos  # 获取鼠标点击的位置
                if bx1 + bw1 >= mx >= bx1 and by1 + bh1 >= my >= by1:
                    pygame.draw.rect(window, (0, 255, 0), (bx1, by1, bw1, bh1))
                    window.blit(text1, (tx1, ty1))
                    pygame.display.update()
                    pygame.quit()
                    Set_diffculity()
                    print("开始游戏")
                elif bx2 + bw2 >= mx >= bx2 and by2 + bh2 >= my >= by2:
                    pygame.draw.rect(window, (255, 0, 0), (bx2, by2, bw2, bh2))
                    window.blit(text2, (tx2, ty2))
                    pygame.display.update()
                    sys.exit()
                    print("退出游戏")



def Set_diffculity():

    global difficulty

    # 1.初始化操作
    pygame.init()

    # 2.创建游戏窗口
    window_size_width = 600
    window_size_height = 480
    window = pygame.display.set_mode((window_size_width, window_size_height))

    # 设置游戏标题
    pygame.display.set_caption('贪吃蛇')

    font = pygame.font.Font("C:/Windows/Fonts/STXINWEI.TTF", 30)

    window.fill(Back_Ground)
    Print_Txt(window, font, 245, 50, f'难度选择')
    # 1.简单按钮
    bx1, by1, bw1, bh1 = 250, 130, 100, 50
    pygame.draw.rect(window, (255, 0, 0), (bx1, by1, bw1, bh1))
    text1 = font.render("简单", True, (255, 255, 255))
    tw1, th1 = text1.get_size()
    tx1, ty1 = bx1 + bw1 / 2 - tw1 / 2, by1 + bh1 / 2 - th1 / 2
    window.blit(text1, (tx1, ty1))

    # 2.普通按钮
    bx2, by2, bw2, bh2 = 250, 230, 100, 50
    pygame.draw.rect(window, (0, 255, 0), (bx2, by2, bw2, bh2))
    text2 = font.render("普通", True, (255, 255, 255))
    tw2, th2 = text2.get_size()
    tx2, ty2 = bx2 + bw2 / 2 - tw2 / 2, by2 + bh2 / 2 - th2 / 2
    window.blit(text2, (tx2, ty2))

    # 3.困难按钮
    bx3, by3, bw3, bh3 = 250, 330, 100, 50
    pygame.draw.rect(window, (0, 255, 0), (bx3, by3, bw3, bh3))
    text3 = font.render("困难", True, (255, 255, 255))
    tw3, th3 = text3.get_size()
    tx3, ty3 = bx3 + bw3 / 2 - tw3 / 2, by3 + bh3 / 2 - th3 / 2
    window.blit(text3, (tx3, ty3))

    pygame.display.update()

    # 3.让游戏保持一直运行的状态
    while True:
        # 4.检测事件
        for event in pygame.event.get():
            # 对事件作出相应的响应
            if event.type == pygame.QUIT:  # 如果点击了关闭按钮
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:  # 如果鼠标按下
                mx, my = event.pos  # 获取鼠标点击的位置
                if bx1 + bw1 >= mx >= bx1 and by1 + bh1 >= my >= by1:
                    pygame.draw.rect(window, (200, 200, 200), (bx1, by1, bw1, bh1))
                    window.blit(text1, (tx1, ty1))
                    pygame.display.update()
                    difficulty = 1
                    print("简单按钮被点击")
                elif bx2 + bw2 >= mx >= bx2 and by2 + bh2 >= my >= by2:
                    pygame.draw.rect(window, (200, 200, 200), (bx2, by2, bw2, bh2))
                    window.blit(text2, (tx2, ty2))
                    pygame.display.update()
                    difficulty = 0.65
                    print("普通按钮被点击")
                elif bx3 + bw3 >= mx >= bx3 and by3 + bh3 >= my >= by3:
                    pygame.draw.rect(window, (200, 200, 200), (bx3, by3, bw3, bh3))
                    window.blit(text3, (tx3, ty3))
                    pygame.display.update()
                    difficulty = 0.35
                    print("困难按钮被点击")

            if event.type == pygame.MOUSEBUTTONUP:
                mx, my = event.pos  # 获取鼠标点击的位置
                if bx1 + bw1 >= mx >= bx1 and by1 + bh1 >= my >= by1:
                    pygame.draw.rect(window, (255, 0, 0), (bx1, by1, bw1, bh1))
                    window.blit(text1, (tx1, ty1))
                    pygame.display.update()
                    pygame.quit()
                    main()
                    print("简单按钮被松开")
                elif bx2 + bw2 >= mx >= bx2 and by2 + bh2 >= my >= by2:
                    pygame.draw.rect(window, (0, 255, 0), (bx2, by2, bw2, bh2))
                    window.blit(text2, (tx2, ty2))
                    pygame.display.update()
                    pygame.quit()
                    main()
                    print("普通按钮被松开")
                elif bx3 + bw3 >= mx >= bx3 and by3 + bh3 >= my >= by3:
                    pygame.draw.rect(window, (0, 255, 0), (bx3, by3, bw3, bh3))
                    window.blit(text3, (tx3, ty3))
                    pygame.display.update()
                    pygame.quit()
                    main()
                    print("困难按钮被松开")


def main():
    print("难度：",difficulty)
    pygame.init()
    screen = pygame.display.set_mode((Screen_Width, Screen_Height))  # 初始化一个准备显示的窗口或屏幕
    pygame.display.set_caption('贪吃蛇')  # Set the current window caption
    # 得分字体设置
    font1 = pygame.font.SysFont('SimHei', 24)
    # GO字体设置
    font2 = pygame.font.SysFont(None, 72)
    fwidth, fheight = font2.size('GAME OVER')  ###
    # 程序bug修复：如果蛇在向右移动，快速点击分别施加向下、向左的命令，向下的命令会被覆盖，只有向左的命令被接受，直接GameOver
    # b变量为了防止这个情况发生
    b = True
    # 蛇
    snake = init_snake()
    # 食物
    food = Creat_Food(snake)
    food_style = Food_Style()
    # 方向控制
    pos = (1, 0)  ###
    # 启动游戏相关变量初始化
    game_over = True  # 结束标志 # 是否开始，当start = True，game_over = True 时，才显示 GAME OVER
    game_start = False  # 开始标志
    score = 0  # 得分
    orispeed = 0.3 * difficulty  # 蛇初始速度
    speed = orispeed  # 蛇速度
    last_move_time = None
    pause = False  # 暂停
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if game_over:
                        game_start = True
                        game_over = False
                        b = True
                        snake = init_snake()
                        food = Creat_Food(snake)
                        food_style = Food_Style()
                        pos = (1, 0)
                        # 得分
                        score = 0
                        last_move_time = time.time()
                elif event.key == K_SPACE:
                    if not game_over:
                        pause = not pause
                # 以下为防止蛇在向右移动时按向左键，导致GameOver
                elif event.key in (K_UP, K_w):
                    if b and not pos[1]:  ###
                        pos = (0, -1)
                        b = False
                elif event.key in (K_DOWN, K_s):
                    if b and not pos[1]:
                        pos = (0, 1)
                        b = False
                elif event.key in (K_LEFT, K_a):
                    if b and not pos[0]:
                        pos = (-1, 0)
                        b = False
                elif event.key in (K_RIGHT, K_d):
                    if b and not pos[0]:
                        pos = (1, 0)
                        b = False
        # 填充背景色
        screen.fill(Back_Ground)
        ###
        # 画网格线、竖线
        for x in range(Size, Screen_Width, Size):
            pygame.draw.line(screen, Black, (x, Area_y[0] * Size), (x, Screen_Height), Line_Width)
        # 画网格线、横线
        for y in range(Area_y[0] * Size, Screen_Height, Size):
            pygame.draw.line(screen, Black, (0, y), (Screen_Width, y), Line_Width)
        # 蛇的爬行过程
        if not game_over:
            curTime = time.time()
            if curTime - last_move_time > speed:  ###
                if not pause:
                    b = True
                    last_move_time = curTime
                    next_s = (snake[0][0] + pos[0], snake[0][1] + pos[1])
                    # 如果吃到了食物
                    if next_s == food:
                        snake.appendleft(next_s)
                        score += food_style[0]
                        speed = orispeed - 0.03 * (score // 100)
                        food = Creat_Food(snake)
                        food_style = Food_Style()
                    else:
                        # 在区域内
                        if Area_x[0] <= next_s[0] <= Area_x[1] and Area_y[0] <= next_s[1] <= Area_y[
                            1] and next_s not in snake:
                            snake.appendleft(next_s)
                            snake.pop()
                        else:
                            game_over = True
        # 画食物
        if not game_over:
            '''
        rect(Surface,color,Rect,width=0)
第一个参数指定矩形绘制到哪个Surface对象上
第二个参数指定颜色
第三个参数指定矩形的范围（left，top，width，height）
第四个参数指定矩形边框的大小（0表示填充矩形）
         '''
        # 避免 GAME OVER 的时候把 GAME OVER 的字给遮住了
        pygame.draw.rect(screen, food_style[1], (food[0] * Size, food[1] * Size, Size, Size), 0)
        # 画蛇
        for s in snake:
            pygame.draw.rect(screen, Dark, (s[0] * Size + Line_Width, s[1] * Size + Line_Width,
                                            Size - Line_Width * 2, Size - Line_Width * 2), 0)
        Print_Txt(screen, font1, 30, 7, f'速度: {score // 100}')
        Print_Txt(screen, font1, 450, 7, f'得分: {score}')
        # 画GameOver
        if game_over:

            if game_start:
                # print('GameOver')
                Print_Txt(screen, font2, (Screen_Width - fwidth) // 2, (Screen_Height - fheight) // 2, 'GAME OVER', Red)
        pygame.display.update()


if __name__ == '__main__':
    start_game()
    # Set_diffculity()
    # main()
