#-*- coding: utf-8 -*-
#author: Zhuoqian Yang yzhq97@buaa.edu.cn

import tkinter as tk
import os
from src.model.CrossPoint import CrossPoint
from PIL import ImageTk, Image

class ChessCanvas(tk.Canvas):

    def __init__(self, master=None, N=8, M=48):
        self.master = master

        self.N = N
        self.M = M
        self.width = N * M + M
        self.height = N * M + M
        self.piece_size = M / 3

        tk.Canvas.__init__(self, master,
                                height=self.height,
                                width=self.width)
        self.bg = ImageTk.PhotoImage(Image.open(os.path.join(".", "img", "wood.png")))
        self.create_image(0, 0, image=self.bg, anchor="nw")

        self.chess_points = []
        self.init_chess_points()
        self.init_chess_canvas()

        self.pieces = {}
        self.inds = {}

    def reset(self):
        for location, piece in self.pieces.items():
            self.delete(piece)
        for location, ind in self.inds.items():
            if ind is not None:
                self.delete(ind)
        self.pieces = {}
        self.inds = {}

    def init_chess_points(self):
        N, M = self.N, self.M
        self.chess_points = [[CrossPoint(i, j, M) for j in range(N)] for i in range(N)]

    def init_chess_canvas(self):
        N, M = self.N, self.M
        for i in range(N):  #绘制竖线
            self.create_line(self.chess_points[i][0].pixel_x,
                             self.chess_points[i][0].pixel_y,
                             self.chess_points[i][N-1].pixel_x,
                             self.chess_points[i][N-1].pixel_y,
                             width=1)

        for j in range(N):  #绘制横线
            self.create_line(self.chess_points[0][j].pixel_x,
                             self.chess_points[0][j].pixel_y,
                             self.chess_points[N-1][j].pixel_x,
                             self.chess_points[N-1][j].pixel_y,
                             width=1)
        for i in range(N):
            for j in range(N):
                r = M / 30.0
                self.create_oval(self.chess_points[i][j].pixel_x-r,
                                 self.chess_points[i][j].pixel_y-r,
                                 self.chess_points[i][j].pixel_x+r,
                                 self.chess_points[i][j].pixel_y+r,
                                 fill='black')

    def render_location(self, location, r, color, outline=None, text=None, text_color=None, width=3.0):
        i, j = location
        if outline is None: outline = color
        piece = self.create_oval(self.chess_points[i][j].pixel_x - r,
                                 self.chess_points[i][j].pixel_y - r,
                                 self.chess_points[i][j].pixel_x + r,
                                 self.chess_points[i][j].pixel_y + r,
                                 fill=color, outline=outline, width=width)
        ind = None
        if text is not None:
            ind = self.create_text(self.chess_points[i][j].pixel_x,
                             self.chess_points[i][j].pixel_y,
                             text=text, fill=text_color)

        self.pieces[location] = piece
        self.inds[location] = ind

    def delete_location(self, location):
        if self.pieces[location] is not None:
            self.delete(self.pieces[location])
        if self.inds[location] is not None:
            self.delete(self.inds[location])

