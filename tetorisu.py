# -*- coding:utf-8 -*-
import tkinter as tk
import random

#定数
BLOCK_SIZE = 25 #ブロックの縦横のサイズpx
FIELD_WIDTH = 10 #フィールドの幅
FIELD_HEIGHT = 20 #フィールドの高さ

MOVE_LEFT = 0 #左にブロックを移動することを示す定数
MOVE_RIGHT = 1 #右にブロックを移動することを示す定数
MOVE_DOWN = 2 #下にブロックを移動することを示す定数

#ブロックを構成する正方形のクラス
class TtrisSquare():
    def __init__(self, x=0, y=0, color="gray"):
        '一つの正方形を作成'
        self.x = x
        self.y = y
        self.color = color

    def set_cold(self, x, y):
        '正方形の座標を設定'
        self.x = x
        self.y = y

    def get_cold(self):
        '正方形の座標を取得'
        return int(self.x), int(self.y)

    def set_color(self, color):
        '正方形の色を設定'

    def get_color(self):
        '正方形の色を取得'
        return self.color

    def get_moved_cord(self, direction):
        '移動後の正方形の座標を取得'

        #移動前の正方形の座標を取得
        x, y = self.get_cord()

        #移動方向を考慮して移動後の座標を計算
        if direction ==MOVE_LEFT:
            return x - 1, y
        elif direction == MOVE_RIGHT:
            return x + 1, y
        elif direction == MOVE_DOWN:
            return x, y + 1
        else:
            return x, y

#テトリス画面を描画するキャンバスクラス
class TetrisCanvas(tk.Canvas):
    def __init__(self, master, field):
        'テトリスを描画するキャンバスを作成'

        canvas_width = field.get_width() * BLOCK_SIZE
        canvas_height = field.get_height() * BLOCK_SIZE

        #tk.Canvasクラスのinit
        super().__init__(master, width=canvas_width,height=canvas_height, bg="white")

        #キャンバスを画面上に設置
        self.place(x=25, y=25)

        #10×20個の正方形を描画することでテトリスの画面を作成
        for y in range(field.get_height()):
            for x in range(field.get_width()):
                square = field.get_square(x, y)
                x1 = x * BLOCK_SIZE
                x2 = (x + 1) * BLOCK_SIZE
                y1 = y * BLOCK_SIZE
                y2 = (y + 1) * BLOCK_SIZE
                self.create_rectangle(
                    x1, y1, x2, y2,
                    outline="white", width=1,
                    fill=square.get_color()
                )

        #一つ前に描画したフィールド設定
        self.before_field = field

    def update(self, field, block):
        'テトリス画面をアップデート'

        #描画用のフィールド(フィールド＋ブロック)を作成
        new_field = TetrisField()
        for y in range(field.get_width()):
            square = field.get_square(x, y)
            color = square.get_color()

            new_square = new_field.get_square(x, y)
            new_square.set_color(color)
        #フィールドにブロックの正方形情報を合成
        if block is not None:
            block_squares = block.get_squares()
            for block_square in block_squares:
                #ブロックの正方形の座標と色を取得
                x, y = block