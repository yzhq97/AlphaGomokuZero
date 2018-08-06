#-*- coding: utf-8 -*-
#author: Zhuoqian Yang yzhq97@buaa.edu.cn

import os
import tkinter as tk
import tkinter.font as tkf
import src.config as config
from src.components.GameCanvas import GameCanvas
from PIL import ImageTk, Image

class GameScene(tk.Frame):

    def __init__(self, master, game_app):
        self.N = config.N
        self.scn_width = game_app.scn_width
        self.scn_height = game_app.scn_height
        self.canvas_width = self.scn_height
        self.canvas_height = self.scn_height
        self.M = self.canvas_height / (self.N+1)
        self.play_out = config.PLAYOUT
        self.model = None
        self.human_order = None

        self.master = master
        self.game_app = game_app
        self.play_data = self.game_app.play_data
        tk.Frame.__init__(self, master, background=config.BGCOLOR)

        self.construct()

    def reset(self):
        self.msg_text.set("")
        self.status_text.set("")
        self.stats_text.set("")
        self.canvas.reset()

    def construct(self):
        panel_width = (self.scn_width - self.scn_height)/2
        panel_height = self.scn_height

        title_font = tkf.Font(family=config.FONTFAMILY, size=24, weight=tkf.BOLD)
        msg_font = tkf.Font(family=config.FONTFAMILY, size=20)

        self.msg_text = tk.StringVar()
        self.status_text = tk.StringVar()
        self.stats_text = tk.StringVar()

        self.mid_frame = tk.Frame(self, background=config.BGCOLOR, padx=20)

        self.canvas = GameCanvas(self.mid_frame, self)
        self.canvas.pack()

        self.right_panel = tk.Frame(self, width=panel_width, height=panel_height, padx=10, background=config.BGCOLOR)

        self.title_label = tk.Label(self.right_panel, height=3, text=u"五子棋", bg=config.BGCOLOR, font=title_font)
        self.status_label = tk.Label(self.right_panel, height=3, bg=config.BGCOLOR, font=msg_font, textvariable=self.status_text)
        self.stats_label = tk.Label(self.right_panel, height=3, bg=config.BGCOLOR, font=msg_font, textvariable=self.stats_text)
        self.msg_label = tk.Label(self.right_panel, height=3, bg=config.BGCOLOR, font=msg_font, textvariable=self.msg_text)
        self.exit_image = ImageTk.PhotoImage(Image.open(os.path.join(".", "img", "exit_btn.png")))
        self.exit_btn = tk.Button(self.right_panel, command=self.on_exit,
                                   width=260, height=80, border=0,
                                   bg=config.BGCOLOR, activebackground=config.BGCOLOR,
                                   highlightbackground=config.BGCOLOR,
                                   image=self.exit_image)

        self.title_label.pack(side='top')
        self.status_label.pack(side='top')
        self.stats_label.pack(side='top')
        self.msg_label.pack(side='top')
        self.exit_btn.pack(side='top')

        self.mid_frame.pack(side='left')
        self.right_panel.pack(side='left')

    def start_game(self, model, human_order):
        self.reset()
        self.model = model
        self.human_order = human_order
        self.show_play_data()

        status_str = u"当前棋局："

        if model == config.MODEL_EASY:
            status_str += u"简单难度\n"
        elif model == config.MODEL_MED:
            status_str += u"中等难度\n"
        else:
            status_str += u"困难难度\n"

        if human_order == 0:
            status_str += u"人类执黑，AI执白"
        else:
            status_str += u"AI执黑，人类执白"

        self.status_text.set(status_str)

        self.canvas.game_start()

    def on_exit(self):
        self.canvas.pvn.close()
        self.game_app.on_game_exit()

    def on_game_end(self, winner):
        self.game_app.on_game_end(winner)
        self.show_play_data()

    def show_message(self, msg):
        self.msg_text.set(msg)

    def show_play_data(self):
        stats_str = u""

        if self.model == config.MODEL_EASY:
            stats_str += u"简单模型，自我对弈训练6000局\n"
            stats_str += u"该难度AI在展览期间胜率：\n" \
                         u"执黑%4.1f%% 执白%4.1f%%" % (
                100*self.play_data.easy_black_winrate(),
                100*self.play_data.easy_white_winrate()
            )
        elif self.model == config.MODEL_MED:
            stats_str += u"中等模型，自我对弈训练8000局\n"
            stats_str += u"该难度AI在展览期间胜率：\n" \
                         u"执黑%4.1f%% 执白%4.1f%%" % (
                100 * self.play_data.medium_black_winrate(),
                100 * self.play_data.medium_white_winrate()
            )
        else:
            stats_str += u"困难模型，自我对弈训练15000局\n"
            stats_str += u"该难度AI在展览期间胜率：\n" \
                         u"执黑%4.1f%% 执白%4.1f%%" % (
                100 * self.play_data.hard_black_winrate(),
                100 * self.play_data.hard_white_winrate()
            )

        self.stats_text.set(stats_str)


    def show_think(self, board, mcts_root):
        self.game_app.board = board
        self.game_app.mcts_root = mcts_root
        self.game_app.show_think()

    def show_think_finish(self):
        self.game_app.show_think_finish()