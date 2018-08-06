#-*- coding: utf-8 -*-
#author: Zhuoqian Yang yzhq97@buaa.edu.cn

import os
import tkinter as tk
import tkinter.font as tkf
import src.config as config
from src.components.ThinkCanvas import ThinkCanvas
from src.components.GameCanvas import GameCanvas
from PIL import ImageTk, Image

class ThinkScene(tk.Frame):
    def __init__(self, master, game_app, board, mcts_root):
        self.N = config.N
        self.scn_width = game_app.scn_width
        self.scn_height = game_app.scn_height
        self.canvas_width = self.scn_height
        self.canvas_height = self.scn_height
        self.M = (self.canvas_height-200)/ 3 / (self.N+1)
        self.board = board
        self.mcts_root = mcts_root

        self.master = master
        self.game_app = game_app
        tk.Frame.__init__(self, master, background=config.BGCOLOR)

        self.construct()

    def construct(self):
        title_font = tkf.Font(family=config.FONTFAMILY, size=18, weight=tkf.BOLD)
        status_font = tkf.Font(family=config.FONTFAMILY, size=14)

        self.left_panel = tk.Frame(self, pady=10, bg=config.BGCOLOR)

        self.title_label = tk.Label(self.left_panel, font=title_font, height=1, text=u"AI思维过程展示", bg=config.BGCOLOR)
        self.desc_label = tk.Label(self.left_panel, font=status_font, height=15, width=32,
                                   wraplength = 375, anchor='w', justify='left',
                                   text=config.THINK_DESC, bg=config.BGCOLOR)
        self.close_image = ImageTk.PhotoImage(Image.open(os.path.join(".", "img", "close_btn.png")))
        self.close_btn = tk.Button(self.left_panel, command=self.show_think_finish,
                                  width=260, height=80, border=0,
                                  bg=config.BGCOLOR, activebackground=config.BGCOLOR,
                                  highlightbackground=config.BGCOLOR,
                                  image=self.close_image)
        self.title_label.pack(side='top')
        self.desc_label.pack(side='top')
        # self.close_btn.pack(side='top')

        self.main_panel = tk.Frame(self, padx=30, pady=10, bg=config.BGCOLOR)

        self.board_col_1 = tk.Frame(self.main_panel, padx=30, bg=config.BGCOLOR)
        self.desc_label_1 = tk.Label(self.board_col_1, font=title_font, height=1, text=u"第一轮", bg=config.BGCOLOR)
        self.canvas_1_1 = ThinkCanvas(self.board_col_1, self.N, self.M)
        self.desc_label_1_1 = tk.Label(self.board_col_1, font=status_font, height=1, text=u"走法1", bg=config.BGCOLOR)
        self.canvas_1_2 = ThinkCanvas(self.board_col_1, self.N, self.M)
        self.desc_label_1_2 = tk.Label(self.board_col_1, font=status_font, height=1, text=u"走法2", bg=config.BGCOLOR)
        self.canvas_1_3 = ThinkCanvas(self.board_col_1, self.N, self.M)
        self.desc_label_1_3 = tk.Label(self.board_col_1, font=status_font, height=1, text=u"走法3", bg=config.BGCOLOR)
        self.desc_label_1.pack(side='top')
        self.canvas_1_1.pack(side='top')
        self.desc_label_1_1.pack(side='top')
        self.canvas_1_2.pack(side='top')
        self.desc_label_1_2.pack(side='top')
        self.canvas_1_3.pack(side='top')
        self.desc_label_1_3.pack(side='top')
        self.board_col_1.pack(side='left')

        self.board_col_2 = tk.Frame(self.main_panel, padx=60, bg=config.BGCOLOR)
        self.desc_label_2 = tk.Label(self.board_col_2, font=title_font, height=1, text=u"第二轮", bg=config.BGCOLOR)
        self.canvas_2_1 = ThinkCanvas(self.board_col_2, self.N, self.M)
        self.desc_label_2_1 = tk.Label(self.board_col_2, font=status_font, height=1, text=u"走法1", bg=config.BGCOLOR)
        self.canvas_2_2 = ThinkCanvas(self.board_col_2, self.N, self.M)
        self.desc_label_2_2 = tk.Label(self.board_col_2, font=status_font, height=1, text=u"走法2", bg=config.BGCOLOR)
        self.canvas_2_3 = ThinkCanvas(self.board_col_2, self.N, self.M)
        self.desc_label_2_3 = tk.Label(self.board_col_2, font=status_font, height=1, text=u"走法3", bg=config.BGCOLOR)
        self.desc_label_2.pack(side='top')
        self.canvas_2_1.pack(side='top')
        self.desc_label_2_1.pack(side='top')
        self.canvas_2_2.pack(side='top')
        self.desc_label_2_2.pack(side='top')
        self.canvas_2_3.pack(side='top')
        self.desc_label_2_3.pack(side='top')
        self.board_col_2.pack(side='left')

        self.board_col_3 = tk.Frame(self.main_panel, padx=30, bg=config.BGCOLOR)
        self.desc_label_3 = tk.Label(self.board_col_3, font=title_font, height=1, text=u"第三轮", bg=config.BGCOLOR)
        self.canvas_3_1 = ThinkCanvas(self.board_col_3, self.N, self.M)
        self.desc_label_3_1 = tk.Label(self.board_col_3, font=status_font, height=1, text=u"走法1", bg=config.BGCOLOR)
        self.canvas_3_2 = ThinkCanvas(self.board_col_3, self.N, self.M)
        self.desc_label_3_2 = tk.Label(self.board_col_3, font=status_font, height=1, text=u"走法2", bg=config.BGCOLOR)
        self.canvas_3_3 = ThinkCanvas(self.board_col_3, self.N, self.M)
        self.desc_label_3_3 = tk.Label(self.board_col_3, font=status_font, height=1, text=u"走法3", bg=config.BGCOLOR)
        self.desc_label_3.pack(side='top')
        self.canvas_3_1.pack(side='top')
        self.desc_label_3_1.pack(side='top')
        self.canvas_3_2.pack(side='top')
        self.desc_label_3_2.pack(side='top')
        self.canvas_3_3.pack(side='top')
        self.desc_label_3_3.pack(side='top')
        self.board_col_3.pack(side='left')

        self.left_panel.pack(side='left')
        self.main_panel.pack(side='left')

    def show(self):
        self.canvas_1_1.show_think(self.board, self.mcts_root, level=0, order=0)
        self.canvas_1_2.show_think(self.board, self.mcts_root, level=0, order=1)
        self.canvas_1_3.show_think(self.board, self.mcts_root, level=0, order=2)

        self.canvas_2_1.show_think(self.board, self.mcts_root, level=1, order=0)
        self.canvas_2_2.show_think(self.board, self.mcts_root, level=1, order=1)
        self.canvas_2_3.show_think(self.board, self.mcts_root, level=1, order=2)

        self.canvas_3_1.show_think(self.board, self.mcts_root, level=2, order=0)
        self.canvas_3_2.show_think(self.board, self.mcts_root, level=2, order=1)
        self.canvas_3_3.show_think(self.board, self.mcts_root, level=2, order=2)

    def reset(self):
        self.canvas_1_1.reset()
        self.canvas_1_2.reset()
        self.canvas_1_3.reset()
        self.canvas_2_1.reset()
        self.canvas_2_2.reset()
        self.canvas_2_3.reset()
        self.canvas_3_1.reset()
        self.canvas_3_2.reset()
        self.canvas_3_3.reset()

    def show_think_finish(self):
        self.reset()
        self.game_app.show_think_finish()