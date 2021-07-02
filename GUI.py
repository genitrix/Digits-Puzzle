import random
from itertools import chain
from sys import exit

import pygame
from pygame.locals import *

import IDA_Star


# 颜色类
class Color():
    WHITE = (255, 255, 255)
    SNOW = (255, 250, 250)
    BLUE = (144, 207, 248)
    RED = (255, 150, 150)
    IVORY = (255, 255, 240)
    BLACK = (41, 36, 33)
    TOMATO = (255, 99, 71)
    PURPLE = (204, 153, 255)
    PURPLE_CLICKED = (178, 102, 255)
    GREY = (128, 128, 128)


# 数码块大小
BlockWidth = 65

# init
pygame.init()
# 设置屏幕大小为720p（1280*720）
screen = pygame.display.set_mode((1280, 720))
NUM = 4


# CurrPiece class
class CurrPiece(pygame.Surface):
    font = pygame.font.Font(None, 32)

    def __init__(self, num):
        pygame.surface.Surface.__init__(self, (BlockWidth, BlockWidth))
        self.fill(Color.BLUE)
        text = CurrPiece.font.render(str(num), True, Color.WHITE)
        textRect = text.get_rect()
        textRect.center = (BlockWidth / 2, BlockWidth / 2)
        self.blit(text, textRect.topleft)


## des pieces
class DesPiece(pygame.Surface):
    font = pygame.font.Font(None, 32)

    def __init__(self, num):
        pygame.surface.Surface.__init__(self, (BlockWidth, BlockWidth))
        self.fill(Color.RED)
        text = CurrPiece.font.render(str(num), True, Color.WHITE)
        textRect = text.get_rect()
        textRect.center = (BlockWidth / 2, BlockWidth / 2)
        self.blit(text, textRect.topleft)


# 填充当前状态
def fill(source):
    pieces = []
    source.reverse()
    while len(source) >= 1:
        insert = source.pop()
        if insert != 0:
            pieces.append(CurrPiece(insert))
        else:
            pieces.append(0)
    return pieces


## 填充目标状态
def fill_des(source):
    pieces = []
    source.reverse()
    # print("stage")
    # print(source)
    while len(source) >= 1:
        insert = source.pop()
        if insert != 0:
            pieces.append(DesPiece(insert))
        else:
            pieces.append(0)
    return pieces


def text_objects(text, font):
    text_s = font.render(text, True, Color.BLACK)
    return text_s, text_s.get_rect()


# 按钮函数
# ac是点击后的
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    text_small = pygame.font.Font("font.TTF", 20)
    textSurf, textRect = text_objects(msg, text_small)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)


# 按钮触发函数：移动到下一个状态
def next_state():
    path = Game.path

    if Game.step < len(path):
        current_state = list(chain(*path[Game.step]))
        Game.curr_pieces = fill(current_state)
        # pygame.display.update()
        print('step', Game.step)
        print(path[Game.step])
        Game.step += 1
    elif Game.step == len(path):
        print("Reach target state")
        Game.step += 1


# 按钮触发函数：回到初始状态
def return_init_state():
    path = Game.path
    Game.step = 0
    current_state = list(chain(*path[Game.step]))
    Game.curr_pieces = fill(current_state)
    Game.step += 1
    # 打印初始状态
    print("Initial state:")
    print('step', 0)
    print(path[0])


# 按钮触发函数：刷新初始状态
def new_state():
    Game.ini_state = random.randint(1, 9)
    origin = IDA_Star.Source.source[Game.ini_state]
    (path, bound) = IDA_Star.ida_star(origin)
    Game.path = path
    Game.bound = bound
    Game.step = 0
    current_state = list(chain(*path[Game.step]))
    Game.curr_pieces = fill(current_state)
    Game.step += 1
    # 打印初始状态
    print("初始状态：")
    print('step', 0)
    print(path[0])


# GUI的主体
class Game():
    pieces = []
    # 降维，一维化
    # source = [[0, 1, 3, 4], [5, 2, 7, 8], [9, 6, 11, 12], [13, 10, 14, 15]]
    # source就是初始状态
    # 初始状态的选择
    ini_state = 9
    origin = IDA_Star.Source.source[ini_state]
    source = list(chain(*origin))
    org_des = IDA_Star.Source.des
    des = list(chain(*org_des))
    (path, bound) = IDA_Star.ida_star(origin)
    step = 1

    # 当前状态
    curr_pieces = fill(source)
    # 最终目标状态
    des_pieces = fill_des(des)
    current = 0

    def start_game(self):
        # 打印初始状态
        print("初始状态：")
        print('step', 0)
        print(self.path[0])
        while True:
            # Handle event
            event = pygame.event.wait()

            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    next_state()
            # 绘制屏幕背景
            screen.fill(Color.IVORY)

            # 绘制当前方块
            # 当前状态绘制的起点
            startPoint = (12, 12)
            cnt = 0
            for pieces in self.curr_pieces:
                if pieces == 0:
                    cnt += 1
                    continue
                else:
                    # X用余数，从1、2、3递增，而Y用商，每过4个增加1
                    xy = (startPoint[0] + (int(cnt % NUM)) * (BlockWidth + 12),
                          startPoint[1] + (int(cnt / NUM)) * (BlockWidth + 12))
                    screen.blit(pieces, xy)
                    # print("XY position")
                    # print(xy)
                    cnt += 1
            # screen.
            # pygame.display.flip()

            # 绘制目标固定方块
            # 当前状态绘制的起点
            start_des = (420, 12)
            cnt2 = 0
            for pieces in self.des_pieces:
                if pieces == 0:
                    cnt2 += 1
                    continue
                else:
                    # X用余数，从1、2、3递增，而Y用商，每过4个增加1
                    xy = (start_des[0] + (int(cnt2 % NUM)) * (BlockWidth + 12),
                          start_des[1] + (int(cnt2 / NUM)) * (BlockWidth + 12))
                    screen.blit(pieces, xy)
                    # print("XY position")
                    # print(xy)
                    cnt2 += 1

            # 绘制提示信息
            #
            font_large = pygame.font.Font('font.TTF', 42)
            font_medium = pygame.font.Font('font.TTF', 32)
            font_small = pygame.font.Font('font.TTF', 20)
            # font_large = pygame.font.Font(None, 72)
            text_src = font_large.render("Current State", True, Color.BLUE)
            text_dest = font_large.render("Target State", True, Color.RED)
            text_remind_1 = font_small.render("Press Enter or click to move the block", True, Color.GREY)
            text_remind_2 = font_large.render("The final state has been reached. Click to continue.", True, Color.GREY)
            text_remind_3 = font_small.render("Press ESC to exit the program", True, Color.GREY)

            text_src_rect = text_src.get_rect()
            text_src_rect.center = (574 / 4 + 5, screen.get_height() / 2)
            screen.blit(text_src, text_src_rect.topleft)

            text_dest_rect = text_dest.get_rect()
            text_dest_rect.center = (550, screen.get_height() / 2)
            screen.blit(text_dest, text_dest_rect.topleft)

            text_rmd1 = text_remind_1.get_rect()
            text_rmd1.center = (860, (BlockWidth + 12) * 3 + 12)
            screen.blit(text_remind_1, text_rmd1.center)

            text_rmd3 = text_remind_3.get_rect()
            text_rmd3.center = (860, (BlockWidth + 12) * 3 + 12 + 36)
            screen.blit(text_remind_3, text_rmd3.center)

            text_end = text_remind_2.get_rect()
            text_end.center = (screen.get_width() / 2, screen.get_height() / 2 + 170)

            if self.step >= len(self.path):
                screen.blit(text_remind_2, text_end.topleft)
                # pygame.display.update()

            # 设置按钮
            # 下一个状态
            button("Move digital block", 860, 12, 210, 65, Color.PURPLE, Color.PURPLE_CLICKED, next_state)
            # 回到初始状态
            button("Return to initial state", 860, BlockWidth + 12 * 2, 210, 65, Color.PURPLE, Color.PURPLE_CLICKED, return_init_state)
            # 刷新初始状态
            button("Modify initial state", 860, (BlockWidth + 12) * 2 + 12, 210, 65, Color.PURPLE, Color.PURPLE_CLICKED, new_state)
            # 展示GUI窗体
            # pygame.display.flip()
            icon = pygame.image.load("icon.png")
            pygame.display.set_icon(icon)
            pygame.display.set_caption("15 Digits Puzzle")
            pygame.display.flip()


# main
def main():
    while True:
        game = Game()
        game.start_game()
        # Draw
        screen.fill(Color.IVORY)


# start here
if __name__ == "__main__":
    main()
