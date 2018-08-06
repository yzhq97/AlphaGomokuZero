#-*- coding: utf-8 -*-
#author: Zhuoqian Yang yzhq97@buaa.edu.cn

import os
import tkinter as tk
import src.config as config
from PIL import ImageTk, Image

class IdleScene(tk.Frame):

    def __init__(self, master, game_app):
        self.master = master
        self.game_app = game_app

        tk.Frame.__init__(self, master)
        self.construct()

    def construct(self):
        self.idle_image = ImageTk.PhotoImage(Image.open(os.path.join(".", "img", "idle.jpg")))
        self.label = tk.Label(self, image=self.idle_image)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        self.label.pack()