#!/usr/bin/env python
#-*- coding: utf-8 -*-
#author: Zhuoqian Yang yzhq97@buaa.edu.cn

from src.GameApp import GameApp
import tkinter as tk

root = tk.Tk()
window2 = tk.Toplevel()
GameApp(root, window2)
root.mainloop()