#-*- coding: utf-8 -*-
#author: Zhuoqian Yang yzhq97@buaa.edu.cn

import tkinter as tk
import tkinter.font as tkf
import src.config as config
import os
from PIL import ImageTk, Image
from src.GameScene import GameScene

class WelcomeScene(tk.Frame):
    def __init__(self, master, game_app):
        self.game_app = game_app
        self.scn_width = game_app.scn_width
        self.scn_height = game_app.scn_height
        self.play_data = self.game_app.play_data
        tk.Frame.__init__(self, master,
                          height=self.scn_height,
                          background=config.BGCOLOR)
        self.construct()
        self.show_play_data()

    def construct(self):
        title_font = tkf.Font(family=config.FONTFAMILY, size=36, weight=tkf.BOLD)
        text_font = tkf.Font(family=config.FONTFAMILY, size=20)
        desc_font = tkf.Font(family=config.FONTFAMILY, size=16)

        self.title_panel = tk.Frame(self, pady=self.scn_height*0.1, bg=config.BGCOLOR)
        self.title_label = tk.Label(self.title_panel, height=1, text=u"五子棋",
                                    bg=config.BGCOLOR, font=title_font)
        self.title_label.pack()



        self.stats_panel = tk.Frame(self, pady=self.scn_height*0.05, bg=config.BGCOLOR)

        self.easy_var = tk.StringVar()
        self.medium_var = tk.StringVar()
        self.hard_var = tk.StringVar()
        desc_str = u"* 胜率数据通过统计展览期间对局数据得到"

        self.easy_label = tk.Label(self.stats_panel, height=2, bg=config.BGCOLOR, font=text_font,
                                     textvariable=self.easy_var)
        self.medium_label = tk.Label(self.stats_panel, height=2, bg=config.BGCOLOR, font=text_font,
                                   textvariable=self.medium_var)
        self.hard_label = tk.Label(self.stats_panel, height=2, bg=config.BGCOLOR, font=text_font,
                                   textvariable=self.hard_var)
        self.desc_label = tk.Label(self.stats_panel, height=2, bg=config.BGCOLOR, font=desc_font,
                                   text=desc_str)

        self.easy_label.pack()
        self.medium_label.pack()
        self.hard_label.pack()
        self.desc_label.pack()

        self.btn_panel = tk.Frame(self)

        self.easy_btn_image = ImageTk.PhotoImage(Image.open(os.path.join(".", "img", "easy_btn.png")))
        self.medium_btn_image = ImageTk.PhotoImage(Image.open(os.path.join(".", "img", "medium_btn.png")))
        self.hard_btn_image = ImageTk.PhotoImage(Image.open(os.path.join(".", "img", "hard_btn.png")))

        self.easy_mode_btn = tk.Button(self.btn_panel, command=self.on_easy,
                                       width=260, height=80, border=0,
                                       bg=config.BGCOLOR, activebackground=config.BGCOLOR,
                                       highlightbackground=config.BGCOLOR,
                                       image=self.easy_btn_image)

        self.medium_mode_btn = tk.Button(self.btn_panel, command=self.on_medium,
                                         width=260, height=80, border=0,
                                         bg=config.BGCOLOR, activebackground=config.BGCOLOR,
                                         highlightbackground=config.BGCOLOR,
                                         image=self.medium_btn_image)

        self.hard_mode_btn = tk.Button(self.btn_panel, command=self.on_hard,
                                       width=260, height=80, border=0,
                                       bg=config.BGCOLOR, activebackground=config.BGCOLOR,
                                       highlightbackground=config.BGCOLOR,
                                       image=self.hard_btn_image)
        self.easy_mode_btn.pack(side='top')
        self.medium_mode_btn.pack(side='top')
        self.hard_mode_btn.pack(side='top')

        self.title_panel.pack(side='top')
        self.btn_panel.pack(side='top')
        self.stats_panel.pack(side='top')

    def show_play_data(self):
        easy_str = u"简单模型：自我对弈训练6000局，它在展览期间执黑胜率%4.1f%% 执白胜率%4.1f%%" \
                   % (100 * self.play_data.easy_black_winrate(), 100 * self.play_data.easy_white_winrate())
        medium_str = u"中等模型：自我对弈训练8000局，它在展览期间执黑胜率%4.1f%% 执白胜率%4.1f%%" \
                     % (100 * self.play_data.medium_black_winrate(), 100 * self.play_data.medium_white_winrate())
        hard_str = u"困难模型：自我对弈训练15000局，它在展览期间执黑胜率%4.1f%% 执白胜率%4.1f%%" \
                   % (100 * self.play_data.hard_black_winrate(), 100 * self.play_data.hard_white_winrate())
        self.easy_var.set(easy_str)
        self.medium_var.set(medium_str)
        self.hard_var.set(hard_str)

    def on_easy(self):
        self.game_app.model = config.MODEL_EASY
        self.game_app.on_select_difficulty_finish()

    def on_medium(self):
        self.game_app.model = config.MODEL_MED
        self.game_app.on_select_difficulty_finish()

    def on_hard(self):
        self.game_app.model = config.MODEL_HARD
        self.game_app.on_select_difficulty_finish()

