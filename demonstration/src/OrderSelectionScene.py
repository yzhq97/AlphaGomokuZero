#-*- coding: utf-8 -*-
#author: Zhuoqian Yang yzhq97@buaa.edu.cn


import tkinter as tk
import tkinter.font as tkf
import src.config as config
import os
from PIL import ImageTk, Image

class OrderSelectionScene(tk.Frame):
    def __init__(self, master, game_app):
        self.game_app = game_app
        self.scn_height = game_app.scn_height
        tk.Frame.__init__(self, master,
                          height=self.scn_height,
                          background=config.BGCOLOR)
        self.construct()

    def construct(self):
        title_font = tkf.Font(family=config.FONTFAMILY, size=36, weight=tkf.BOLD)
        text_font = tkf.Font(family=config.FONTFAMILY, size=20)

        self.title_panel = tk.Frame(self, pady=self.scn_height * 0.2, bg=config.BGCOLOR)
        self.title_label = tk.Label(self.title_panel, height=1, text=u"请选择",
                                    bg=config.BGCOLOR, font=title_font)
        self.title_label.pack()

        self.btn_panel = tk.Frame(self)

        self.black_image = ImageTk.PhotoImage(Image.open(os.path.join(".", "img", "black_btn.png")))
        self.white_image = ImageTk.PhotoImage(Image.open(os.path.join(".", "img", "white_btn.png")))

        self.black_btn = tk.Button(self.btn_panel, command=self.on_black,
                                   width=260, height=80, border=0,
                                   bg=config.BGCOLOR, activebackground=config.BGCOLOR,
                                   highlightbackground=config.BGCOLOR,
                                   image=self.black_image)
        self.white_btn = tk.Button(self.btn_panel, command=self.on_white,
                                   width=260, height=80, border=0,
                                   bg=config.BGCOLOR, activebackground=config.BGCOLOR,
                                   highlightbackground=config.BGCOLOR,
                                   image=self.white_image)
        self.black_btn.pack(side='top')
        self.white_btn.pack(side='top')

        self.title_panel.pack(side='top')
        self.btn_panel.pack(side='top')

    def on_black(self):
        self.game_app.human_order = 0
        self.game_app.on_select_order_finish()

    def on_white(self):
        self.game_app.human_order = 1
        self.game_app.on_select_order_finish()