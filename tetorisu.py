# -*- coding:utf-8 -*-
import tkinter as tk
import random

# 定数
BLOCK_SIZE = 25     # ブロックの縦横のサイズpx
FIELD_WIDTH = 10    # フィールドの幅
FIELD_HEIGHT = 20   # フィールドの高さ

MOVE_LEFT = 0   # 左にブロックを移動することを示す定数
MOVE_RIGHT = 1  # 右にブロックを移動することを示す定数
MOVE_DOWN = 2   # 下にブロックを移動することを示す定数

# ブロックを構成する正方形のクラス
class TetrisSquare():
    def __init__(self, x=0, y=0, color="gray"):
        # 一つの正方形を作成
        self.x = x
        self.y = y
        self.color = color

    def set_cord(self, x, y):
        # 正方形の座標を設定
        self.x = x
        self.y = y

    def get_cord(self):
        # 正方形の座標を取得
        return int(self.x), int(self.y)

    def set_color(self, color):
        # 正方形の色を設定
        self.color = color

    def get_color(self):
        # 正方形の色を取得
        return self.color

    def get_moved_cord(self, direction):
        # 移動後の正方形の座標を取得 

        # 移動前の正方形の座標を取得
        x, y = self.get_cord()

        #移動方向を考慮して移動後の座標を計算
        if direction == MOVE_LEFT:
            return x - 1, y
        elif direction == MOVE_RIGHT:
            return x + 1, y
        elif direction == MOVE_DOWN:
            return x, y + 1
        else:
            return x, y

# テトリス画面を描画するキャンバスクラス
class TetrisCanvas(tk.Canvas):
    def __init__(self, master, field):
        # テトリスを描画するキャンバスを作成

        canvas_width = field.get_width() * BLOCK_SIZE
        canvas_height = field.get_height() * BLOCK_SIZE

        # tk.Canvasクラスのinit
        super().__init__(master, width=canvas_width, height=canvas_height, bg="white")

        # キャンバスを画面上に設置
        self.place(x=25, y=25)

        # 10×20個の正方形を描画することでテトリスの画面を作成
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

        # 一つ前に描画したフィールド設定
        self.before_field = field

    def update(self, field, block):
        # テトリス画面をアップデート

        # 描画用のフィールド(フィールド＋ブロック)を作成
        new_field = TetrisField()
        for y in range(field.get_height()):
            for x in range(field.get_width()):
                square = field.get_square(x, y)
                color = square.get_color()

                new_square = new_field.get_square(x, y)
                new_square.set_color(color)
        #フィールドにブロックの正方形情報を合成
        if block is not None:
            block_squares = block.get_squares()
            for block_square in block_squares:
                #ブロックの正方形の座標と色を取得
                x, y = block_square.get_cord()
                color = block_square.get_color()

                #取得したフィールド上の正方形の色を更新
                new_field_square = new_field.get_square(x,y)
                new_field_square.set_color(color)

        #描画用のフィールドを用いてキャンバスに描画
        for y in range(field.get_height()):
            for x in range(field.get_width()):#
                
                #(x, y)座標のフィールドの色を取得
                new_square = self.before_field.get_square(x, y)
                new_color = new_square.get_color()

                #(x,y)座標が前回の描画時から変化しない場合は描画しない
                before_square = self.before_field.get_square(x, y)
                before_color = before_square.get_color()
                if(new_color == before_color):
                    continue

                x1 = x * BLOCK_SIZE
                x2 = (x + 1) * BLOCK_SIZE
                y1 = y * BLOCK_SIZE
                y2 = (y + 1) * BLOCK_SIZE
                #フィールドの各位置の色で長方形を描画
                self.create_rectangle(
                    x1,y1,x2,y2,
                    outline = "white", width = 1, fill = new_color
                )
        #前回描画したフィールドの情報を更新
        self.before_field = new_field

    #積まれたブロックの情報を管理するフィールドクラス
class TetrisField():
    def __init__(self):
        self.width = FIELD_WIDTH
        self.height = FIELD_HEIGHT

        #フィールドを初期化
        self.squares = []
        for y in range(self.height):
            for x in range(self.width):
                #フィールドを正方形インスタンスのリストとして管理
                self.squares.append(TetrisSquare(x, y, "gray"))

    def get_width(self):
        #'フィールドの正方形の数(横方向)を取得'
        return self.width

    def get_height(self):
        #'フィールドの正方形の数(縦方向)を取得'

        return self.height

    def get_squares(self):

        return self.squares

    def get_square(self, x, y):
        #'指定した座標の正方形を取得'

        return self.squares[y * self.width + x]

    def judge_game_over(self, block):
        #'ゲームオーバかを判断'

        # フィールド上ですでに埋まっている座標の集合作成
        no_empty_cord = set(square.get_cord() for square in self.get_squares() if square.get_color() != "gray")

        # ブロックがある座標の集合作成
        block_cord = set(square.get_cord() for square in block.get_squares())
        #ブロックの差表の集合とフィールド上に埋まっている座標の集合の積集合を作成
        collision_set = no_empty_cord & block_cord
        #積集合がからであればゲームオーバーではない
        if len(collision_set) == 0:
            ret = False
        else:
            ret = True

        return ret

    def judge_can_move(self, block, direction):
        #'指定した方向にブロックを移動できるかを判断'

        #フィールド上ですでに埋まっている座標の集合作成
        no_empty_cord = set(square.get_cord() for square in self.get_squares() if square.get_color() != "gray")
        #移動後のブロックがある座標の集合作成
        move_block_cord = set(square.get_moved_cord(direction) for square in block.get_squares())
        #フィールドからはみ出すかどうかを判断
        for x, y in move_block_cord:

            #はみ出す場合は移動できない
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                return False

        #移動後のブロックの座標の集合とフィールドのすでに埋まっている座標の集合の積集合を作成
        collision_set = no_empty_cord & move_block_cord

        #積集合が空なら移動可能
        if len(collision_set) == 0:
            ret = True
        else:
            ret = False
        return ret

    def fix_block(self, block):
        #'ブロックを固定してフィールドに追加'

        for square in block.get_squares():
            #ブロックに含まれる正方形の座標と色を取得
            x, y =square.get_cord()
            color = square.get_color()

            #その座標と色をフィールドに反映
            field_square = self.get_square(x, y)
            field_square.set_color(color)

    def delete_line(self):
        #'行の削除を行う'

        #全行に対して削除可能か調べていく
        for y in range(self.height):
            for x in range(self.width):
                #行内に一つでも空があると消せない
                square = self.get_square(x, y)
                if(square.get_color() == "gray"):
                    #次の行へ
                    break
            else:
                #break　されなかった場合はその行は空きがない
                #この行を削除し、この行の上側にある行を１行下に移動
                for down_y in range(y, 0, -1):
                    for x in range(self.width):
                        scr_square = self.get_square(x, down_y -1)
                        dst_square = self.get_square(x, down_y)
                        dst_square.set_color(scr_square.get_color())
                #一番上の行は必ず全て空きになる
                for x in range(self.width):
                    square = self.get_square(x, 0)
                    square.set_color("gray")
#テトリスのブロックのクラス
class TetrisBlock():
    def __init__(self):
        # 'テトリスのブロックを作成'

        #ブロックを構成する正方形のリスト
        self.squares = []

        #ブロックの形をランダムに決定
        block_type = random.randint(1, 4)

        #ブロックの形に応じて４つの正方形の座標と色を決定
        if block_type == 1:
            color = "red"
            cords = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2, 2],
                [FIELD_WIDTH / 2, 3],
            ]
        elif block_type == 2:
            color = "blue"
            cords = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2 - 1, 0],
                [FIELD_WIDTH / 2 - 1, 1],
            ]
        elif block_type == 3:
            color = "green"
            cords = [
                [FIELD_WIDTH / 2 - 1, 0],
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2, 1],
                [FIELD_WIDTH / 2, 2],
            ]
        elif block_type == 4:
            color = "orange"
            cords = [
                [FIELD_WIDTH / 2, 0],
                [FIELD_WIDTH / 2 - 1, 0],
                [FIELD_WIDTH / 2 - 1, 1],
                [FIELD_WIDTH / 2 - 1, 2],
            ]
        #決定した色と座標の正方形を作成してリストに追加
        for cord in cords:
            self.squares.append(TetrisSquare(cord[0], cord[1],color))
    def get_squares(self):
        # 'ブロックを構成する正方形を取得'

        # return [square for square in self.squares]
        return self.squares

    def move(self, direction):
        # 'ブロックを移動'

        #ブロックを構成する正方形を移動
        for square in self.squares:
            x, y = square.get_moved_cord(direction)
            square.set_cord(x, y)
#テトリスゲームを制御するクラス
class TetrisGame():

    def __init__(self, master):
        # 'テトリスのインスタンス作成'

        #ブロック管理リストを初期化
        self.field = TetrisField()

        #落下ブロックをセット
        self.block = None

        # テトリス画面をセット
        self.canvas = TetrisCanvas(master, self.field)

        #テトリス画面をセット
        self.canvas.update(self.field, self.block)

    def start(self, func):
        # 'テトリスを開始'

        #終了時に呼び出す関数をセット
        self.end_func = func

        #ブロック管理リストを初期化
        self.field = TetrisField()

        #落下ブロックを新規追加
        self.new_block()

    def new_block(self):
        # 'ブロックを新規追加'

        #落下中のブロックインスタンスを作成
        self.block = TetrisBlock()

        if self.field.judge_game_over(self.block):
            self.end_func()
            print("GAMEOVER")

        #テトリス画面をアップデート
        self.canvas.update(self.field, self.block)

    def move_block(self, direction):
        # 'ブロックを移動'

        #移動できる場合だけ移動する
        if self.field.judge_can_move(self.block, direction):

            #ブロックを移動
            self.block.move(direction)

            #画面をアップデート
            self.canvas.update(self.field, self.block)
        else:
            #ブロックがした方向に移動できなかった場合
            if direction == MOVE_DOWN:
                #ブロックを固定する
                self.field.fix_block(self.block)
                self.field.delete_line()
                self.new_block()

#イベントを受け付けてそのイベントに応じてテトリスを制御するクラス
class EventHandller():
    def __init__(self, master, game):
        self.master = master

        #制御するゲーム
        self.game = game

        #イベントを定期的に発行するタイマー
        self.timer = None

        #ゲームスタートボタンを設置
        button = tk.Button(master, text='START',command=self.start_event)
        button.place(x=25 + BLOCK_SIZE * FIELD_WIDTH + 25, y=30)

    def start_event(self):
        # 'ゲームスタートボタンを押されたときの処理'
        #テトリス開始
        self.game.start(self.end_event)
        self.running = True

        #タイマーセット
        self.timer_start()

        #キー操作入力受付開始
        self.master.bind("<Left>", self.left_key_event)
        self.master.bind("<Right>", self.right_key_event)
        self.master.bind("<Down>", self.down_key_event)

    def end_event(self):
        # 'ゲーム終了時の処理'
        self.running = False

        #イベント受付を停止
        self.timer_end()
        self.master.unbind("<Left>")
        self.master.unbind("<Right>")
        self.master.unbind("<Down>")

    def timer_end(self):
        # 'タイマーを終了'

        if self.timer is not None:
            self.master.after_cancel(self.timer)
            self.timer = None

    def timer_start(self):
        # タイマー開始

        if self.timer is not None:
            # タイマーを一旦キャンセル
            self.master.after_cancel(self.timer)

        #テトリス実行中の場合のみタイマー開始
        if self.running:
            #タイマーを開始
            self.timer = self.master.after(1000, self.timer_event)

    def left_key_event(self, event):
        # '左キー入力受付時の処理'

        #ブロックを左に動かす
        self.game.move_block(MOVE_LEFT)

    def right_key_event(self, event):
        # '右キー入力時の処理'

        #ブロックを右に動かす
        self.game.move_block(MOVE_RIGHT)
    def down_key_event(self, event):
        # '下キー入力時の処理'

        #ブロックを下に動かす
        self.game.move_block(MOVE_DOWN)

        #落下タイマーを再スタート
        self.timer_start()

    def timer_event(self):
        # 'タイマー満期になったときの処理'

        #下キー入力時と同じ処理を実行
        self.down_key_event(None)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        #アプリウィンドウの設定
        self.geometry("400x600")
        self.title("テトリス")

        #テトリス作成
        game = TetrisGame(self)

        #イベントハンドラー作成
        EventHandller(self, game)


def main():
    'main関数'

    #GUIアプリ生成
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    main()